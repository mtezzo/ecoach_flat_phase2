# COPYRIGHT (c) 2010
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

"""Utilities for using smart python objects in a subject as opposed to
the usual primitive values (string, int, float, etc). Helpful with, for
example, pronoun substitution.
"""

# ------------------------------------------------------------
# pronoun substitution and possessives

class _Gender(object):

    _nameindex = {}
    _codeindex = {}
    
    def __init__(self, name, **attrs):
        """The name argument is indexed in the class for later lookups.
        The attrs are assigned to instance variables.
        """
        self.name = name
        self.code = name[0].lower()
        self._nameindex[name] = self
        self._codeindex[self.code] = self
        for attrkey, val in attrs.items():
            setattr(self, attrkey, val)
    
    def __repr__(self):
        return "<Gender: %s>" % self.name

    def __str__(self):
        return self.name

    @classmethod
    def forstring(cls, s):
        try:
            nameindex = cls._codeindex if len(s) == 1 else cls._nameindex
        except TypeError:
            raise ValueError(s)
        try:
            return nameindex[s.lower()]
        except KeyError, err:
            raise ValueError("no Gender matches %s" % s)


class Gender(object):
    # this class is mostly a namespace -- the action happens in _Gender

    @classmethod
    def forstring(cls, name):
        return _Gender.forstring(name)
        
    MALE = _Gender('male', heshe='he', hisher='his', himher='him', himselfherself='himself',
        manwoman='man', boygirl='boy',menwomen='men')

    FEMALE = _Gender('female', heshe='she', hisher='her', himher='her', himselfherself='herself',
        manwoman='woman', boygirl='girl',menwomen='women')
        
    MALE.opposite, FEMALE.opposite = FEMALE, MALE

    # TODO: 'neuter', 'unknown' (and others?)

    @classmethod
    def picker_for(cls, prop):
        """return a function that takes one argument, a gender string, and
        returns the named property on the characteristics.Gender object
        """
        def _gpicker(genderstring):
            return getattr(cls.forstring(genderstring), prop)
        return _gpicker
    
# ------------------------------------------------------------

class Noun(object):
    """for now, a Noun can be used to calculate a possessive. We might
    add other stuff down the road.
    """
    
    def __init__(self, name):
        self.name = name

    @classmethod
    def forstring(cls, nountype):
        subclass_index = dict([(scls.__name__.lower(), scls) for scls in cls.__subclasses__()])
        lookupname = (nountype+'noun').lower()
        try:
            return subclass_index[lookupname]
        except KeyError:
            raise ValueError("noun type '%s' is unknown" % nountype)


class SingularNoun(Noun):
    def possessive(self, apos_char="'"):
        if self.name.lower().endswith('s'):
            template = "%s%s"
        else:
            template = "%s%ss"
        return template % (self.name, apos_char)


