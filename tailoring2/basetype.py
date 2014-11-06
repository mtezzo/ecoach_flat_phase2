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

"""Represents a possible type for characteristic values. Typically a
primitive type like string, int, etc. Wraps an actual python type.

Broke out the Basetype object from dictionary.py.
"""

import tokenize
from cStringIO import StringIO
import logging
log = logging.getLogger(__name__)

from tailoring2.common import set
from tailoring2 import util

# ------------------------------------------------------------

class Basetype(object):
    """Represents a possible type for characteristic values. Typically a primitive type
    like string, int, etc. Wraps an actual python type.
    
    ivars:
    - name: short name for the basetype, like string or int
    - default: the value to assign if there's no default provided by
        the CharacteristicDefinition object that uses this basetype
    - default_string: the default as it came in originally, before being
        converted to python
    - description: the non-tech description of the basetype
    - pytype: the python type best resembling this basetype
    - isinstance_func: decide whether a given value is of this basetype
    """
    # list of standard basetype instances, populated in __init__()
    _known_types = []

    # dict of {name: basetype instance}
    _lookup_by_name = {}
    
    def __init__(self, name, default, description, pytype, isinstance):
        log.debug(">>>Basetype.__init__(%s, %s, %s)" % (name, pytype, id(self)))
        self.name = name
        self.description = description
        if pytype is None:
            pytype = self.string2pytype(name)
        self.pytype = pytype
        self.default = self.pytype(default)  # convert to its native type
        self.default_string = default
        self.isinstance = isinstance
        self._known_types.append(self)
        self._lookup_by_name[name] = self

    def __repr__(self):
        return "<Basetype %s (python %s) (%s)>" % (self.name, self.pytype, id(self))

    @classmethod
    def string2basetype(cls, typename):
        """given a string, return the basetype instance. Raise TypeError if unknown."""
        try:
            return cls._lookup_by_name[typename]
        except KeyError, err:
            raise TypeError("unknown dictionary type '%s'" % typename)
        
    @classmethod
    def string2pytype(cls, typename):
        """given a string, return the pytype"""
        return cls.string2basetype(typename.strip()).pytype

    @classmethod
    def for_element(self, elem):
        name = elem.get('name')
        assert name is not None
        default = elem.get('default', '')  # default default is the empty string
        description = elem.text
        assert description is not None

        # TODO: an extension mechanism for arbitrary new types would have to be
        # implemented here, wrapping the above lookup in try/except
        # ...
        try:
            return self.string2basetype(name)
        except TypeError, err:
            raise
    
    @classmethod
    def adapt(cls, item):
        """return a Basetype instance adapted to the parameter 'item'"""
        # fits with an existing basetype?
        for basetype in cls._known_types:
            if basetype.isinstance(item):
                return basetype
        # ok, we do need a new type after all
        return cls.synthesize(item)
        
    @classmethod
    def synthesize(cls, proto):
        """return a Basetype created from the object instance 'proto'"""
        newtype = cls.__new__(cls)
        newtype.name = '<synthesized>'
        newtype.description = '<synthesized for %s>' % repr(proto)
        newtype.pytype = type(proto)
        newtype.default = proto
        newtype.default_string = repr(proto)
        return newtype
    
# ------------------------------------------------------------

def is_basestring(val):
    return isinstance(val, basestring)


def is_int_long(val):
    if val is True or val is False:
        return False
    return isinstance(val, int) or isinstance(val, long)

# ------------------------------------------------------------
# define instances

StringBasetype = Basetype(name='string', default='',
    description='String', pytype=unicode, isinstance=is_basestring)

# since the trend in Python is to integrate int and long (in Python 3 they're all longs),
# we just start with longs.
IntBasetype = Basetype(name='int', default=-1,
    # issue 4408, 9/18/09: when pytype=long (as it was until this change),
    # through a cascade of other issues including Jython's treatment of
    # BigIntegers, comparisons with defaulted values weren't working right.
    # For instance, if BrGoalSet was defaulted to -1, the expression
    # BrGoalSet > 1 would evaluate to True! (This is because BrGoalSet came
    # in as a PyLong, which was implemented in Java as a BigInteger, which
    # does not implement all the usual numerical comparisons, which led
    # to an error condition, which led to a default object being returned,
    # which was interpreted as boolean True. Anyway, there's some stuff
    # in Jython 2.5 that probably needs to be fixed, and this is the workaround
    # until that's done.)
    #
    # FIXME: set this back to pytype=long once the underlying
    # Jython/PyLong/BigInteger numerical comparisons are worked out
    description = 'Number (no decimal)', pytype=int, isinstance=is_int_long)

DecimalBasetype = Basetype(name='decimal', default=-99.9,
    description='Number (with decimal)', pytype=float,
    isinstance = lambda v: isinstance(v, float) or IntBasetype.isinstance(v))

# unfortunately Jython doesn't support datetime natively yet (as of v2.2)
# so we fake it with strings
#
# TODO: the current release of Jython, v2.5, does support datetimes, so
# this code can be updated.
DatetimeBasetype = Basetype(name='datetime', default='1904-01-01 00:00:00T-0500',
    description='Date (YYYY-MM-DD hh:mm)', pytype=unicode, isinstance=is_basestring)

STANDARD_BASETYPES = [StringBasetype, IntBasetype, DecimalBasetype, DatetimeBasetype]
