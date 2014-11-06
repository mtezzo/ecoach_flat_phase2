import os
import logging

from tailoring2.documents import SurveyDocument
from tailoring2.common import Elements

from djangotailoring.project import getproject, project_tailoring_doc

logger = logging.getLogger(__name__)

class TailoringRequestError(Exception): pass

class MissingSectionError(TailoringRequestError): pass

class MissingDocumentError(TailoringRequestError): pass

# jared (use this for inbox - ignore render_transforms)
class TailoringRequest(object):
    
    def __init__(self, project, docpath=None, subject=None, source='',
                 render_transforms=None):
        if not project:
            project = getproject()
        self.project = project
        self.docpath = docpath
        self.subject = subject
        self.default_source = source
        self.render_transforms = render_transforms
    
    def __contains__(self, attr):
        return hasattr(self, attr)
    
    @property
    def messagedoc(self):
        if not hasattr(self, '_messagedoc'):
            logger.info('Fetching message doc: %s', self.docpath)
            if self.docpath is None:
                return None
            try:
                self._messagedoc = project_tailoring_doc(self.docpath)
            except IOError:
                logger.error('No message doc found.')
                raise MissingDocumentError("No document not found at '%s'" %
                    self.docpath)
        return self._messagedoc
    
    @property
    def sections(self):
        if not hasattr(self, '_sections'):
            logger.info('Finding section names in doc.')
            doc = self.messagedoc
            if doc is None:
                return {}
            self._sections = dict((section.get('name'), section)
                                  for section
                                  in doc.getiterator(Elements.SECTION_TAG))
            logger.debug('Sections found: %s', self._sections.keys())
        return self._sections
    
    def pipeline_for_section(self, section):
        try:
            section = self.sections[section]
        except KeyError:
            errormsg = "The section '%s' does not exist in %s " % (section,
                self.docpath)
            logger.error(errormsg)
            raise MissingSectionError(errormsg)
        return self.project.getpipeline(section, self.subject, self, self.render_transforms)
   
    # jared call this to get element tree 
    def render_section(self, section):
        logger.info('Rendering section "%s".', section)
        return self.pipeline_for_section(section).run()
    

