import os
import logging

from tailoring2.documents import SurveyDocument
from tailoring2.project import BasicProject
from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

_project = None
_projectroot = None
_subjectloader = None

logger = logging.getLogger(__name__)

def _get_loader_class(import_path):
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a subject loader module." % import_path)
    module, classname = import_path[:dot], import_path[dot+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing subject loader module %s: "%s"' % (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Subject loader module "%s" does not define a "%s" class.' % (module, classname))



def _initproject():
    global _project
    logger.info('Loading tailoring2 project.')
    project_root = getprojectroot()
    if not project_root:
        logger.critical('TAILORING2_PROJECT_ROOT is not configured.')
    config_file = getattr(settings, 'TAILORING2_PROJECT_CONFIG', None)
    dict_file = getattr(settings, 'TAILORING2_DICTIONARY', None)
    customization_file = getattr(settings, 'TAILORING2_CUSTOMIZATION_MODULE',
        None)
    
    if config_file:
        config_file = absify(config_file, project_root)
        logger.debug('Using config file at: %s',  config_file)
        _project = BasicProject.for_config_file(config_file, project_root)
    elif dict_file and customization_file:
        dict_file = absify(dict_file, project_root)
        customization_file = absify(customization_file, project_root)
        logger.debug('Using dictionary: %s and customisation module: %s',
            dict_file, customization_file)
        _project = BasicProject.for_paths(project_root, dict_file,
            customization_file)
    else:
        logger.debug('Using project rooted at: %s.', project_root)
        _project = BasicProject.for_project_root(project_root)
    logger.info('Finished loading tailoring2 project.')

def _initsubjectloader():
    global _subjectloader
    logger.info('Caching tailoring2 subject loader.')
    project = getproject()
    subjectloader_classname = getattr(settings,
        'TAILORING2_SUBJECT_LOADER_CLASS', None)
    if subjectloader_classname is None:
        logger.debug('Using default subject loader class.')
        subjectloader_classname = 'djangotailoring.subjects.SerializedSubjectLoader'
    logger.debug('Using subject loader class: %s.', subjectloader_classname)
    subjectloader_class = _get_loader_class(subjectloader_classname)
    subjectloader_class.project = project
    _subjectloader = subjectloader_class
    logger.info('Finished caching tailoring2 subject loader.')

def getproject():
    if _project is None:
        _initproject()
    return _project

def setproject(project):
    global _project
    _project = project

def getprojectroot():
    if _project is not None:
        try:
            return _project.paths.root
        except AttributeError:
            pass
    if _projectroot is not None:
        return _projectroot
    return getattr(settings, 'TAILORING2_PROJECT_ROOT', None)

def setprojectroot(projectroot):
    global _projectroot
    _projectroot = projectroot
    if _project is not None:
        getproject()


def getsubjectloader():
    if _subjectloader is None:
        _initsubjectloader()
    return _subjectloader

def absify(path, root):
    return path if os.path.isabs(path) else os.path.join(root, path)

def project_document_path(path):
    return absify(path, getprojectroot())

def project_tailoring_doc(path):
    path = project_document_path(path)
    return SurveyDocument(path, getproject().mtsdict)
