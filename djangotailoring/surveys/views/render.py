import logging

from tailoring2.common import ProcessingAttributes, ClassValues, ET
from tailoring2.render import SurveyCommandTranslator, BasicTransformList
from surveytracking.formatutils import tree_has_content

from djangotailoring.project import getproject
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)

def char_input_for_question(question_element):
    """Identify (as best as possible) the characteristic name for the given
    survey_question element."""
    prefix = ProcessingAttributes.SURVEY_ITEM_PREFIX
    prefix_len = len(prefix)
    itr = question_element.getiterator('input')
    try:
        input = iter(itr).next()
        name = input.get('name', '')
        if name.startswith(prefix):
            return name[prefix_len:], input
    except StopIteration:
        pass
    return None, None

def doctor_tree(tree, errors):
    """Insert the appropriate Survey Error elements to the given tree with
    the contents of an iterable of surveytracking.InvalidDataError exceptions.
    """
    logger.info('Re-inserting error values to survey tree')
    logger.debug('Errors: %s', errors)
    errors_dict = dict((error.key, error) for error in errors)
    for element in tree.getiterator():
        if element.get('class', '') == 'survey_question':
            char, input_element = char_input_for_question(element)
            try:
                error = errors_dict[char]
                logger.debug('Found question for "%s".', char)
            except KeyError:
                logger.debug('No error found for "%s".', char)
            else:
                error_element = ET.Element('div',
                    {'class': ClassValues.VALIDATE})
                if error.type == int:
                    error_element.text = _("Please enter a number.")
                else:
                    error_element.text = _("Please provide a valid response below.")
                element.insert(1, error_element)
                if input_element.get('type', '') == 'text':
                    logger.debug('Adding error value attribute.')
                    input_element.set('value', error.value)


class SurveyRenderChunk(object):
    def __init__(self, tree, subject, treq, page_data, show_errors,
            request_errors=None):
        self.tree = tree
        self.subject = subject
        self.treq = treq
        self.page_data = page_data
        self.show_errors = show_errors
        self.request_errors = request_errors
    
    def has_content(self):
        return tree_has_content(self.render()[0])
    
    def has_errors(self):
        return bool(self.render()[1])
    
    def render(self):
        if not hasattr(self, 'render_result'):
            logger.info('Rendering survey chunk.')
            self.render_result = self._with_request_errors(self._render())
            logger.info('Finished rendering.')
        return self.render_result
    
    render_segment = render
    
    def _with_request_errors(self, render_result):
        tree, errors = render_result
        if self.show_errors and self.request_errors:
            doctor_tree(tree, self.request_errors)
            errors.extend(self.request_errors)
        return tree, errors
    
    def _render(self):
        translator = SurveyCommandTranslator(self.page_data, self.show_errors)
        transforms = BasicTransformList(translator.translate)
        return getproject().getpipeline(self.tree, self.subject, self.treq,
            render_transforms=transforms).run()    
    

