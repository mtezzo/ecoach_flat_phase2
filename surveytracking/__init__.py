from projectutils import *
from formatutils import *
from slicing import *
from classes import *

from tailoring2.documents import SurveyDocument

def pages_from_tree(doctree, dictionary=None):
    deps = flat_dependency_map(dictionary) if dictionary is not None else {}
    return [Page(p) for p in
            DependencySlicer(doctree, deps).tree_segments()]
    
def pages_from_string(xmlstring, dictionary=None):
    return pages_from_tree(ET.fromstring(xmlstring), dictionary)
    
def pages_from_path(docpath, dictionary=None):
    return pages_from_tree(SurveyDocument(docpath, dictionary).getroot(),
        dictionary)

def manager_for_doctree(survey_doc, project=None, source=None):
    dictionary = project.mtsdict if project is not None else None
    pages = pages_from_tree(survey_doc, dictionary)
    return SurveyManager(pages, project, source=source)

def manager_from_string(xmlstring, project=None, dictionary=None, source=None):
    surveytree = ET.fromstring(xmlstring)
    if project is not None and dictionary is None:
        dictionary = project.mtsdict
    pages = pages_from_tree(surveytree, dictionary)
    return SurveyManager(pages, project, source=source)

def manager_from_path(docpath, project=None, dictionary=None, source=None):
    if dictionary is None and project is not None:
        dictionary = project.mtsdict
    return manager_for_doctree(SurveyDocument(docpath, dictionary).getroot(),
        project, source)


__all__ = ['Page', 'SurveyManager', 'SurveyState', 'DependencySlicer',
    'ClassicSlicer', 'OnePerPageSlicer', 'SurveySlicer', 'dump_pages',
    'flat_dependency_map', 'manager_from_string', 'manager_from_path',
    'InvalidDataError', 'ValidationError', 'InsufficientDataError',
    'EndOfSurvey', 'GotoDestination', 'pages_from_tree', 'pages_from_string',
    'pages_from_path']