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

"""General utility functions used by the rest of the tailoring package.
"""

from __future__ import generators

import os,string
import urlparse
from urllib import pathname2url, url2pathname, quote, unquote
import types
import tokenize
import keyword
import __builtin__

try:
    set
except NameError:
    from sets import Set as set
    
# ------------------------------------------------------------

# Helpers for string2bool(). All comparisons are in lowercase, so no need
# to add mixed case or caps versions of these terms.
BOOL_TRUE = set(["true", "yes", "on", "enabled", "1"])
BOOL_FALSE = set(["false", "no", "off", "disabled", "0"])

# ------------------------------------------------------------

class Bunch:
    """Simple holder object -- like a dictionary but uses attribute-style
    access (obj.attr) instead of dict-style (obj['attr']). See Python Cookbook:
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def __repr__(self):
        return repr(self.__dict__)
        
    def __contains__(self, key):
        return key in self.__dict__

def isString(s):
    """basic test of string-ness -- more extensive code at this recipe:
            http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/305888

    >>> int(isString('hello'))
    1
    >>> int(isString(['hello']))
    0
    >>> int(isString(0))
    0
    >>> int(isString(u'hello'))
    1
    >>> int(isString(None))
    0
    """
    if isinstance(s, basestring):
        return True
    for method in ['index', 'count', 'replace']:
        if not hasattr(s, method):
            return False
        if not callable(getattr(s, method)):
            return False
    return True


def isList(alist):
    """Convenience method that works with all 2.x versions of Python
    to determine whether or not something is listlike.
    
    function copied from BeautifulSoup.py:
        http://www.crummy.com/software/BeautifulSoup/index.html
        (PSF license)

    >>> int(isList(0))
    0
    >>> int(isList([1]))
    1
    >>> int(isList(None))
    0
    >>> int(isList([]))
    1
    
    Tuples are list-like:
    >>> int(isList((1, 2)))
    1

    Strings, despite being sequences, are not listlike:
    >>> int(isList('hello'))
    0

    A dict is iterable, so it counts:
    >>> int(isList({1:2}))
    1
    >>> int(isList({1:2}.keys()))
    1
    
    """
    return hasattr(alist, '__iter__') \
           or (type(alist) in (types.ListType, types.TupleType))


def isDict(adict):
    """basic test of dict-ness.
    
    >>> intisdict = lambda d: int(isDict(d))
    >>> intisdict({})
    1
    >>> intisdict([])
    0
    >>> intisdict('a')
    0
    >>> intisdict(None)
    0
    >>> intisdict(0)
    0
    >>> cd = ChainedDict([dict(one=1), dict(two=2)])
    >>> intisdict(cd)
    1
    >>> isDict(Bunch(a=1, b=2))
    0
    """
    return hasattr(adict, '__getitem__') and not hasattr(adict, 'index')
    

def isNumber(aNumber):
    """Convenience test to check that a value is a basic python numeric type.
    
    >>> intIsNumber = lambda d: int(isNumber(d))
    >>> intIsNumber(1)
    1
    >>> intIsNumber(1.01)
    1
    >>> intIsNumber(1 + 2j)
    1
    >>> intIsNumber(1L)
    1
    >>> intIsNumber(None)
    0
    >>> intIsNumber('Hello World!')
    0
    >>> intIsNumber({})
    0
    >>> intIsNumber([])
    0
    >>> intIsNumber(())
    0
    """
    return (type(aNumber) in (types.IntType, types.LongType, types.FloatType,
                              types.ComplexType))

def execmodule(modulefile):
    """convenience for execmodules() -- for when you have only one module file.
    Returns a dictionary of the after-exec namespace.
    """
    return execmodules([modulefile])[-1]

    
def execmodules(modulefiles):
    """'execfile' each module in turn, returning a list of dictionaries with
    each of the intermediate results, oldest first
    """
    results = []
    for mod in modulefiles:
        if results:
            intermediate = results[-1].copy()
        else:
            intermediate = {}
        execfile(mod, globals(), intermediate)
        results.append(intermediate)
    return results


def file_contents_always_newlines(filepath):
    """return the contents of the file. Ensure that Windows line endings
    (\r\n) are converted to Unix line endings (\n).

    Useful for feeding the contents of a code module to Python's
    exec/eval machinery, which will choke unless it sees Unix's newlines.

    For files with Windows line endings, this matches the behavior of a
    file read in "universal newlines" mode (open(myfile, 'rU').read()),
    although it is much slower.

    Note that this function does NOT attempt to handle Classic Mac line
    endings (\r) because we don't run into many of those files anymore.

    If you know you're on a version of Python or Jython that supports
    'rU', just use that instead; this function is useful when your code
    may have to run under old environments.

    For the record, CPython 2.3+ and Jython 2.5+ support 'rU'; Jython
    2.2 does not.
      http://www.python.org/doc/2.3.5/whatsnew/node7.html
    """
    try:
        contents_raw = open(filepath, 'rU').read()
    except IOError, err:
        # jython doesn't have 'rU' yet, so we convert the newlines manually
        contents_raw = open(filepath, 'rb').read()
        if '\r\n' in contents_raw:
            contents_raw = contents_raw.replace('\r\n', '\n')
    return contents_raw


def module_names(modulepath, incoming_names=None):
    if incoming_names is None:
        names = {}
    else:
        names = incoming_names.copy()
    contents = file(modulepath, 'rU').read()
    exec contents in names
    return names
    
    
def evaluation_globals(modulepath):
    """return a dict containing the globals (modules, function defs) to be used
    for derivation.
    """
    if modulepath is None:
        return globals().copy()
    module_raw = file_contents_always_newlines(modulepath)        
    module = compile(module_raw, modulepath, 'exec')
    glb = globals().copy()
    exec module in glb
    return glb

# TEMP PLUGIN -- possibly a better name
module_names = evaluation_globals


def flatten(*args):
    """flatten a nested list or tuple... only works for these types, not custom containers
    
    - returns a generator for items, not a list
    
    see this recipe (H Krekel):
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/121294
        
    another recipe (by R Hettinger) and discussion thread:
        http://mail.python.org/pipermail/python-list/2004-October/246522.html

    >>> list(flatten([1, 2]))
    [1, 2]
    >>> list(flatten([1, [2]]))
    [1, 2]
    >>> list(flatten([1, 2, [3, 4], 5]))
    [1, 2, 3, 4, 5]
    >>> list(flatten([1, [2, [3, [4], 5], 6], 7]))
    [1, 2, 3, 4, 5, 6, 7]
    """
    for arg in args: 
        if type(arg) in (type(()),type([])):
            for elem in arg:
                for f in flatten(elem):
                    yield f
        else: yield arg


class ChainedDict(object):
    """Composes a list of dicts into a single dict-like class. On key
    lookup, each dict in the searchlist is searched in order until the
    key is found. The searchlist must contain dicts (or
    __getitem__-supporting objects).
    


    Here are a couple of sample dicts we'll use for illustration:
    >>> d1 = {'one': 1, 'two': 2}
    >>> d2 = {'one': 'one', 'three': 'three'}
    
    Specify the searchlist in order of precedence -- that is, put the
    most "important" dict first. For simple attribute access the
    ChainedDict behaves like a normal dict.
    >>> cdict = ChainedDict([d1, d2])
    >>> cdict['one']
    1
    >>> cdict['two']
    2
    >>> cdict['three']
    'three'
    
    If you ask for a nonexistent key, you get a KeyError. (Note that
    this test is wrapped in a try/except because Python and Jython
    return slightly different output in their KeyErrors, so the wrapper
    makes the test pass in both environments.)
    >>> try: cdict['four']
    ... except KeyError: 'missing key'
    'missing key'
    
    If you change the searchlist order, you get different results:
    >>> cdict2 = ChainedDict([d2, d1])
    >>> cdict2['one']
    'one'
    >>> cdict2['two']
    2
    >>> cdict2['three']
    'three'
    
    The cdict itself is not a dict instance, but you can call flatdict()
    to get one. (Note: the True/False tests below are wrapped in int()
    for compatibility with Jython 2.2, which represents True as 1 and
    False as 0.)
    >>> int(isinstance(cdict2, dict))
    0
    >>> int(isinstance(cdict2.flatdict(), dict))
    1
    
    Maybe in future we'll be a dict subclass and thus usable anywhere a
    real dict is needed -- but for now use the flatdict() method. The
    flatdict can be compared the way any dict can, as you'd expect:
    >>> int(cdict2.flatdict() == dict(one='one', two=2, three='three'))
    1
    >>> int(cdict.flatdict() == cdict2.flatdict())
    0
    
    The chained dict itself is read-only:
    >>> cdict['one'] = 'bugs'
    Traceback (most recent call last):
        ...
    TypeError: 'ChainedDict' object does not support item assignment
    
    But you can change the objects in the searchlist:
    >>> d1['one'] = 'bugs'
    >>> cdict['one']
    'bugs'

    You can also change the searchlist itself at any time. Before the change:
    >>> int(cdict.flatdict() == cdict2.flatdict())
    0
    
    After:
    >>> cdict.searchlist = cdict2.searchlist
    >>> int(cdict.flatdict() == cdict2.flatdict())
    1
    
    Despite it not being a dict instance, you can use a ChainedDict in eval():
    >>> eval("red", globals(), dict(red='#f00'))
    '#f00'
    >>> eval("red", globals(), ChainedDict([dict(red='#FF0000'), dict(red='#f00')]))
    '#FF0000'
    
    A ChainedDict also supports some of the other dict syntax:
    >>> int('one' in cdict)
    1
    >>> int('eighteen' in cdict)
    0
    >>> cdict.get('one')
    'one'
    >>> print cdict.get('eleventy')
    None
    >>> cdict.get('eleventy', 11)
    11
    
    For some discussion on this type of thing, see this thread:
        Intro with sys.get_frame() magic:
            http://mail.python.org/pipermail/python-list/2004-November/249237.html
        
        Advice: use chainmap():
            http://mail.python.org/pipermail/python-list/2004-November/249689.html

        See also Ka-Ping Yee's industrial-strength-templating module:
            http://mail.python.org/pipermail/python-list/2004-November/249409.html
    """
    
    def __init__(self, searchlist=None, name=None):
        self.searchlist = searchlist or []
        self.name = name
        
    def __getitem__(self, key):
        for aDict in self.searchlist:
            try:
                # JYTHON: guard clause here because if aDict is a java.util.Map,
                # it will happily return None/null for a missing key rather than
                # raising KeyError as the engine expects.
                if key not in aDict:
                    continue
                return aDict[key]
            except KeyError:
                pass
        raise KeyError(key)
    
    def __contains__(self, key):
        try:
            val = self.__getitem__(key)
            return True
        except KeyError:
            return False
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
            
    def flatdict(self):
        """return a standard dictionary composed of the values in the chained
        dict. key/value pairs earlier in the chained dict's searchList take precedence.
        
        Useful for eval(), which requires a true dict and not just a dict-like object.
        (Python 2.4 removes this limitation of eval().)
        """
        reverseSearchList = self.searchlist[:]
        reverseSearchList.reverse()
        flat = {}
        for aDict in reverseSearchList:
            # JYTHON: update() raises when aDict is actually a java.util.Map instance,
            # so we need to work around that. But update() is such a common operation
            # (and, in CPython, written in optimized C) that we create two different
            # code paths here.
            if hasattr(aDict, 'hashCode'):
                # assume this is a java instance (and further that it's a java.util.Map)
                # so do the update manually
                for key in aDict:
                    flat[key] = aDict[key]
            else:
                # ordinary python instance -- use optimized code path
                flat.update(aDict)
        return flat

    def append(self, aDict):
        """append a new component dictionary to the end of the searchlist
        """
        self.searchlist.append(aDict)

    def prepend(self, aDict):
        """add a new component dictionary at the beginning of the searchlist
        """
        self.searchlist.insert(0, aDict)

    def __setitem__(self, key, val):
        raise TypeError("'ChainedDict' object does not support item assignment")
    
    def __repr__(self):
#         return "%s: %s" % (repr(self.__class__), repr(self.flatdict()))
        clsname = self.__class__.__name__
        return "<%s '%s'>" % (clsname, self.name) if self.name\
            else "<%s>" % (clsname)            
        
    def keys(self):
        return self.flatdict().keys()


# defaults typically need to be applied source by source.
# nested dict of {sourcename: ChainedDict([allchars[src]+primary_defaults[src]])}
def nested_chained_dict(chain):
    """combine nested dictionaries into a nested dictionary of
    ChainedDict instances.

    @param chain: a list of dictionaries. Each dictionary is assumed to
    be nested, with the top-level keys mapping to other sub-dictionaries
    (in other words, each dictionary is subject-shaped).

    @return dict: a similarly nested dictionary, each of whose
    subdictionaries is a ChainedDict grouping subdictionaries by
    top-level-key in the order of occurrence in 'chain.' The returned
    dictionary's top-level keys will be the union of all the top-level
    keys in 'chain.'
    """
    result = {}
    setunion = lambda l1, l2: set(l1).union(l2)
    # all top-level keys of chain, no duplicates
    sources = reduce(setunion, chain)
    for src in sources:
        chain_segments = [item.get(src, {}) for item in chain]
        result[src] = ChainedDict(chain_segments, name=src)
    return result


class LaminatedDict(object):
    """
    Present a dict-like barrier around any dict-like object, protecting the
    wrapped object from modifications.  A LaminatedDict will accept item
    assignment and deletion, but only on a layer above the wrapped dictionary.
    This allows the laminated (wrapped) dictionary to be used in contexts where
    modification is necessary to the domain, but modifications shouldn't apply
    permanently.
    
    Consider the basic dictionary:
    >>> abcs = {'a': 'a', 'b': 'b', 'c': 'c'}
    
    We may not want to destroy our abcs, lest we upset the nature of the
    language in use.  So, we should laminate it, for preservation.
    
    >>> l = LaminatedDict(abcs)
    
    l is now available to do many mapping operations, without harming our abcs.
    
    And for testing purposes, let's create a handy function for sorted keys
    
    >>> def sortedkeys(d):
    ...     k = list(d.keys())
    ...     k.sort()
    ...     return k
    >>> int(l.keys() == abcs.keys())
    1
    >>> l['d'] = 'd'
    >>> sortedkeys(l)
    ['a', 'b', 'c', 'd']
    >>> sortedkeys(abcs)
    ['a', 'b', 'c']
    >>> int(l.keys() == abcs.keys())
    0
    
    >>> l['d'] = 'e' # ooo, look what we have here.
    >>> sortedkeys(l)
    ['a', 'b', 'c', 'd']
    >>> l['d']
    'e'
    >>> del l['a']
    >>> sortedkeys(l)
    ['b', 'c', 'd']
    >>> sortedkeys(abcs)
    ['a', 'b', 'c']
    >>> int(l['b'] == abcs['b'])
    1
    >>> l['b'] = 'q'
    >>> int(l['b'] == abcs['b'])
    0

    If you ask for a nonexistent key, you get a KeyError. (Note that
    this test is wrapped in a try/except because Python and Jython
    return slightly different output in their KeyErrors, so the wrapper
    makes the test pass in both environments.)
    >>> del l['b']
    >>> try: l['b']
    ... except KeyError: 'missing key'
    'missing key'
    >>> try: del l['b']
    ... except KeyError: 'missing key'
    'missing key'
    >>> del l['d']
    >>> sortedkeys(l)
    ['c']
    >>> abcs['b']
    'b'
    
    """
    
    def __init__(self, protected, temp=None, hidden=None):
        self.protected = protected
        if temp is None:
            self.tablecloth = {}
        else:
            self.tablecloth = temp
        if hidden is None:
            self.deleted = []
        else:
            self.deleted = hidden
    
    def __repr__(self):
        return "%s(temp=%r, protected=%r, hidden=%r)" % (
            self.__class__.__name__, self.tablecloth, self.protected,
            self.deleted )
    
    def __getitem__(self, key):
        if key in self.deleted:
            raise KeyError(key)
        try:
            return self.tablecloth[key]
        except KeyError:
            return self.protected[key]
    
    def __setitem__(self, key, val):
        self.tablecloth[key] = val
        if key in self.deleted:
            self.deleted.remove(key)
    
    def __contains__(self, key):
        try:
            val = self.__getitem__(key)
            return True
        except KeyError:
            return False
    
    def __delitem__(self, key):
        deleted = False
        if key in self.tablecloth:
            del self.tablecloth[key]
            deleted = True
        if key in self.protected and key not in self.deleted:
            self.deleted.append(key)
            deleted = True
        if not deleted:
            raise KeyError(key)
    
    def keys(self):
        keys = list(self.tablecloth.keys())
        keys.extend([key for key in self.protected.keys() if key not in self.deleted])
        return keys
    
    def flatten(self):
        d = {}
        d.update(self.protected)
        for k in self.deleted:
            del d[k]
        d.update(self.tablecloth)
        return d

def dictmerge(*dicts):
    """convenience -- take a list of dictionaries and merge them. First in the
    list takes precedence.
    """
    return ChainedDict(list(dicts)).flatdict()


class DottedLookup:
    """allow attribute-style lookup for the passed-in dict
    
    >>> d = dict(one=1, two=2)
    >>> dotted = DottedLookup(d)
    >>> dotted.one
    1
    >>> dotted.two
    2
    >>> try:
    ...     dotted.three
    ...     print "fail"
    ... except AttributeError:
    ...     pass
    
    Can you print the lookup? Yes (but not shown because
    of Python vs Jython differences in a dict's exact repr).
    >>> int("<DottedLookup" in repr(dotted))
    1

    Can you check membership? Yes:
    >>> int('one' in dotted)
    1
    >>> int('two' in dotted)
    1
    >>> int('three' in dotted)
    0
    
    Can you still use dict-style lookup? Yes.
    >>> dotted['two']
    2
    
    Can you still use dict.get? Yes.
    >>> dotted.get('two')
    2
    >>> dotted.get('nosuchitem')
    >>> dotted.get('nosuchitemwithdefault', 'Yup')
    'Yup'
    """
    def __init__(self, wrapped_dict):
        self.wrapped_dict = wrapped_dict

    def __getattr__(self, attr):
        try:
            return self.wrapped_dict[attr]
        except KeyError:
            raise AttributeError(attr)

    def __contains__(self, attr):
        try:
            val = self.__getattr__(attr)
            return True
        except AttributeError:
            return False

    def __getitem__(self, key):
        return self.wrapped_dict[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
            
    def __repr__(self):
        return "<DottedLookup for %s>" % (self.wrapped_dict)

# remove whitespace and punctuation
WS_PLUS_PUNC = string.whitespace + string.punctuation
NO_SPACE_PUNC_TRANS_TABLE = string.maketrans(string.printable, string.printable)

def noSpace(aString):
    """return a string with whitespace removed"""
    return str(aString.encode('ascii', 'replace')).translate(NO_SPACE_PUNC_TRANS_TABLE, string.whitespace)

def noSpacePunc(aString):
    """return aString with spaces and punctuation removed"""
    return str(aString.encode('ascii', 'replace')).translate(NO_SPACE_PUNC_TRANS_TABLE, WS_PLUS_PUNC)

def string2bool(value, quiet=False):
    """given a string with a boolean-like value, return True or False.
    if 'quiet', will pass back the string as-is (non-empty strings will
    evaluate as True); if not 'quiet', raises ValueError.
    
    for some discussion, see this thread:
        http://mail.python.org/pipermail/python-list/2004-April/thread.html#216418

    and in particular this message for a list of accepted values:
        http://mail.python.org/pipermail/python-list/2004-April/216418.html
    """
    s = str(value).lower()
    if s in BOOL_TRUE:
        return True
    if s in BOOL_FALSE:
        return False
    if quiet:
        return value
    else:
        raise ValueError, "couldn't convert '%s' to a boolean" % value


def string2number(value, quiet=True):
    """convert answer to a number if possible -- try int, then float
    
    if 'quiet', will pass back the value, otherwise raises ValueError
    """
    try:
        # if value comes in as already a number, we don't want to
        # accidentally truncate it to an int
        if int(value) == float(value):
            return int(value)
    except (ValueError, TypeError):
        pass
    try:
        return float(value)
    except (ValueError, TypeError):
        pass
    if quiet:
        return value
    else:
        raise ValueError, "couldn't convert '%s' to a number" % value


def bool2attrib(aBool):
    if aBool:
        return u"true"
    else:
        return u"false"


def filepath2url(fpath, sep=None):
    """convert the filepath 'fpath' to a file:// url and return it.
    Urlquote troublesome characters and handle platform- specific path
    separator characters. (Note: the only difference from
    urllib.pathname2url() is that we prepend the 'file://' scheme.)

    Spaces and tildes are urlquoted:
    >>> filepath2url('~bozo/Documents/my word file.doc')
    'file:%7Ebozo/Documents/my%20word%20file.doc'
    
    Windows backslashes are converted to forward slashes:
    
    # TODO: cannot see how to test this while on a Mac
    #>>> filepath2url('C:\My Files\my word file.doc')
    #'file:///My%20Files/my%20word%20file.doc'
    """
    return 'file:%s' % pathname2url(fpath)


def url2filepath(url, sep=None):
    """convert the file:// url to a local filepath and return it. Unquotes
    urlescaped characters and uses the local file separator. The distinction
    from urllib.url2pathname is we assume a file:// url. If the scheme isn't
    'file', raise ValueError. 'sep' is a the character to use for the file separator.
    If not passed, os.sep is used.

#     Spaces and tildes are unquoted:
#     >>> url2filepath('file:///bozo/Documents/my%20word%20file.doc%7E', sep='/')
#     '/bozo/Documents/my word file.doc~'
#     
#     On Windows, forward slashes are converted to backslashes.
#     >>> backslash = chr(92)
#     >>> url2filepath('file:///bozodocs/Documents/my%20word%20file.doc', sep=backslash)
#     '\\\\bozodocs\\\\Documents\\\\my word file.doc'
# 
#     (Believe it or not, those quad-backslashes actually come out as a
#     single backslash in the result string.)
    
    # next test fails under Jython 2.2's crippled doctest
#     Passing a non-file scheme is not allowed:
#     >>> url2filepath("http://google.com")
#     Traceback (most recent call last):    
#     ...
#     ValueError: only the 'file' scheme is supported, not 'http'
    """
    if sep is None:
        sep = os.sep
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    if scheme != 'file':
        raise ValueError("only the 'file' scheme is supported, not '%s'" % scheme)
    # note: not using os.path.split() and join() because there's no real path
    # arithmetic here, and because those functions don't admit a custom sep
    # character
    return url2pathname(path)
#     path = unquote(path)
#     components = path.split('/')
#     return sep.join(components)
    

# ------------------------------------------------------------

class VariableCollector(object):
    """a variable scanner that recognizes dotted expressions (eg, T0.FruitDailyIntake)
    (unlike the AST-based name collector class above)
    
    The core _scanvars_all() and lookup() methods are copied and modified from the standard
    library cgitb module.
    """
    
    __UNDEF__ = []                          # a special sentinel object
    
    def __init__(self, reader, locals):
        """reader is a callable object which provides the same interface
            as the readline() method of built-in file objects (see the
            documentation for the standard library's tokenize module)
        locals is a dict of variables known to be in the local scope. (Locals,
            if present, will be returned and classified in the output.)
        """
        self.reader = reader
        self.locals = locals

    def lookup(self, name, globals=globals()):
        """Find the value for a given name in the given environment.
        return (location, value) tuple
        
        globals param is deliberately memoized
        """
        if name in self.locals:
            return 'local', self.locals[name]
        if name in globals:
            builtins = self.builtins()
            if name in builtins:
                return 'builtin', builtins[name]
            return 'global', globals[name]
        return None, self.__UNDEF__
        
    def scanvars_all(self):
        """Scan one logical line of Python and look up values of variables used.
        Return a list containing a 3-tuple (name, isUltimate, value) for each variable found.
        
        'isUltimate' is a boolean -- True if the variable is the full expansion of
        a compound (dotted) expression of lookups, eg T0.FruitDailyIntake.
        T0 would also appear in the returned result, but its isUltimate will be False.
        """
        vars, lasttoken, parent, prefix = [], None, None, ''
        # keep track of values (eg, T0) which are just stepping stones
        # to the ones we care about (eg, T0.FruitDailyIntake)
        intermediates = set()
        for ttype, token, start, end, line in tokenize.generate_tokens(self.reader):
            value = None
            if ttype == tokenize.NEWLINE: break
            if ttype == tokenize.NAME and token not in keyword.kwlist:
                if lasttoken == '.':
                    if parent is not self.__UNDEF__:
                        value = getattr(parent, token, self.__UNDEF__)
                        vars.append((prefix + token, value))
                else:
                    where, value = self.lookup(token)
                    vars.append((token, value))
            elif token == '.':
                if last_ttype != tokenize.NAME:
                    # eg, {'key': 'value'}.get(xx) -- the '}' might be the token,
                    # in which case we don't want to think it's actually a name.
                    continue
                # now we know lasttoken is a stepping stone
                intermediates.add(lasttoken)
                prefix += lasttoken + '.'
                parent = value
            else:
                parent, prefix = None, ''
            lasttoken = token
            last_ttype = ttype
        def isUltimate(v):
            return v not in intermediates
        vars = [(token, isUltimate(token), value) for token, value in vars]
        return vars

    ##
    # main client API method
    
    def scanvars(self):
        """return list of 2-tuples (name, value) with builtins and intermediates removed
        
        also apply predicates in filters parameter, if any.
        predicates should take one argument, a 3-tuple (name, isUltimate, value).
        """
        vars = self.scanvars_all()
        return [(name, value) for name, isUltimate, value in vars
                if isUltimate and not self.isBuiltin(name)]
        
    ##
    # utils
    
    def builtins(self):
        return __builtin__.__dict__
        # this one replaced because __builtins__ doesn't exist in Jython 2.2
#         return globals().get('__builtins__', {})

    ##
    # predicates
        
    def isBuiltin(self, name):
        return name in self.builtins()

# ------------------------------------------------------------

class CaseNormalizer(object):
    
    def __init__(self, normalnames):
        self.normalnames = normalnames
        self.lowerindex = dict([(name.lower(), name) for name in self.normalnames])

    def normalize(self, name):
        return self.lowerindex.get(name.lower())

    
# Dictionary utilities ---------------------------------------

class NonNumericValue(object):
    """A wrapper around a value that came from the outside world as an
    inappropriate type. That is, if a value is expected to be a number, as
    defined in an MTS dictionary, but does not coerce appropriately, it is
    wrapped on conversion to be handled more appropriately in error reporting
    later in the pipeline."""
    
    def __init__(self, value, expectedtype):
        self.value = value
        self.expectedtype = expectedtype
    
    # since it's an incorrect value, it's always False in comparisons.
    _fail = lambda self, *args: False
    
    __lt__ = _fail
    __le__ = _fail
    __gt__ = _fail
    __ge__ = _fail
    __ne__ = _fail
    __eq__ = _fail
    __nonzero__ = lambda self: bool(self.value)
    
    __str__ = lambda self: str(self.value)
    __unicode__ = lambda self: unicode(self.value)
    
    def attemptconversion(self):
        return self.expectedtype(self.value)
    

class InvalidDataError(Exception):
    def __init__(self, key, value, type):
        self.key = key
        self.value = value
        self.type = type
    
    def __str__(self):
        return "The value %(value)s cannot be coerced to " \
            "type %(key)s (%(type)s)" % self.__dict__
    

def data_to_dictionary_types(data, dictionary):
    """Given a mapping of characteristic names to values, return a
    mapping of the same, with the values converted, as best as possible,
    to the types defined by the dictionary.
    
    Generally, this is used to convert a bunch of strings to their appropriate
    data types. The processing should conform as follows:
    
    - First, if the characteristic is multivalued, and the data is not a
        non-string sequence, wrap it in a single-item list.
    - If the value is normalized to the appropriate type, or, in the case of
        multivalued characteristics, all of the values are normalized to the
        appropriate type, add it to the return mapping.
    - If the intended type is Numeric, but the value is not, then wrap the
        incoming value in a NonNumericValue object, for later inspection.
    - If the value isn't the empty string (that is, there was some data in it,
        and it wasn't normalized), raise an InvalidDataError.
    """
    newdata = {}
    for key in data:
        cdef = dictionary.char_index.get(key)
        cdeftype = cdef.basetype.pytype
        if cdef is not None:
            val = data[key]
            if isinstance(val, NonNumericValue):
                newdata[key] = val
                continue
            if cdef.is_multivalued and not isList(val):
                if val is None:
                    val = []
                else:
                    val = [val]
            val = cdef.basetype_normalize(val)
            if isinstance(val, (cdeftype, types.NoneType)):
                newdata[key] = val
            elif ( cdef.is_multivalued
                    and all(map(lambda v: isinstance(v, cdeftype), val)) ):
                newdata[key] = val
            elif issubclass(cdef.basetype.pytype, (int, float)):
                newdata[key] = NonNumericValue(val, cdeftype)
            elif val != "":
                raise InvalidDataError(key, val, cdeftype)
    return newdata

# ------------------------------------------------------------

if __name__ == '__main__':
    import sys
    import doctest
    # jython22 has an inconvenient version of doctest
    __main__ = sys.modules['__main__']
    doctest.testmod(__main__)
