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

"""Decorators to allow per-project extensions and customizations.
"""

# decorators and "phone home"

import sys
import itertools
import logging
log = logging.getLogger(__name__)


class ExtensionError(Exception):
    pass


class _Registry(object):
    """simple register-and-record decorator. Doesn't modify function call.
    """

    _extension_names = set([])
    
    def __init__(self):
        # key = public decorator name, val = list of decorated funcs
        log.info(">>>__init__")
        self._registered_funcs = {}
    
    def register(self, key, func):
        log.info("registering extension: '%s': %s" % (key, func))
        self._registered_funcs.setdefault(key, []).append(func)

    def getall(self, key):
        return self._registered_funcs.get(key, [])

    def getone(self, key):
        """If it's set, return the first extension point value for the given
        decorator. Otherwise return None.
        """
        try:
            return self.getall(key)[0]
        except IndexError:
            return None

    def clear(self, key=None):
        """clear all registered functions, or, optionally, all registered
        functions under the given key
        """
        if key is None:
            self._registered_funcs.clear()
        else:
            self._registered_funcs[key] = []
        
    @classmethod
    def decorator(cls, method):
        cls._extension_names.add(method.func_name)
        return method
        
    def decorator_namespace(self):
        return dict((name, getattr(self, name)) for name in self._extension_names)


class Registry(_Registry):
    # use subclass so the decorator works
    # TODO: this is ugly; use metaclass instead

    @_Registry.decorator
    def expose(self, func):
        """Mark the decorated function as available for subject
        generation (ie, for the derived calculations specified in the
        dictionary) and for message generation (ie, logic and
        substitutions in the message docs).
        
        The decorated function needs no special API, and it's not
        modified. It will be called as needed during subject generation
        and/or message generation.
        """
        self.register('expose', func)
        return func

    @_Registry.decorator
    def source(self, func):
        """The decorated function implements a derived data source declared
        in the dictionary.
        
        The original function must be named for the source (eg, a function
        that implements the derived data source SUMMARY must be named
        SUMMARY).
        
        The function takes four arguments:
            - source: a source key
            - running_selection_chars: a subject-shaped dictionary of
                characteristics
            - mtsdict: an MTSDictionary instance
            - evalglobals: a dictionary containing functions and objects
                used for derivation

        The decorated function returns a 3-tuple of (selection_chars,
        message_chars, errors). The two *_chars results are both
        dictionaries of {charname: charvalue} (ie, not nested by
        source). errors is a list of errors encountered in processing.
    
        The function will be called sometime during subject generation; when
        exactly depends on the order of the sources in the MTSDictionary.
        """
        self.register('source', func)
        return func

    @_Registry.decorator
    def toplevel_sources(self, func):
        """The decorated function returns a list of data source names
        (ie, strings) to be hoisted to the top level of the evaluation
        context for subject and message generation.
        
        The function should take one argument, a TailoringRequest instance.

        The function will be called once per creation of a Pipeline
        instance.
        """
        self.register('toplevel_sources', func)
        return func

    @_Registry.decorator
    def make_evaluation_context(self, func):
        """The decorated function returns a dict-like object suitable for
        use as the local variables in a selection/substitution eval() call.
        Typically this would be a util.ChainedDict containing subject characteristics,
        some at the top level (settable here or with toplevel_sources() above),
        some nested with dotted access.
        
        The decorated function is called with three arguments:
            - mtsdict: an MTSDictionary instance
            - evalglobals: a dictionary containing functions and objects to be
                used during evaluation. Suitable for passing to eval() as the
                globals dictionary.
            - treq: a TailoringRequest instance
        """
        self.register('make_evaluation_context', func)
        return func

    @_Registry.decorator
    def custom_project_class(self, func):
        """The decorated function returns a class object which is used
        instead of BasicProject. (It would typically be a subclass of
        BasicProject).
        """
        self.register('custom_project_class', func)
        return func


##
# set up shared registry object and the module-level decorators,
# which phone home to the shared registry.

shared_registry = Registry()
_this_module = sys.modules[__name__]
for decname in Registry._extension_names:
    shared_decorator = getattr(shared_registry, decname)
    _this_module.__dict__[decname] = shared_decorator
del _this_module, decname

__all__ = list(itertools.chain(Registry._extension_names, ['Registry', 'shared_registry']))

#
##
