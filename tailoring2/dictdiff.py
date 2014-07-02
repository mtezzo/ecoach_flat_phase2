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

"""Enumerate the differences between two dictionaries.
"""
        
# stand-in for a missing value -- can't use None, since that might already
# be in the dictionary under inspection
class __MISSING_CLS(object):
    def __repr__(self):
        return "<MISSING>"

MISSING = __MISSING_CLS()


def dictdiff(dict1, dict2):
    """Given two dictionaries, return a list of 3-tuples:
    (key, dict1-value, dict2-value) for each key on which the
    dictionaries differ. The list is unsorted but a simple call to 
    sort() or sorted() will sort by key.
    
    If is key is missing from one dictionary, that value will be
    represented in the tuple with the MISSING object defined in this
    module.
    
    >>> len(dictdiff({}, {}))
    0
    >>> dictdiff(dict(a=1), {})
    [('a', 1, <MISSING>)]
    >>> dictdiff(dict(a=1, b=2), dict(a=1))
    [('b', 2, <MISSING>)]
    >>> dictdiff(dict(a=1, b=2), dict(a=1, b=3))
    [('b', 2, 3)]
    >>> sorted(dictdiff(dict(a=None), dict(b=None)))
    [('a', None, <MISSING>), ('b', <MISSING>, None)]
    >>> dictdiff(dict(a=None), {})
    [('a', None, <MISSING>)]
    >>> sorted(dictdiff(dict(z=26, y=25), dict(a=1, b=2)))
    [('a', <MISSING>, 1), ('b', <MISSING>, 2), ('y', 25, <MISSING>), ('z', 26, <MISSING>)]
    """
    allkeys = set(dict1).union(dict2)
    valcomps = [(key, dict1.get(key, MISSING), dict2.get(key, MISSING))
            for key in allkeys]
    diffs = [(key, lhs, rhs) for key, lhs, rhs in valcomps if not lhs == rhs]
    return diffs

# ------------------------------------------------------------
# fill in some missing names for running the doctests under Jython

try:
    set
except NameError:
    from sets import Set as set

try:
    sorted
except NameError:
    def sorted(lst):
        listcopy = lst[:]
        listcopy.sort()
        return listcopy

# ------------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod()
