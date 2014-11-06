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

"""Create the dictionary-like contexts that the selection and
substitution modules use while processing.
"""

import sys
import itertools
import __builtin__
import types

from tailoring2 import util
from tailoring2 import authorutil

# ------------------------------------------------------------

# memoize
_authorutil_exportable_names = None

# ------------------------------------------------------------

def keep_module_item(name, val):
    """predicate for screening items that might be in an imported module.
    Omits builtins, private names, and modules.

    Short alias for tests:    
    >>> kmi = keep_module_item
    
    Ordinary characteristic names are retained:
    >>> int(kmi('FirstName', 'Waldo'))
    1
    
    Builtins are omitted:
    >>> int(kmi('dict', dict))
    0
    
    Single-underscore names are retained:
    >>> int(kmi('_FirstName', 'Waldo'))
    1
    
    Double-underscore names are omitted:
    >>> int(kmi('__FirstName', 'Waldo'))
    0
    
    Modules and packages, both stdlib and non-stdlib, are retained
    *before* they've been imported but not after:
    >>> int(kmi('quopri', ''))
    1
    >>> import quopri  # this is a deliberately obscure stdlib module
    >>> int(kmi('quopri', ''))
    0
    >>> int(kmi('tailoring2', ''))
    0
    """
    return not (name in __builtin__.__dict__ or
            name.startswith('__') or
            name in sys.modules or
            isinstance(val, types.ModuleType))


def authorutil_exportable_names():
    """return a dict of the names from the authorutil module that we
    want to export for message generation.
    
    >>> names = authorutil_exportable_names()

    The names contain functions that are defined in authorutil:
    >>> int('isEmpty' in authorutil.__dict__)
    1
    >>> int('isEmpty' in names)
    1

    But not the modules that authorutil imports:
    >>> int('re' in authorutil.__dict__)
    1
    >>> int('re' in names)
    0
    >>> int('util' in authorutil.__dict__)
    1
    >>> int('util' in names)
    0

    The exported names also omit anything that starts with a double underscore.
    >>> int('__name__' in authorutil.__dict__)
    1
    >>> int('__name__' in names)
    0
    >>> int('__file__' in authorutil.__dict__)
    1
    >>> int('__file__' in names)
    0
    
    The dict is only calculated once.
    """
    global _authorutil_exportable_names
    if not _authorutil_exportable_names:
        _authorutil_exportable_names = dict([(name, val)
                for name, val in authorutil.__dict__.items() if keep_module_item(name, val)])
    return _authorutil_exportable_names

# ------------------------------------------------------------

def flat_evaluation_context(allchars):
    """return a ChainedDict arranged for engine execution. Unlike nested_evaluation_context,
    this function assumes that allchars is a flat namespace with no data sources.
    
    @param allchars: a dictionary containing subject characteristics. The characteristics
        are available at the top level of the dictionary; that is, there are assumed to be
        no data sources involved, and no hoisting or dotted access insertions will be done.

    The passed in dictionary has no knowledge of the authorutil functions:
    >>> chars = dict(FirstName="Waldo")
    >>> int('isEmpty' in chars)
    0
    
    The returned evaluation context does know about authorutil:
    >>> context = flat_evaluation_context(chars)
    >>> int('isEmpty' in context)
    1
    
    But the original dictionary still doesn't know:
    >>> int('isEmpty' in chars)
    0
    """        
    return util.ChainedDict([allchars, authorutil_exportable_names()])


def nested_evaluation_context(toplevel_source, data_sources, allchars, appfunctions=None):
    """return a ChainedDict arranged for engine execution. The sub-dictionary
    referred to by toplevel_source becomes available at the top level of
    the returned dictionary. All the subdictionaries referred to by data_sources
    become available through dotted access: eg, T0.FirstName.
    
    @param toplevel_source: a string present as a key in allchars; the key
        should resolve to a dictionary.
    @param data_sources: a list of strings representing data sources such 
        as the one in toplevel_source (T0, T1, etc.). (toplevel_source should
        be one of the members of data_sources.)
    @param allchars: a dictionary containing subject characteristics. The top-level
        keys are codes representing data sources (T0, T1, etc.). The values under
        those keys are dictionaries of subject characteristics (FirstName=Waldo, etc.).
    @param appfunctions: a dictionary containing any custom functions that should
        be part of the evaluation context

    Basic usage:        
    >>> flatchars = dict(T0=dict(FirstName="Waldo"))
    >>> ctx = nested_evaluation_context('T0', ['T0'], flatchars)
    >>> ctx['FirstName']
    'Waldo'
    >>> ctx['T0'].FirstName
    'Waldo'

    In an eval(), you can use simple dot syntax to get at the values:
    >>> eval('FirstName', {}, ctx)
    'Waldo'
    >>> eval('T0.FirstName', {}, ctx)
    'Waldo'

    Missing names become errors of different types depending on how they're
    called. A missing top-level attribute is a KeyError when called dictionary-style:
    >>> try: ctx['NoSuchAttribute']; print 'fail'
    ... except KeyError: pass
    
    But inside eval() it's a NameError:
    >>> try: eval('NoSuchAttribute', {}, ctx); print 'fail'
    ... except NameError: pass
    
    Dict access to a nested attribute is a KeyError:
    >>> try: ctx['T0.NoSuchAttribute']; print 'fail'
    ... except KeyError: pass
    
    But a missing attribute on a known top-level data source is an AttributeError:
    >>> try: ctx['T0'].NoSuchAttribute; print 'fail'
    ... except AttributeError: pass
    >>> try: eval('T0.NoSuchAttribute', {}, ctx); print 'fail'
    ... except AttributeError: pass
    
    Adding an app function to the eval context makes it available:
    >>> appfuncs = dict(summish=sum)
    >>> ctxplus = nested_evaluation_context('T0', ['T0'], flatchars, appfunctions=appfuncs)
    >>> eval('sum((1, 2, 3))', {}, ctxplus)
    6
    >>> eval('summish((1, 2, 3))', {}, ctxplus)
    6
    >>> try: eval('summish((1, 2, 3))', {}, ctx)
    ... except NameError: pass
    """
    toplevel_chars = allchars[toplevel_source]
    dotted_lookups = [(source, util.DottedLookup(allchars[source])) for source in data_sources]
    dotted_lookups = dict(dotted_lookups)
    searchlist = [dotted_lookups, toplevel_chars]
    if appfunctions is not None:
        searchlist.append(appfunctions)
    searchlist.extend([authorutil_exportable_names(), allchars])
    return util.ChainedDict(searchlist)

# ------------------------------------------------------------


def hoist_some(toplevel_sources, all_sources, evalglobals):
    """return an eval-context factory function that hoists the
    characteristics under certain data sources to the top level. The
    returned function is a one-arg function that itself returns a
    mapping object suitable for use as the 'locals' argument to eval().
    
    toplevel_sources is an iterable of strings -- data source keys
    all_sources is a list of data source keys
    evalglobals is a dictionary (pydict) of function and variable names
        to use in eval() (note: evalglobals need not include the subject
        characteristics -- they are passed in later)
    """
    def make_eval(allchars):
        """return a dict-like object (a ChainedDict) suitable for use as
        the locals mapping in eval(). allchars is a subject-shaped
        nested dictionary of sources to characteristic dicts.
        """
        dotted_lookups = dict([(source, util.DottedLookup(allchars[source])) for source in all_sources])
        toplevel_chars = util.ChainedDict([allchars[src] for src in toplevel_sources]).flatdict()
        searchlist = [dotted_lookups, toplevel_chars, evalglobals, allchars]
        return util.ChainedDict(searchlist)
    return make_eval
    
    
def hoist_all(all_sources, evalglobals):
    """return an eval-context factory function that hoists all the
    characteristics in the subject, regardless of data source, to the
    top level. The returned function is a one-arg function that itself
    returns a mapping object suitable for use as the 'locals' argument
    to eval().
    
    hoist_all() is very handy for small projects but should be
    customized for any larger project that collects data under the same
    name but at different time points. (For example, a weekly checkin
    question.)

    all_sources is a list of data source keys
    evalglobals is a dictionary (pydict) of function and variable names
        to use in eval() (note: evalglobals need not include the subject
        characteristics -- they are passed in later)
    """
    return hoist_some(all_sources, all_sources, evalglobals)


# ------------------------------------------------------------

if __name__ == '__main__':
    import sys
    import doctest
    # jython22 has an inconvenient version of doctest
    __main__ = sys.modules['__main__']
    doctest.testmod(__main__)
