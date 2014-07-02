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

"""Load a subject from a JSON file path; apply derived calculations and
substitutions according to the MTS Dictionary.
"""

import sys
import os
import os.path
import optparse
import fileinput
import urlparse
from urllib import quote
import functools
import copy
import logging
log = logging.getLogger(__name__)

# tailoring machinery setup
from tailoring2.common import set, DeriveError, json
from tailoring2.translations import GetTextContexts, pgettext_lazy
from tailoring2 import evaluationcontext
from tailoring2 import util
from tailoring2 import extensions


class Subject(object):
    def __init__(self, data_sources=None, primary_chars=None, selection_chars=None, message_chars=None):
        self.data_sources = data_sources or []
        self.primary_chars = primary_chars or {}
        if selection_chars is None:
            selection_chars = self.primary_chars.copy()
        self.selection_chars = selection_chars        
        if message_chars is None:
            message_chars = selection_chars.copy()
        self.message_chars = message_chars

    # note that the following initializer methods are NOT data-source aware, so
    # your sources have to be!

    def forpath(cls, subjectpath):
        """subjectpath is a file to an exec-able Python file. Exec the file and return the
        resulting Subject class (selection_chars and message_chars will be equal)
        """
        assert os.path.exists(subjectpath), subjectpath
        basic_chars = util.execmodule(subjectpath)
        return cls(primary_chars=basic_chars)
    forpath = classmethod(forpath)
    
    def forstring(cls, subjectstring):
        """subjectstring is a string containing Python source code. Exec
        the string and return the resulting Subject class
        (selection_chars and message_chars will be equal)
        """
        basic_chars = {}
        exec subjectstring in globals(), basic_chars
        return cls(primary_chars=basic_chars)
    forstring = classmethod(forstring)

    def forfile(cls, fileobj):
        """given a file-like object containing Python source code, read and exec it
        and return the resulting Subject
        """
        return cls.forstring(fileobj.read())
    forfile = classmethod(forfile)


# ------------------------------------------------------------
# subject factory -- migrated from project.py

# each scheme handler implements a getreadable(url) method that
# returns a file-like object given a url. (The url must be appropriate
# for their particular scheme -- it's the caller's responsibility to make
# sure that's true.

class FileSchemeHandler:
    def getreadable(self, url):
        """given a file url, return an open file object"""
        return open(util.url2filepath(url), 'rb')

# TODO: HTTPSchemeHandler, MySQLSchemeHandler, etc.

class SchemeLookupError(Exception):
    pass
    
# a data handler is given a file-like object with a read() method (eg, an
# open file, a urlopen object, etc) and returns a dict containing primary
# characteristic data

class JSONDataHandler:
    def parse(self, fileobj):
        return json.loads(fileobj.read())

# TODO: Python source handler, mysql-row handler, etc.

class DataHandlerLookupError(Exception):
    pass


class SubjectFactory(object):
    
    def __init__(self, mtsdict, evaluation_globals=None, custom_source_map=None):
        """mtsdict is an MTSDictionary instance
        evaluation_globals is a dictionary used when eval-ing the derived
            characteristic expressions. It would typically contain any library
            functions to be used, whether from a project-specific plugin
            module or from tailoring2.authorutil. If not provided,
            globals() will be used.
        custom_source_map is a dictionary of {sourcename: <sourcefunc>},
            where sourcefunc implements the indicated data source. sourcefunc
            takes four arguments:
                source (a name or a datasource object? -- TODO)
                running_selection_chars (a dictionary that will be updated)
                mtsdict
                evalglobals
        """        
        # set up url handling strategies
        self._scheme_handlers = {'file': FileSchemeHandler()}
        self._scheme_handlers.update(self.update_scheme_handlers())
        
        json_handler = JSONDataHandler()
        self._data_handlers = {'json': json_handler, 'testcase': json_handler}
        self._data_handlers.update(self.update_data_handlers())
        
        self.mtsdict = mtsdict
        self.evaluation_globals = evaluation_globals or globals().copy()
        self.default_chars = self.mtsdict.default_chars()
        if custom_source_map is None:
            custom_source_map = {}
        self.custom_source_map = custom_source_map
    
    def update_scheme_handlers(self):
        """return a dict of {schemename: handler-obj}. Subclasses should
        override this to handle custom schemes
        """
        return {}

    def update_data_handlers(self):
        """return a dict of {dataextension: handler-obj}. Subclasses should
        override this to handle custom data types
        """
        return {}

    def char_dict_is_flat(self, chardict):
        # if any of the top-level *values* are dicts, assume char dict isn't flat
        isflat = True
        for val in chardict.values():
            if util.isDict(val):
                return False
        # in addition to the declared sources, allow for one undeclared source,
        # the empty string
        num_mtsdict_sources = len(self.mtsdict.sources) + 1
        # (almost?) certainly already a flat dict
        return len(chardict) > num_mtsdict_sources
        
    def get_primary_chars(self, url):
        """return a dict of primary chars
        """
        assert url is not None, url
        scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
        try:
            scheme_handler = self._scheme_handlers[scheme.lower()]
        except KeyError, err:
            raise SchemeLookupError("scheme '%s' unknown" % scheme)
        try:
            extension = os.path.splitext(path)[1][1:]  # json, py, testcase, etc
            data_handler = self._data_handlers[extension.lower()]
        except AttributeError, err:
            # path is None
            raise DataHandlerLookupError("no subject path provided")
        except IndexError, err:
            # no extension in path
            raise DataHandlerLookupError("file type unknown for '%s' (no extension provided)" % path)
        except KeyError, err:
            # unknown data handler
            raise DataHandlerLookupError("no handler for '%s' type" % extension)
        file_like_obj = scheme_handler.getreadable(url)
        allchars = data_handler.parse(file_like_obj)
        
        # XXX- sometimes the characteristics are nested, sometimes not. This whole
        # business is pretty ugly.
        if self.char_dict_is_flat(allchars):
            log.warn("original dict in %s is flat, adding dummy empty-string source" % url)
            return {'': allchars}
        return allchars

    def blank_primary_chars(self):
        """return a dictionary of blank characteristics arranged so the
        nesting matches the dictionary's sources
        """
        blank_primary_chars = {}
        sources = self.mtsdict.sources or ['']
        for source in sources:
            blank_primary_chars[source] = {}
        return blank_primary_chars
    
    def getsubject(self, url):
        """returns a tuple containing a Subject object and a list of errors
        encountered in subject generation
        """
        primary_chars = self.get_primary_chars(url)
        return self.subject_for_primary_chars(primary_chars)
        
    def getsubject_for_primary_chars(self, primary_chars):
        return self.subject_for_primary_chars(primary_chars)

    def subject_for_primary_chars(self, primary_chars):
        # changes from base class:
        # - call construct_source_chars in the loop
        # - dispatch to custom source implementation where necessary (set up chained dict?)
        # - 
        log.debug(">>>subject_for_primary_chars")
        log.debug("incoming primary_chars: %s" % primary_chars)
        if not primary_chars:
            primary_chars = {}
            for src in self.mtsdict.sources:
                primary_chars[src.name] = {}
            
        all_errors = []
        selection_chars = {}
        message_chars = {}
        for src in self.mtsdict.sources:
            selection_chars[src.name] = primary_chars.get(src.name, {}).copy()
            message_chars[src.name] = {}
        
        for source in self.mtsdict.sources:
            log.debug("generating chars for %s" % source)
            log.debug("pre sourcemaker() call, selection_chars[%s] = %s" % (source.name, selection_chars[source.name]))

            # check for custom source extensions
            # TODO- refactor if/else into function map
            custom_source_impl = self.custom_source_map.get(source.name)
            if custom_source_impl:
                sel_slice, msg_slice, errs = custom_source_impl(source.name, selection_chars, self.mtsdict, self.evaluation_globals)
                selection_chars[source.name].update(sel_slice)
            else:
                pre_result, errs = self.pre_derived_custom(source, self.evaluation_globals, selection_chars)
                selection_chars[source.name].update(pre_result)

                dphase = DerivePhase('main', self.mtsdict, source, self.evaluation_globals)
                main_result, main_errs = dphase.run(selection_chars)
                errs.extend(main_errs)
                selection_chars[source.name].update(main_result)
                
                post_result, post_errors = self.post_derived_custom(source, self.evaluation_globals, selection_chars)
                errs.extend(post_errors)
                selection_chars[source.name].update(post_result)
                
                sel_slice = util.dictmerge(pre_result, main_result, post_result)

            all_errors.extend(errs)
            text_subs, text_sub_errors = self.mtsdict.textsubs(sel_slice)
            text_subs = self.i18n_message_chars(text_subs)
            message_chars[source.name] = util.dictmerge(text_subs, selection_chars[source.name])
            all_errors.extend(text_sub_errors)
        
        # using names instead of source objects because a bunch of downstream stuff
        # expects it. Would be nice to use the objects eventually.
        sourcenames = [src.name for src in self.mtsdict.sources]
        mysubject = Subject(data_sources=sourcenames,
            primary_chars=primary_chars,
            selection_chars=selection_chars,
            message_chars=message_chars)
        return (mysubject, all_errors)
            
    def pre_derived_custom(self, source, evalglobals, allchars):
        """do any necessary project-specific customization and return a
        (dictionary, errors) tuple of new characteristics to be included
        in the evaluation. This method is called _before_ the derived
        characteristics are calculated. The default implementation
        returns an empty dict and an empty error list. Projects should
        override and implement as necessary.
        """
        return ({}, [])

    def post_derived_custom(self, source, evalglobals, allchars):
        """do any necessary project-specific customization and return a
        (dictionary, errors) tuple of new characteristics to be included
        in the evaluation. This method is called _after_ the derived
        characteristics are calculated. The default implementation
        returns an empty dict and an empty error list. Projects should
        override and implement as necessary.
        """
        return ({}, [])
    
    def i18n_char_val(self, cdef, val):
        rset_name = cdef.restrictionset.name
        context_name = '|'.join([GetTextContexts.SUBSTITUTION_TEXT, rset_name])
        if cdef.is_multivalued:
            return [pgettext_lazy(context_name, v) for v in val]
        return pgettext_lazy(context_name, val)
    
    def i18n_message_chars(self, chars):
        new_chars = {}
        for charname, val in chars.items():
            cdef = self.mtsdict.char_index.get(charname)
            if cdef is not None:
                new_chars[charname] = self.i18n_char_val(cdef, val)
            else:
                new_chars[charname] = val
        return new_chars
    

# ------------------------------------------------------------

class DerivePhase(object):

    def __init__(self, name, mtsdict, source, evalglobals):
        self.name = name
        self.mtsdict = mtsdict
        self.source = source
        self.evalglobals = evalglobals
        self.primary_defaults = self.mtsdict.primary_defaults

    def run(self, allchars, othercontext=None):
        running_result = {}  # will become sel_slice aka first return value
        errors = []
        
        # defaults need to be applied source by source.
        # nested dict of {sourcename: ChainedDict([allchars[src]+primary_defaults[src]])}
        primary_plus = util.nested_chained_dict([allchars, self.primary_defaults])
        dotted_lookups = dict([(src.name, util.DottedLookup(primary_plus[src.name]))
            for src in self.mtsdict.sources if src is not self.source])

        # include live attachment to current source
        assert self.source.name not in dotted_lookups
        current_source_snapshot = util.ChainedDict([primary_plus[self.source.name], running_result], name='current_source_snapshot')
        dotted_lookups[self.source.name] = primary_plus[self.source.name] = util.DottedLookup(current_source_snapshot)
        
        magic_vars = {'__source__': self.source}
        magic_vars.update(othercontext or {})
        # TODO- more sophisticated hoisting? replicate pipeline's hoisting if possible
        hoisted_main_source = primary_plus[self.source.name]
        evalcontext = util.ChainedDict([running_result, hoisted_main_source,
            dotted_lookups, primary_plus, magic_vars],
            name="evalcontext")
        
        derived_chars_in_source = [cdef for cdef in self.mtsdict.derived_chars_topo
            if self.source.name in cdef.sources]
        log.debug("derived_chars_in_source: %s" % derived_chars_in_source)
        for chardef in derived_chars_in_source:
            name = chardef.name
            if name in evalcontext:
                val = evalcontext[name]
                log.info("a value for the derived char '%s' is already present (%s): copying" % (name, repr(val)))
                # TODO: add override warning here?
                # ...
                running_result[name] = val
                continue

            log.info('deriving %s: %s' % (name, chardef.derivedcalc.expression_string))
            try:
                running_result[name] = chardef.derive(self.evalglobals, evalcontext)
            except Exception, err:
                log.warn('error in %s: %s' % (name, err))
                errors.append(DeriveError(err, chardef, self.source, self))
                log.debug('using default for %s: %s' % (name, chardef.default))
                running_result[name] = chardef.default

        sel_slice = current_source_snapshot.flatdict()
        log.debug("<<<%s(%s): result=%s, errors=%s" % (self.name, self.source, sel_slice, errors))
        return (sel_slice, errors)
        
# ------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
