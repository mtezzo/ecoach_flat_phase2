# COPYRIGHT (c) 2008
# THE REGENTS OF THE UNIVERSITY OF MICHIGAN
# ALL RIGHTS RESERVED
#
# PERMISSION IS GRANTED TO USE, COPY, CREATE DERIVATIVE WORKS AND
# REDISTRIBUTE THIS SOFTWARE AND SUCH DERIVATIVE WORKS FOR NONCOMMERCIAL
# EDUCATION AND RESEARCH PURPOSES, SO LONG AS NO FEE IS CHARGED, AND SO
# LONG AS THE COPYRIGHT NOTICE ABOVE, THIS GRANT OF PERMISSION, AND THE
# DISCLAIMER BELOW APPEAR IN ALL COPIES MADE; AND SO LONG AS THE NAME OF
# THE UNIVERSITY OF MICHIGAN IS NOT USED IN ANY ADVERTISING OR PUBLICITY
# PERTAINING TO THE USE OR DISTRIBUTION OF THIS SOFTWARE WITHOUT SPECIFIC,
# WRITTEN PRIOR AUTHORIZATION.
#
# THIS SOFTWARE IS PROVIDED AS IS, WITHOUT REPRESENTATION FROM THE
# UNIVERSITY OF MICHIGAN AS TO ITS FITNESS FOR ANY PURPOSE, AND WITHOUT
# WARRANTY BY THE UNIVERSITY OF MICHIGAN OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE REGENTS OF THE
# UNIVERSITY OF MICHIGAN SHALL NOT BE LIABLE FOR ANY DAMAGES, INCLUDING
# SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, WITH RESPECT TO
# ANY CLAIM ARISING OUT OF OR IN CONNECTION WITH THE USE OF THE SOFTWARE,
# EVEN IF IT HAS BEEN OR IS HEREAFTER ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGES.

"""Parse the MTS dictionary format, with a particular eye toward
calculating derived characteristics.

Uses ElementTree to parse the format, but the ET is discarded when
finished; what remains is just a Python data structure with no ties to
the on-disk representation.
"""

import sys
import itertools
import sys
import tokenize
from cStringIO import StringIO
import copy
import math
import logging
log = logging.getLogger(__name__)

import itertools

from tailoring2.common import DeriveError, ET, set
from tailoring2 import elementutil, util
from tailoring2.textutil import parwrap
from tailoring2.basetype import Basetype, STANDARD_BASETYPES

# ------------------------------------------------------------

# Upon parsing with ET, this string is prefixed to every tag in the
# dictionary. We remove the prefix before processing.
CHCR_NAMESPACE = "{http://chcr.umich.edu}"


# ------------------------------------------------------------
class DictionaryConstructionError(Exception):
    """raised when there's some error in the dictionary that prevents it from
    being constructed
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg
        
    def __repr__(self):
        return "<DictionaryConstructionError: %s>" % (self.msg)
        

class DependencyError(Exception):
    """raised when a circular dependency (a cycle) is encountered during
    derived characteristic sorting
    """
    pass


class TextSubstitutionError(Exception):
    """wrapper error raised when there's some problem in a text substitution.
    The original error is retained in the 'err' attribute.
    """
    def __init__(self, message, err):
        Exception.__init__(self, message)
        self.msg = message
        self.err = err
        
    def __repr__(self):
        return "<TextSubstitutionError: %s (%s)>" % (self.msg, self.err)


class ValidationError(Exception):
    """raised when there's some problem validating a dictionary. See also
    the subject data validation errors lower in this module
    (SubjectDataValidationError and friends).
    """
    def __init__(self, message, value, restrictionset):
        Exception.__init__(self, message)
        self.msg = message
        self.value = value
        self.restrictionset = restrictionset

    def __repr__(self):
        return "<ValidationError: %s>" % self.msg

# ------------------------------------------------------------

def toposort(dependencies):
    """@param dependencies: a dictionary of {str: [str]} where the key is a
    characteristic name and the value is a list of characteristic names.
    The characteristics named in the item's value must be computed
    before the characteristic named in the key can be computed.
    
    @return: a list of characteristic names in dependency order, from
    fewest dependencies to most dependencies. (The exact order is not
    guaranteed across multiple runs.)
    
    Raise DependencyError if there is a cycle in the dependencies or if
    the dependency set is inconsistent (ie, a name is in a dependency
    sublist but not declared at the top level).
    
    Algorithm adapted from an Eric Lippert blog post.
    """
    result = []
    marked = set()
    in_progress = set()

    def visit(dependency):
        # modifies marked, in_progress, and result from enclosing scope;
        # reads but does not modify dependencies
        if dependency in marked:
            return
        if dependency in in_progress:
            raise DependencyError("cycle in %s" % dependency)
        in_progress.add(dependency)
        try:
            subdeps = dependencies[dependency]
        except KeyError:
            raise DependencyError("unknown name %s" % dependency)
        for child in subdeps:
            visit(child)
        in_progress.remove(dependency)
        marked.add(dependency)
        result.append(dependency)

    for dependency in dependencies:
        visit(dependency)
    return result
    
# ------------------------------------------------------------

class DataSource(object):
    """represents a data source object (eg, T0, T1, Baseline, SUMMARY)
    found in a dictionary. Note that although in a subject a data source
    contains characteristics, here in the dictionary the data source is
    just a marker -- it doesn't contain anything.
    """

    def __init__(self, name, is_derived=False):
        self.name = name
        self.is_derived = is_derived

    def __repr__(self):
        return "<Source: %s>" % self.name


class MTSDictionary(object):
    """Container for subject characteristics and other associated data
    like restrictions, sources, and keywords. Knows how to instantiate
    itself from a workbench-created xml file. Knows how to perform text
    substitutions and resolve characteristic dependencies.
    """

    NOSOURCE = DataSource('')  # empty string
    
    def __init__(self, characteristics, basetypes, restrictions,
            sources=None, keywords=None):
        """@param characteristics: a list of CharacteristicDefinition objects
        @param restrictions: a list of CharacteristicRestrictionSet objects
        
        Instance variables:
        - characteristics is a list of CharacteristicDefinition objects (the same
            list that was passed as a parameter)
        - char_index is a dict of chardefs by name
        - derived_chars is a set of the chardefs in the dictionary that are derived
        - primary_chars is a set of the chardefs that are not derived
        - basetypes is a list of Basetype objects
        - basetype_index is a dict of Basetype objects by name
        - restrictions is a list of CharacteristicRestrictionSet objects (same list as the
            parameter)
        - restriction_index is a dict of restrictionsets by name
        - sources is a list of DataSource objects
        - keywords is a set of strings, each a possible characteristic classification
        """
        self.characteristics = characteristics
        self.char_index = dict([(chardef.name, chardef) for chardef in self.characteristics])
        self.derived_chars = set([chardef for chardef in self.characteristics if chardef.is_derived])
        self.primary_chars = set([chardef for chardef in self.characteristics if not chardef.is_derived])
        self.restrictions = restrictions
        self.restriction_index = dict([(restriction.name, restriction) for restriction in self.restrictions])
        self.basetypes = basetypes
        self.basetype_index = dict([(basetype.name, basetype) for basetype in self.basetypes])
        self.sources = sources or [self.NOSOURCE]
        self.source_index = dict([(source.name, source) for source in self.sources])
        self.keywords = keywords or set([])
        self.nested_default_chars = self._make_nested_default_chars()
        def getprimarydefaults():
            # extract only the primary chars from self.mtsdict.nested_defaults
            # TODO: move minifunc out of __init__ and maybe combine with _make_nested_default_chars()
            nested_defaults = copy.deepcopy(self.nested_default_chars)
            for srcname, srcdata in nested_defaults.items():
                for key, val in srcdata.items():
                    cdef = self.char_index[key]
                    if cdef.is_derived:
                        del srcdata[key]
            return nested_defaults
        self.primary_defaults = getprimarydefaults()

    @classmethod
    def for_tree(cls, tree):
        """given an elementtree representing a dictionary structure, return
        a new MTSDictionary object. The tree should already have its namespaces
        stripped out.
        """
        restriction_container = tree.find('./restrictions')
        assert restriction_container is not None
        restrictions = [CharacteristicRestrictionSet.for_element(elem)
                for elem in restriction_container.findall('restriction')]
        restriction_lookup = dict([(restriction.name, restriction) for restriction in restrictions])
        basetype_container = tree.find('./basetypes')
        assert basetype_container is not None
        basetypes = [Basetype.for_element(elem)
                for elem in basetype_container.findall('basetype')]
        basetype_index = dict([(basetype.name, basetype) for basetype in basetypes])
        basetype_lookup = lambda n: basetype_index[n]
        chardefs = [CharacteristicDefinition.for_element(elem, basetype_lookup, restriction_lookup)
                for elem in tree.findall('.//characteristic')]
        sources_raw = [(elem.get('name'), util.string2bool(elem.get("derived", 0)))
                for elem in tree.findall('.//source')]
        sources = [DataSource(*source) for source in sources_raw]
        #Added the default Source to always be a part of the dictionary
        sources.append(MTSDictionary.NOSOURCE)
        # note that keyword order is discarded
        keywords = set([elem.get('name') for elem in tree.findall('.//keyword')])
        
        mtsdict = MTSDictionary(chardefs, basetypes, restrictions, sources, keywords)
        mtsdict.assign_dependencies()
        return mtsdict


    def transformed_dep(self, nametoken):
        """if pattern of nametoken is source.char, return as is
        - if char, as is
        - if char.property, return char
        - if first elem is neither source nor char, return None
        """
        log.debug("nametuple=%s", nametoken)
        nametuple = nametoken.split('.')
        if nametuple[0] in self.char_index:
            log.debug("first element is char")
            return nametuple[0]
        if nametuple[0] in self.source_index:
            log.debug("first element is source, checking second")
            try:
                if nametuple[1] in self.char_index:
                    log.debug("second element is char, checking source reciprocity")
                    chardef = self.char_index[nametuple[1]]
                    assert nametuple[0] in chardef.sources
                    log.debug("source.char -> true")
                    return nametoken
            except IndexError:
                # was source only(!)
                return None
        log.debug("no match -- false")
        return None


    def assign_dependencies(self):
        # calculate dependencies now that everything has been parsed out
        xt = default_dependency_extractor

        for chardef in self.derived_chars:
            log.debug(chardef)
            log.debug("expr=%s", chardef.derivedcalc.expression_string)
            raw_deps = [depset for depset in xt(chardef.derivedcalc.expression_string)]
            log.debug("raw=%s", raw_deps)
            transformed_deps = [self.transformed_dep(depset) for depset in raw_deps]
            log.debug("transformed=%s", transformed_deps)
            filtered_deps = [depset for depset in transformed_deps if depset is not None]
            log.debug("filtered=%s", filtered_deps)
            chardef.derivedcalc.dependencies = filtered_deps

        # store the orderings
        self.all_chars_topo = self._all_chars_topo()
        self.derived_chars_topo = self._derived_chars_topo()
        log.debug("derived_chars_topo: %s" % self.derived_chars_topo)
        

    @classmethod
    def for_file(cls, dictionary_file):
        """given a file-like object containing XML data for a dictionary,
        or a path to that file, create and return a new MTSDictionary object.
        """
        tree = ET.parse(dictionary_file)
        elementutil.removeNamespacesFromTree(tree, CHCR_NAMESPACE)
        return cls.for_tree(tree)

    @classmethod
    def DummyDictionary(cls):
        """in case the Workbench doesn't have a dictionary file to pass us"""
        return MTSDictionary([], STANDARD_BASETYPES, [])

    def __getattr__(self, name):
        """allow attribute-style access to the chardefs in char_index"""
        try:
            return self.char_index[name]
        except KeyError:
            raise AttributeError(name)
        
    def _all_chars_topo(self):
        """return a list of characteristics in dependency order, from
        fewest dependencies to most dependencies. (The exact order is
        not guaranteed across multiple runs.)
        """
        def dependencynames(chardef):
            """return a list of strings -- the names of the
            characteristics that this one depends on. Note that all the
            characteristics referred to must be in this dictionary;
            unrecognized names (eg, from a function library or from a
            different dictionary) are omitted.
            """
            if not chardef.is_derived:
                return []
            return [dep for dep in chardef.derivedcalc.dependencies
                    if dep in self.char_index]
        dependencymap = dict([(chardef.name, dependencynames(chardef))
                for chardef in self.characteristics])
        dependency_order = toposort(dependencymap)
        assert dependency_order is not None
        chars_order = [self.char_index[charname] for charname in dependency_order]
        return chars_order

    def _derived_chars_topo(self):
        return [char for char in self.all_chars_topo if char.is_derived]

    def _flat_dependency_map(self):
        """Calculates a mapping of Characteristic names to all of the
        non-derived characteristics names in this dictionary that it depends
        on directly or indirectly. Returns a dictionary,
        {<unicode>: set(<unicode>)}."""
        def desourceify(dependencyname):
            try:
                source, dependencyname = dependencyname.split('.', 1)
                if source not in self.source_index:
                    return source
                else:
                    dependencyname, rest = dependencyname.split('.', 1)
                    if dependencyname not in self.char_index:
                        return '%s.%s' % (dependencyname, rest)
            except ValueError:
                pass
            return dependencyname
        my_map = {}
        for chardef in self.all_chars_topo:
            deps = set()
            if chardef.is_derived:
                deplist = chardef.derivedcalc.dependencies
                for dep in deplist:
                    dep = desourceify(dep)
                    if dep in my_map and len(my_map[dep]) > 0:
                        deps.update(my_map[dep])
                    elif dep in self.char_index:
                        deps.add(dep)
            my_map[chardef.name] = deps
        return my_map

    def textsubs(self, chars):
        """Calculate the text substitutions for this dictionary and the
        given set of characteristics. Return a tuple of (result, errors).
        
        @param chars: a dict of characteristics. (It can also be a
        dict-like object like a ChainedDict or an evalcontext.) The
        items should be unsourced -- ie, with all characteristics at the
        top level rather than being nested under sources like T0 and T1.
        @return: a (result, errors) tuple: result is a dictionary of the
        characteristics that have had a text substitution made (omitting
        keys that had no substitution defined) and errors is a list of
        TextSubstitutionError instances.
        """
        result = {}
        errors = []
        for chardef in self.characteristics:
            charname = chardef.name
            try:
                subjectval = chars.get(charname)
                if not subjectval:
                    continue
                textsubval = chardef.textsub(subjectval)
                if not textsubval:
                    continue
                result[chardef] = textsubval
            except Exception, err:
                errors.append(TextSubstitutionError("%s" % charname, err))

        # purge keys with no substitution defined (eg, val=None or val=[None])
        def isnotempty(chardef, val):
            if chardef.is_multivalued:
                vals = val
                return [v for v in vals if v]
            return val
        result = dict((chardef.name, subval) for chardef, subval in result.items()
            if isnotempty(chardef, subval))
        return result, errors

    def default_chars(self):
        """mine the dictionary for defaults; return a dictionary of
        {charname: default-for-name}
        """
        return dict([(chardef.name, chardef.default) for chardef in self.characteristics])

    def _make_nested_default_chars(self):
        """return a subject-shaped dictionary of default characteristics.
        
        Slow and inefficient but should only need to be calculated once.
        """
        all = {}
        for source in self.sources:
            all[source.name] = current = {}
            for chardef in self.characteristics:
                if chardef.sources and source.name not in chardef.sources:
                    continue
                current[chardef.name] = chardef.default
        return all
        
def identity(o):
    """the simplist function ever: return the argument. Useful for standing in
    for the coercetype arguments in the methods that follow."""
    return o

class Restriction(object):
    t2valname = '__tailoring2_value_name__'
    
    def expression(self, name):
        return "True"
    
    def isvalid(self, value):
        localz = {self.t2valname: value}
        return eval(self.expression(self.t2valname), {}, localz)

class ValueRestriction(Restriction):
    """a possible characteristic value that is discrete and (optionally)
    enumerated
    """
    def __init__(self, symbol, text=None, textsub=None, mapto=None):
        self.symbol = symbol
        self.text = text
        self.textsub = textsub
        self.mapto = mapto
        if mapto is not None:
            try:
                self.mapto = int(mapto)
            except ValueError, err:
                raise DictionaryConstructionError("cannot convert mapto value %s to an int" % repr(mapto))
    
    def expression(self, name):
        return "%s == %r" % (name, self.symbol)
    
    @classmethod
    def for_element(cls, elem):
        return cls(**dict((k, v) for k, v in elem.items()
            if k in frozenset(('symbol', 'text', 'textsub', 'mapto'))))


class InclusionRestriction(Restriction):
    unbounded_min = -sys.maxint - 1
    unbounded_max = sys.maxint

    def __init__(self, min, max):
        self.min, self.max = min, max
        self.message = 'must be between'
        self.message_post = ''
    
    def is_unbounded(self):
        return self.min == self.unbounded_min or self.max == self.unbounded_max
    
    def is_unbounded_lower(self):
        return self.min == self.unbounded_min
    
    def is_unbounded_upper(self):
        return self.max == self.unbounded_max        

    def expression(self, name):
        terms = [name]
        if self.min != self.unbounded_min:
            terms.insert(0, repr(self.min))
        if self.max != self.unbounded_max:
            terms.append(repr(self.max))
        return ' <= '.join(terms)

    @classmethod
    def for_element(cls, elem):
        return cls(**dict((k, v) for k, v in elem.items()
            if k in frozenset(('min', 'max'))))


class LengthRestriction(InclusionRestriction):
    unbounded_min = 0
    
    def __init__(self, min='', max=''):
        try:
            min = int(min)
        except ValueError:
            min = self.unbounded_min

        try:
            max = int(max)
        except ValueError:
            max = self.unbounded_max
                        
        super(LengthRestriction, self).__init__(min, max)
        self.message_post = ' characters long.'

    def expression(self, name):
        return super(LengthRestriction, self).expression('len(%s)' % name)
    
    @classmethod
    def for_element(cls, elem):
        return cls(**dict((k, v) for k, v in elem.items()
            if k in frozenset(('min', 'max'))))
    

class RangeRestriction(InclusionRestriction):
    def __init__(self, min='', max='', mintext=None,maxtext=None):
        try:
            min = float(min)
        except ValueError:
            min = self.unbounded_min
        
        try:
            max = float(max)
        except ValueError:
            max = self.unbounded_max
                        
        self.mintext = mintext
        self.maxtext = maxtext
        super(RangeRestriction, self).__init__(min, max)
    
    def __iter__(self):
        if self.is_unbounded():
            raise ValueError, 'Range is non-iterable if unbounded.'
        return iter(xrange(int(self.min), int(self.max) + 1))
    
    @classmethod
    def for_element(cls, elem):
        return cls(**dict((k, v) for k, v in elem.items()
            if k in frozenset(('min', 'max', 'mintext', 'maxtext'))))    
    

def ValueIterator(restrictionset, coercetype=identity):
    for restriction in restrictionset.all_restrictions:
        if isinstance(restriction, ValueRestriction):
            yield coercetype(restriction.symbol)
        elif isinstance(restriction, RangeRestriction):
            for val in iter(restriction):
                yield val
                
def SurveyValueIterator(restrictionset, coercetype=identity):
    for restriction in restrictionset.all_restrictions:
        if isinstance(restriction, ValueRestriction):
            yield {'response_value':coercetype(restriction.symbol), 'response_text':restriction.text}
        elif isinstance(restriction, RangeRestriction):
            for val in iter(restriction):
                text = val
                if restriction.min == val:
                    text = restriction.mintext if restriction.mintext else text
                if restriction.max == val:
                    text = restriction.maxtext if restriction.maxtext else text                    
                yield {'response_value':val, 'response_text':text}                  

class CharacteristicRestrictionSet(object):
    """Characteristics can have restrictions attached to them for
    validation purposes.

    This is an incomplete implementation: it's mostly here for text
    substitution lookup and dictionary-defined characteristic
    validation.
    """
    def __init__(self, name, restrictions):
        # TODO: currently ignores function restrictions
        self.name = name
        self.all_restrictions = restrictions or []
        self.values = [r for r in self.all_restrictions
            if isinstance(r, ValueRestriction)]
        self.ranges = [r for r in self.all_restrictions
            if isinstance(r, RangeRestriction)]
        self.lengths = [r for r in self.all_restrictions
            if isinstance(r, LengthRestriction)]
        self.value_index = dict((val.symbol, val) for val in self.values)
        # TODO: add the other restriction types here        
    
    def _values_expression(self, name, coercetype):
        values = [repr(coercetype(val)) for val in self.value_index]
        if len(values) == 0:
            valueexpression = None
        elif len(values) == 1:
            valueexpression = '%s == %s' % (name, values[0])
        else:
            valueexpression = '%s in (%s)' % (name, ','.join(values))
        return valueexpression
    
    def _inclusion_expression(self, name, coercetype):
        valuesexpression = self._values_expression(name, coercetype)
        inclusionexpressions = [r.expression(name) for r in self.ranges]
        if valuesexpression:
            inclusionexpressions.append(valuesexpression)
        return parwrap(' or '.join(parwrap(e) for e in inclusionexpressions))
    
    def _properties_expression(self, name, coercetype):
        lengthexpressions = [l.expression(name) for l in self.lengths]
        return parwrap(' and '.join(parwrap(e) for e in lengthexpressions))
    
    def expression(self, name, coercetype=identity, include_properties=True):
        inclusions = self._inclusion_expression(name, coercetype)
        properties = self._properties_expression(name, coercetype)
        expressions = []
        if inclusions:
            expressions.append(inclusions)
        if properties and include_properties:
            expressions.append(properties)
        return parwrap(' and '.join(parwrap(e) for e in expressions))
    
    def validate(self, value, coercetype=identity):
        # test for membership of inclusion rules
        if self.values or self.ranges:
            def testvalue(valuerestriction):
                return coercetype(valuerestriction.symbol) == value
            valuetests = (testvalue(vr) for vr in self.values)
            rangetests = (r.isvalid(value) for r in self.ranges)
            inclusiontests = itertools.chain(valuetests, rangetests)
            if not any(inclusiontests):
                raise ValidationError(
                    "value '%s' not recognized for %s" % (value, self.name),
                    value=value, restrictionset=self)
        if self.lengths:
            for length in self.lengths:
                if not length.isvalid(value):
                    raise ValidationError(
                        "value %r is not between %s and %s characters long for %s" %
                        (value, length.min, length.max, self.name),
                        value=value, restrictionset=self)
    
    def textsub(self, symbol):
        try:
            return self.value_index[unicode(symbol)].textsub
        except KeyError:
            return None

    @classmethod
    def for_element(cls, elem):
        """@param elem: a <restriction> element to inspect and extract
        properties from. (It's something else's responsibility to iterate through
        the <restrictions> container.)
        @return: an instantiated CharacteristicRestrictionSet object
        """
        name = elem.get("name")
        restrictionbuilders = {
            'value': ValueRestriction.for_element,
            'range': RangeRestriction.for_element,
            'length': LengthRestriction.for_element
        }
        restrictions = []
        for child in elem:
            try:
                builder = restrictionbuilders[child.tag]
            except KeyError:
                pass
            else:
                restrictions.append(builder(child))
        return CharacteristicRestrictionSet(name, restrictions)

    @classmethod
    def DummyRestrictionSet(cls):
        return cls('dummy', None)


def safe_convert_with_basetype(basetype, val):
    """return val as converted into the specified basetype, or just val
    if conversion fails
    """
    if val is None:
        return None
    try:
        return basetype.pytype(val)
    except (ValueError, TypeError), err:
        log.warn("couldn't convert %s to %s, skipping" % (repr(val), basetype))
    return val


class CharacteristicDefinition(object):
    """Properties of a given characteristic. In the file format, these
    are all stored as unicode strings. Some of them stay strings, but
    some become Python types.
        - name (unicode)
        - basetype (a type instance, like int or unicode)
        - default: object of one of the basetypes
        - is_required (bool)
        - is_derived (bool)
        - is_multivalued (bool)
        - sources (list of unicode)
        - keywords (set of unicode)
        - restrictionset (CharacteristicRestrictionSet object)
        - derivednote (unicode): only present if is_derived is true
        - derivedcalc (DerivedCalc instance): only present if is_derived is true
        - question (unicode): only present for NON-derived characteristics

    TODO: split into proper subclasses:
        PrimaryCharacteristicDefinition and DerivedCharacteristicDefinition
    """
        
    def validate(self, value):
        # raise if no good, otherwise pass silently
        validator = self.restrictionset.validate
        # if the value is a list-y object, test all values in the list
        if self.is_multivalued:
            if not util.isList(value):
                raise ValidationError(
                    "Values for '%s' must be in a list" % self.name,
                    value=value, restrictionset=None)
            for val in value:
                validator(val, self.basetype.pytype)
        else:
            validator(value, self.basetype.pytype)
    
    def validation_expression(self):
        """return an expression that will evaluate to True for all cases
        for which this characteristic is valid."""
        return self.restrictionset.expression(self.name, self.basetype.pytype)
    
    def valid_values_iterator(self):
        """return an iterator over the ordered set of valid values of this
        characteristic. The iterator will raise an Overflow value if it
        encounters a range restriction that is unbounded in some form. As
        a defense, consider checking valid_value_count()."""
        return ValueIterator(self.restrictionset, self.basetype.pytype)
    
    def valid_surveyvalues_iterator(self):
        """return an iterator over the ordered set of valid values of this
        characteristic. The iterator will raise an Overflow value if it
        encounters a range restriction that is unbounded in some form. As
        a defense, consider checking valid_value_count()."""
        return SurveyValueIterator(self.restrictionset, self.basetype.pytype)    
    
    def valid_value_count(self):
        """return the number of values that this characteristic has defined.
        This assumes that for any range restriction, there is a value for each
        whole integer value. If there are any unbounded ranges in the
        restriction set, this returns -1.
        """
        count = 0
        for range in self.restrictionset.ranges:
            if range.is_unbounded():
                return -1
            count += int(math.floor(range.max)) - int(math.ceil(range.min)) + 1
        count += len(self.restrictionset.value_index)
        return count
    
    def derive(self, evalglobals, evalcontext):
        """return the result of this chardef's derive calculation. Any
        exception that arises during the calculation will bubble up to
        the caller.
        
        @param evalglobals: true dictionary to be used as the 'globals'
            param in an eval() call. Typically comes out of a project's
            evaluation_globals attribute and contains builtins, authorutil,
            and any @exposed function extensions.
        @param evalcontext: mapping object to be used as the 'locals'
            param in an eval() call. Typically has characteristic values for
            the current subject and whatever additional lookups are
            necessary.
        """
        assert self.is_derived
        log.debug('>>>chardef.derive(%s): %s' % (self.name, self.derivedcalc.expression_string))
        expr = self.derivedcalc.expression
        if expr is None:
            # expression is a compiled code object. If it's None, that means there
            # was some kind of problem compiling the string. Go ahead and try
            # to evaluate the string and capture the resulting error.
            expr = self.derivedcalc.expression_string
        if not expr:
            log.info("assigning default to %s, expression is empty (%s)" % (self.name, expr))
            return self.default
        # this eval() might very well raise something (anything!)... caller must handle.
        dval = eval(expr, evalglobals, util.LaminatedDict(evalcontext))
        log.info("%s = %s" % (self.name, repr(dval)))
        return dval
        
    def textsub(self, value):
        # return textsub or None if nothing is defined for that value
        if self.is_multivalued:
            values = value
            return [self.restrictionset.textsub(val) for val in values if val]
        else:
            return self.restrictionset.textsub(value)
    
    def basetype_normalize(self, val):
        """normalize one value, converting it (or each element if
        multivalued) to the declared basetype. Return the converted
        value; silently return the original, unconverted value if the
        key isn't in the dictionary or if conversion failed for some
        reason.
        """
        if val is None:
            return None
        if self.is_multivalued:
            return [safe_convert_with_basetype(self.basetype, subval) for subval in val]
        else:
            return safe_convert_with_basetype(self.basetype, val)
    
    def __repr__(self):
        return "<Characteristic: %s>" % self.name

    @classmethod
    def for_element(cls, elem, basetype_lookup=None, restriction_lookup=None):
        """This is the designated initializer for this class: there is
        no useful __init__(). However, the class method synthesize() is
        an alternative initializer.
        
        @param elem: a <characteristic> element to inspect and
        extract properties from. All the properties become Python
        instances. The element is neither modified nor retained.
        @param basetype_lookup: a callable of one function converting a
            name (a string) into a Basetype object. If not passed, the
            standard basetype lookup will be used.
        @param restriction_lookup: a dict containing CharacteristicRestrictionSet
            objects indexed by name. If not passed, a dummy set will be used.
        @return: an initialized CharacteristicDefinition instance
        """
        if basetype_lookup is None:
            basetype_lookup = Basetype.string2basetype
            
        cdef = cls()
        
        name = elem.get('name')
        assert name is not None
        cdef.name = name

        basetype_name = elem.get('basetype')
        if basetype_name is None:
            raise DictionaryConstructionError("%s has no basetype" % name)
        try:
            cdef.basetype = basetype_lookup(basetype_name)
        except TypeError, err:
            raise DictionaryConstructionError("basetype '%s' unknown" % basetype_name)
        try:
            default_string = elem.get('default')
            if default_string is None:
                cdef._default = None
            else:
                cdef._default = cdef.basetype.pytype(default_string)
        except (TypeError, ValueError), err:
            raise DictionaryConstructionError("could not convert given default '%s' to type %s" %
                    (default_string, cdef.basetype.pytype))
        
        cdef.is_required = util.string2bool(elem.get('required'))
        cdef.is_multivalued = util.string2bool(elem.get('multivalued'))
        cdef.sources = [source.text.strip() for source in elem.findall('./sourceref')]
        if not cdef.sources:
            cdef.sources.append(MTSDictionary.NOSOURCE.name)
        cdef.keywords = set([kw.text.strip() for kw in elem.findall('./keywordref')])
        restriction_name = elem.get('restriction')
        if restriction_name is None or restriction_lookup is None:
            cdef.restrictionset = CharacteristicRestrictionSet.DummyRestrictionSet()
        else:
            try:
                cdef.restrictionset = restriction_lookup[restriction_name]
            except KeyError, err:
                missing_restriction = err.args[0]
                raise DictionaryConstructionError("missing restriction '%s'" % missing_restriction)                
        cdef.is_derived = util.string2bool(elem.get('derived'))
        if cdef.is_derived:
            dnote = elem.find('./derivednote')
            if dnote is not None:
                cdef.derivednote = dnote.text
            dcalc = elem.find('./derivedcalc')
            if dcalc is None:
                # quietly insert an empty calculation here so as to provide the least
                # surprising result
                dcalc = ET.Element('derivedcalc')
                dcalc.text = ''
            cdef.derivedcalc = DerivedCalc(dcalc.text)
            cdef.question = None
        else:
            try:
                cdef.question = elem.find('question').text
            except AttributeError:
                cdef.question = None
            
        return cdef
    
    @property
    def default(self):
        """return own default or delegate to basetype"""
        if self._default is not None:
            return self._default
        if self.is_multivalued:
            return []
        return self.basetype.default
    
    @classmethod
    def synthesize(cls, key, value):
        """Class method returns a permissive CharacteristicDefinition instance that
        is adapted to the key/value pair passed in.
        """
        def sniff_base_value(val):
            if not util.isList(val):
                return val
            # it's a list, so use the first value; if empty, use a string
            try:
                return val[0]
            except IndexError:
                # passed an empty list
                return '1'  # any dummy string
            except KeyError:
                # passed a dict -- use first value
                return sniff_base_value(val.values())
            
        cdef = cls()
        cdef.name = key
        base_value = sniff_base_value(value)
        cdef.basetype = Basetype.adapt(base_value)
        cdef._default = None  # defer to basetype
        cdef.is_required = False
        cdef.is_derived = False
        cdef.is_multivalued = util.isList(value)
        cdef.sources = [MTSDictionary.NOSOURCE.name]
        cdef.restrictionset = CharacteristicRestrictionSet.DummyRestrictionSet()
        return cdef

# ------------------------------------------------------------

def naive_dependency_extractor(expression_string):
    try:
        reader = StringIO(expression_string).readline
        calcvars = util.VariableCollector(reader, {}).scanvars()
        return set([name for name, value in calcvars])
    except tokenize.TokenError, err:
        # this happens if there was a syntax error in expression_string
        return set()

default_dependency_extractor = naive_dependency_extractor


class DerivedCalc(object):
    """data needed to calculate a derived characteristic
    - expression_string -- raw string expression
    - expression -- code object, compiled from expression_raw. If None, there was
            a syntax error in the expression string
    - dependencies -- set of characteristic names needed for
            expression evaluation
    """
    def __init__(self, expression_string, dependency_extractor=None):
        """expression_string is a valid Python expression.
        
        dependency_extractor is a function. It takes one arg, an
        expression string, and returns a set of strings, the names of
        the expression's dependencies. If not supplied, a naive
        implementation is used.
        """
        if expression_string is None:
            expression_string = ''
        if dependency_extractor is None:
            dependency_extractor = default_dependency_extractor

        try:
            self.expression = compile(expression_string, '<string>', 'eval')
        except SyntaxError, err:
            self.expression = None
            # not our problem, will get flagged way downstream when derive() happens
            pass
        
        self.expression_string = expression_string
        
        # moving this calculation up to the dictionary level where all the
        # necessary context is available
        self.dependencies = []

    def __repr__(self):
        return "<DerivedCalc: %s>" % self.expression_string



# ------------------------------------------------------------
# data validation -- first draft is migrated from realu2's tailorweb.model.subjects module

class SubjectDataValidationError(Exception):
    """Any error in subject validation. For now at least, the only
    operational difference between errors is in the string message.
    All instances have a 'key' ivar, though.
    
    TODO:
        - merge with ValidationError class above
    """
    def __init__(self, key, message):
        Exception.__init__(self, message)
        self.key = key
    def __repr__(self):
        return "SubjectValidationError in '%s': %s" % (self.key, self.message)

class UnsourcedKeyError(SubjectDataValidationError):
    def __init__(self, key):
        SubjectDataValidationError.__init__(self, key, self._message(key))
    def _message(self, key):
        return "top-level key '%s' is not a dictionary source" % key
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self._message(self.key))

class NotPythonDictionaryError(SubjectDataValidationError):
    def __init__(self, key, badval):
        SubjectDataValidationError.__init__(self, key, self._message(key, badval))
        self.badval = badval
    def _message(self, key, badval):
        return "top-level value '%s' is not a python dictionary: %s" % (key, type(badval))
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self._message(self.key, self.badval))

class CharacteristicLookupError(SubjectDataValidationError):
    def __init__(self, key):
        SubjectDataValidationError.__init__(self, key, self._message(key))
    def _message(self, key):
        return "characteristic '%s' not found in dictionary" % key
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self._message(self.key))

class MisdeclaredSourceError(SubjectDataValidationError):
    def __init__(self, key, badsource):
        SubjectDataValidationError.__init__(self, key, self._message(key, badsource))
        self.badsource = badsource
    def _message(self, key, badsource):
        return "characteristic '%s' submitted under a misdeclared source (%s)" % (key, badsource)
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self._message(self.key, self.badsource))

class PluralityMismatchError(SubjectDataValidationError):
    def __init__(self, key, badval):
        SubjectDataValidationError.__init__(self, key, self._message(key, badval))
        self.badval = badval
    def _message(self, key, badval):
        return "submitted characteristic %s = %s has wrong plurality" % (key, repr(badval))
    def __repr__(self):
        return "%s: submitted characteristic %s = %s has wrong plurality" %\
            (self.__class__.__name__, self._message(self.key, self.badval))

class BasetypeMismatchError(SubjectDataValidationError):
    def __init__(self, key, badval, expected_type):
        SubjectDataValidationError.__init__(self, key, self._message(key, badval, expected_type))
        self.badval = badval
        self.expected_type = expected_type
    def _message(self, key, badval, expected_type):
        return "submitted characteristic %s = %s is wrong expected type (%s)" %\
            (key, repr(badval), expected_type)
    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self._message(self.key, self.badval, self.expected_type))
        
    
class SubjectDataValidator(object):
    """validate submitted subject data against a dictionary. For now the
    subject data is a nested dictionary such as you might get from a
    JSON submission. Checks that characteristics are properly named and
    sourced.
    
    TODO: doesn't check char values against the dictionary's restrictions
        yet -- just checks char names.
    TODO: rework as a list of validators -- then all you have to do to customize
        is plug in your own validator(s)
    """
    # TODO: this class is a looted carcass -- plug the docstring into
    # mtsdict.validate() when ready
    pass
    
# ------------------------------------------------------------
# validator functions -- all take a dict of nested data, an optional
# mtsdict, and an optional validator-specific parameter (or sets of
# parameters). If the validator-specific functions are supplied, the
# function will use those. If they are not supplied, the function will use
# the mtsdict instead. (You must supply at least one of the keyword
# parameters.) All return a possibly-empty list of SubjectValidationError
# instances.
#
# (in future might provide a 'context' catch-all param for stuff that
# isn't covered)

def ValidateTopKeysAreSources(data, mtsdict=None, source_set=None):
    """insist top-level keys in data are mts dict sources"""
    if mtsdict is None and source_set is None:
        raise ValueError("must supply either mtsdict or source_set")
    if source_set is None:
        source_set = set(src.name for src in mtsdict.sources)
    def is_source(key):
        return key in source_set
    unsourced_keys = [key for key in data.keys() if not is_source(key)]
    unsourced_key_errors = [UnsourcedKeyError(key)
            for key in unsourced_keys]
    return unsourced_key_errors


def ValidateTopValuesAreDicts(data, mtsdict=None):
    """insist all top-level values are pydicts (or dict-like anyway). To
    preserve contract, accepts an mtsdict argument but ignores it.
    """
    try:
        nondict_items = [(key, val) for key, val in data.items() if not util.isDict(val)]
        return [NotPythonDictionaryError(key, val) for key, val in nondict_items]
    except AttributeError, err:
        return [NotPythonDictionaryError(data, data)]


def ValidateCharacteristicLookup(data, mtsdict=None, chardef_lookup=None):
    """insist all second-level keys are mtsdict characteristics
    which belong to the given source.        
    - data is a nested dictionary, the submitted subject data.
    - chardef_index is a one-arg function mapping names ->
    CharacteristicDefinition objects (result of None indicates not
    present). If not supplied, the mtsdict's built-in index will be
    used.
    """
    if mtsdict is None and chardef_lookup is None:
        raise ValueError("must supply either mtsdict or chardef_lookup")
    if chardef_lookup is None:
        chardef_lookup = mtsdict.char_index.get
    errors = []

    for submitted_source in data.keys():
        for charname, charval in data[submitted_source].items():
            chardef = chardef_lookup(charname)
            if chardef is None:
                errors.append(CharacteristicLookupError(charname))
                continue
            if not submitted_source in set(chardef.sources):
                errors.append(MisdeclaredSourceError(charname, submitted_source))
            # TODO someday: check charval against chardef's restrictions
            # ...
    return errors


def ValidateResponsePlurality(data, mtsdict=None, chardef_lookup=None):
    """submitting a single-response item to a mutliple-response type is
    a Bad Thing, and vice versa.
    """
    if mtsdict is None and chardef_lookup is None:
        raise ValueError("must supply either mtsdict or chardef_lookup")
    if chardef_lookup is None:
        chardef_lookup = mtsdict.char_index.get
    errors = []
    for submitted_source in data.keys():
        for charname, charval in data[submitted_source].items():
            chardef = chardef_lookup(charname)
            if chardef is None:
                # ignore this error -- should be caught by another validator
                log.warn("ignoring missing char '%s'" % charname)
                continue
            datum_is_list = util.isList(charval)
            if datum_is_list is not chardef.is_multivalued:
                errors.append(PluralityMismatchError(charname, charval))
    return errors


def ValidateBasetypes(data, mtsdict=None, chardef_lookup=None):
    """bad things: submitting a string to an int or float field; vice versa. Does _not_ do
    any kind of auto-coercion (eg, trying to take int("6") as opposed to int(6)).
    """
    if mtsdict is None and chardef_lookup is None:
        raise ValueError("must supply either mtsdict or chardef_lookup")
    if chardef_lookup is None:
        chardef_lookup = mtsdict.char_index.get
    errors = []
    for submitted_source in data.keys():
        for charname, charval in data[submitted_source].items():
            chardef = chardef_lookup(charname)
            if chardef is None:
                # ignore this error -- should be caught by another validator
                log.warn("ignoring missing char '%s'" % charname)
                continue
            if chardef.is_multivalued:
                if not util.isList(charval):
                    errors.append(BasetypeMismatchError(
                            charname, charval, []))
                    continue
                for subval in charval:
                    if not chardef.basetype.isinstance(subval):
                        errors.append(BasetypeMismatchError(
                                charname, subval, chardef.basetype))

            elif not chardef.basetype.isinstance(charval):
                # looks bad, but there's one allowed exception: ints can be posted to a float field
                if isinstance(charval, int) and chardef.basetype.pytype is float:
                    continue
                errors.append(BasetypeMismatchError(
                        charname, charval, chardef.basetype))

    return errors
