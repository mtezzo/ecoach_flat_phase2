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

"""A basic implementation of project-delegated functions. The
BasicProject implementation here is intended for use by the Workbench
but can be extended or replaced for custom needs.
"""
import sys
import os
import os.path
import glob
from pprint import pprint
import logging
log = logging.getLogger(__name__)

from tailoring2.common import set
from tailoring2 import config
from tailoring2.dictionary import MTSDictionary
from tailoring2 import subject
from tailoring2 import evaluationcontext
from tailoring2 import extensions
from tailoring2 import util
from tailoring2 import pipeline
from tailoring2 import render
from tailoring2 import runtime


def project_paths(root, dictpath=None,app_customize=None):
    """given a root path to the top level of a project (a path object),
    return a collection of subordinate paths:
        - root
        - messages
        - testcases
        - app_customize
        - dict
        
    Makes a few assumptions about interior component locations.
    
    Each path is an attribute of the returned util.Bunch object. We make
    no assurances about the existence or validity of any of the paths.
    """
    if dictpath is None:
        try:
            dictpath = glob.glob('%s/*.dictionary' % root)[0]
        except IndexError:
            raise IOError("no dictionary file found at project root: %s" % root)
           
    if app_customize is None:       
     	app_customize = os.path.join(root, 'Utilities', 'Tool Support', 'application.py')
     	
    return util.Bunch(root=root, dict=dictpath, app_customize=app_customize,
            messages=os.path.join(root, 'Messages'),
            testcases=os.path.join(root, 'Test Cases'),
            surveys=os.path.join(root , 'Surveys'))

    
# ------------------------------------------------------------

class BasicProject(object):

    def __new__(cls, *args, **kwargs):
        ##
        # install plugins

        def extract_appmodulepath():
            appmodulepath = kwargs.get('appmodulepath')
            if appmodulepath is not None:
                return appmodulepath
            try:
                return args[1]
            except IndexError:
                return None
        appmodulepath = extract_appmodulepath()

        # put appmodulepath's parent onto sys.path so you can import
        # any project-specific modules from appmodule
        if appmodulepath is not None:
            parent_folder = os.path.dirname(os.path.abspath(appmodulepath))
            sys.path.append(parent_folder)
        
        # exec the module, which triggers plugin registration. If there is no
        # appmodule, that's fine -- there just won't be any registered plugins.
        extension_registry = extensions.shared_registry
        appmodule_exec_namespace = extension_registry.decorator_namespace()
        if appmodulepath is not None:
            appmodule_contents = file(appmodulepath, 'rU').read()
            appmodule_code = compile(appmodule_contents, appmodulepath, 'exec')
            exec appmodule_code in appmodule_exec_namespace
        # ok, now the per-project decorated functions should be in extension_registry.

        instance = object.__new__(cls)  # as of Python 2.6, object.__new__ no longer takes *args, **kwargs
        # this namespace needs to stay around now that stuff has been exec-ed in it
        # TODO: verify this -- quick test by replacing with an empty dict yields no
        # additional test failures.
        instance._appmodule_exec_namespace = appmodule_exec_namespace

        # special case: is there a custom make_project() registered?  if so, call
        # it and use the result as our __class__. Otherwise BasicProject will be
        # used.
        custom_project_class = extension_registry.getone('custom_project_class')
        if custom_project_class is not None:
            instance.__class__ = custom_project_class()
            # if we switch the class, __init__() will no longer be called automatically
            # for us, so we do it manually.
            instance.__init__(*args, **kwargs)
        # last created project is blessed
        runtime._project = instance
        return instance

    def __init__(self, mtsdictpath, appmodulepath=None):
        assert os.path.exists(mtsdictpath), mtsdictpath
        self.mtsdictpath = mtsdictpath
        # TODO: may watch file later, for now just grab it once
        self.mtsdict = MTSDictionary.for_file(self.mtsdictpath)
        
        self.appmodulepath = appmodulepath
        if appmodulepath is not None:
            assert os.path.exists(appmodulepath), appmodulepath
            # put appmodule on sys.path so it can import other things
            appmodule_parent = os.path.dirname(self.appmodulepath)
            sys.path.append(appmodule_parent)

        # pull out the registered extensions and apply them to various parts of
        # the project and its subordinates.
        # UPDATE 30 April: using a global registry instead of per-project
        self.extension_registry = extensions.shared_registry  # extensions.Registry()
        
        # TEMP attributes for debugging
        # @expose -> evaluation_globals
        self.ef = exposed_funcs = dict((fn.func_name, fn) for fn in self.extension_registry.getall('expose'))
        self._aen = self._appmodule_exec_namespace  # TEMP alias
        
        # used by both subject factory and pipeline
        self.evaluation_globals = util.ChainedDict([exposed_funcs,
            evaluationcontext.authorutil_exportable_names(),
            globals()]).flatdict()

        # TODO? check registered source extensions -- are they in the dictionary? (should raise?)
        self.custom_source_map = self._extension_index('source')
        self.view_index = self._extension_index('view')

        self.subject_factory = subject.SubjectFactory(self.mtsdict, self.evaluation_globals, self.custom_source_map)
        self.SF = self.subject_factory  # temp alias for delegation

    @classmethod        
    def for_config_file(cls, config_file, project_root=None):
        if project_root is not None:
            assert os.path.exists(project_root), project_root
        myconfig = config.Configuration.from_file(config_file, project_root)
        proj = cls.for_config(myconfig)
        return proj

    @classmethod    
    def for_config(cls, config):
        proj = cls.for_paths(config.projectroot, config.dictionarypath, config.customizationpath)
        proj.config = config
        return proj

    @classmethod
    def for_paths(cls, projectrootpath, dictionarypath, customizationpath):
        log.debug(">>>for_paths()")
        log.debug(locals())
        try:
            proj = cls(dictionarypath, customizationpath)
            log.debug("proj=%s" % proj)
            proj.paths = project_paths(projectrootpath,dictionarypath,customizationpath)
            log.debug("proj.paths=%s" % proj.paths)
            proj.name = os.path.splitext(os.path.basename(dictionarypath))[0]  #.namebase
            log.debug("proj.name=%s" % proj.name)
            return proj
        except Exception, err:
            log.error(err)
            raise

    @classmethod    
    def _for_project_root(cls, project_root, alternate_mtsdict_path=None):
        """given the path to an MTS project (ie, the enclosing folder),
        create and return a tailoring2.BasicProject object. (Make a few
        assumptions about interior component locations.) Optionally supply
        an alternate mtsdict path if you want to use a different main
        dictionary.
        """
        assert os.path.exists(project_root), project_root
        paths = project_paths(project_root)
        if alternate_mtsdict_path is not None:
            paths.dict = alternate_mtsdict_path
        assert os.path.exists(paths.dict), paths.dict
        assert os.path.exists(paths.app_customize), paths.app_customize
        proj = cls(paths.dict, paths.app_customize)
        # add useful additional attributes to project -- might be added to
        # standard tailoring2.project in future
        proj.paths = paths
        proj.name = os.path.splitext(os.path.basename(paths.dict))[0]  #.namebase
        return proj

    @classmethod    
    def for_project_root(cls, project_root, alternate_mtsdict_path=None):
        assert os.path.exists(project_root), project_root
        configpath = os.path.join(project_root, config.DEFAULT_CONFIG_FILE_NAME)
        if not os.path.exists(configpath):
            return cls._for_project_root(project_root,alternate_mtsdict_path)
        return cls.for_config_file(configpath, project_root)

    def _extension_index(self, extkey):
        return dict((fn.func_name, fn) for fn in self.extension_registry.getall(extkey))
        
    def get_eval_factory(self, treq):
        """return the appropriate one-arg function for
        make_evaluation_context. Make selection based on which tailoring2
        extensions have been registered in the project's customization
        module. Default is the quite-liberal hoist_all().
        
        treq is a TailoringRequest object, basically context passed
        along to the eventual evalcontext-creator.
        """
        evalglobals = self.evaluation_globals
        all_source_names = [source.name for source in self.mtsdict.sources]
    
        make_eval_context = self.extension_registry.getone('make_evaluation_context')
        if make_eval_context is not None:
            log.debug("using custom make_evaluation_context()")
            return make_eval_context(self.mtsdict, evalglobals, treq)
    
        toplevel_sources = self.extension_registry.getone('toplevel_sources')
        if toplevel_sources is not None:
            log.debug("using custom top_level_sources()")
            return evaluationcontext.hoist_some(toplevel_sources(treq), all_source_names, evalglobals)            
        
        if 'default_source' in treq:
            return evaluationcontext.hoist_some([treq.default_source], all_source_names, evalglobals)
            
        # note that treq is dropped for hoist_all()
        return evaluationcontext.hoist_all(all_source_names, evalglobals)
    
    def get_render_transforms(self):
        return render.BasicTransformList(render.SurveyCommandTranslator().translate)
        
    def getpipeline(self, message, subject, treq=None, render_transforms=None):
        render_transforms = render_transforms or self.get_render_transforms()
        return pipeline.Pipeline(message, subject, self.get_eval_factory(treq),
            render_transforms=render_transforms)

    ##
    # follows here lots of delegation to the subject factory for methods that
    # used to be implemented in the project itself. Eventually some or most of
    # these methods will be removed, leaving just a high-level API.
    
    def subject_for_primary_chars(self, primary_chars):
        return self.SF.subject_for_primary_chars(primary_chars)

    def getsubject(self, url):
        return self.SF.getsubject(url)

    def default_chars(self):
        return self.SF.default_chars

    def get_primary_chars(self, url):
        return self.SF.get_primary_chars(url)
