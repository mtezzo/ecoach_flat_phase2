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

"""
Given a message document that has been through the selection pipeline,
here are functions for rendering it in HTML (or in plain text or,
someday, in other formats)
"""

import sys
import os
import os.path
import optparse
import copy
import itertools
import fileinput
import re
import functools
import warnings
from cStringIO import StringIO
from xml.sax.saxutils import unescape
import logging
log = logging.getLogger(__name__)

from tailoring2.common import *
from tailoring2.elementutil import cleanup
from tailoring2 import textutil
from tailoring2 import meld3
from tailoring2.util import string2bool
from tailoring2.authorutil import isEmpty
# ------------------------------------------------------------

SELECTION_ARTIFACTS = set([
        SourceAttributes.IF,
        SourceAttributes.ORDERBY,
        SourceAttributes.LIMIT])

CONTROL_ARTIFACTS = set([
        ProcessingAttributes.SELECTED,
        ProcessingAttributes.INDEX,
        ProcessingAttributes.LIMITED])

SURVEY_ARTIFACTS = set([
        SourceAttributes.CHARACTERISTIC,
        SourceAttributes.QUESTION_TYPE,
        SourceAttributes.GOTO])

# ------------------------------------------------------------
# utils

def bool_attr_value(elem, attr, default=True):
    """get the specified attribute from 'elem', evaluate the attribute
    string as a boolean and return the bool. If the attribute is not
    present, return the specified default value.
    """
    attr_value = elem.get(attr)
    if attr_value is None:
        return default
    return string2bool(attr_value)


def element_can_produce_content(elem):
    return elem.tag in Elements.CONTENT_PRODUCING_ELEMENTS


def element_is_leaf(elem):
    return elem.tag in Elements.LEAF_ELEMENTS


def replace_tags(tree, old, new):
    """change elements with tag 'old' to tag 'new' throughout tree. No
    modifications except the tag name.
    """
    for elem in tree.getiterator(old):
        elem.tag = new


def evict_nodes(tree, predicate):
    """entirely remove any elements (and their children) where
    predicate(e) is false.
    """
    # listcomp, not generator expr, for jython friendliness
    parent_map = dict([(c, p) for p in tree.getiterator() for c in p])
    evictable_nodes = [node for node in tree.getroot().getiterator() if not predicate(node)]
    for node in evictable_nodes:
        parent_map[node].remove(node)


def filter_attributes(tree, attr_filter):
    """traverse all the tree's elements, removing attributes for which
    attr_filter(attrkey, attrvalue) is False.
    """
    for elem in tree.getiterator():
        saved_attribs = dict([(key, value) for key, value in elem.attrib.items()
                if attr_filter(key, value)])
        elem.attrib.clear()
        elem.attrib.update(saved_attribs)
    
def survey_name(name):
    return u'%s%s' % (ProcessingAttributes.SURVEY_ITEM_PREFIX, name)
# ------------------------------------------------------------
# lower-level utility sub-phases. These all directly modify the tree.

def RemoveUnselectedCommands(tree):
    """remove commands where selected == false"""
    def is_selected_predicate(elem):
        return bool_attr_value(elem, ProcessingAttributes.SELECTED, default=True)
    evict_nodes(tree, is_selected_predicate)


def RemoveLimitedCommands(tree):
    """remove commands where limited == true"""
    def is_within_limits_predicate(elem):
        return not bool_attr_value(elem, ProcessingAttributes.LIMITED, default=False)
    evict_nodes(tree, is_within_limits_predicate)


class CommandTranslator(object):
    """
    <section> --> <div id="{name}">
    <block> --> <div*>
    <select> --> <div*>
    <list> --> <ul>
    <listitem> --> <li>
    <text> --> <span*>
    <heading> --> <h2>
    <graphic> --> <img>
    <paragraph> --> <p>
    
    *- only translate <block>, <select>, or <text> if the element has a
    'tag' attr set; otherwise, include the content inline. (HoistNullTags
    does the actual work of inlining the content.)
    """
    
    def translate(self, tree):
        for elem in tree.getiterator():
            method_name = "translate_%s" % (elem.tag.lower())
            try:
                method = getattr(self, method_name)
                method(elem)
            except AttributeError, err:
                log.debug("no translator for %s, leaving untouched" % elem.tag)
                pass
            if elem.get('tag'):
                del elem.attrib['tag']

    def should_wrap_command(self, elem):
        # if has a tag
        return elem.get('tag') is not None

    def wrap_command(self, elem, default_tag=None):
        # set tag and trigger name->id translation
        # XXX- what if the elem has no explicit 'tag' attr and default_tag isn't
        # passed? Then tag goes to None and the element is probably later stripped
        # out of the output by HoistNullTags.
        tag = elem.get('tag', default_tag)
        elem.tag = tag
        if elem.get('tag'):
            del elem.attrib['tag']
        if elem.get('name'):
            elem.set('id', elem.get('name'))
            del elem.attrib['name']

    def strip_command(self, elem):
        # set tag to none, clear class and name attrs
        elem.tag = None
        if elem.get('class'):
            del elem.attrib['class']
        if elem.get('name'):
            del elem.attrib['name']

    def translate_section(self, elem):
        elem.tag = 'div'
        name = elem.get('name')
        if name is None:
            errmsg = "section has no 'name' attribute"
            err = AttributeError(errmsg)
            raise ProcessingError(err, 'render', elem, message=errmsg)
        self.wrap_command(elem, default_tag='div')
        
    def translate_block(self, elem):
        if self.should_wrap_command(elem):
            self.wrap_command(elem)
        else:
            self.strip_command(elem)
        
    def translate_select(self, elem):
        # same as block
        self.translate_block(elem)
    
    def translate_list(self, elem):
        elem.tag = elem.get('tag', 'ul')
        if elem.get('name'):
            elem.set('id', elem.get('name'))
            del elem.attrib['name']
        if elem.get('listtype'):
            if elem.get('listtype') == 'bulleted':
                elem.tag = 'ul' 
            elif elem.get('listtype') == 'numbered':
                elem.tag = 'ol'    
            del elem.attrib['listtype']               
            
    def translate_listitem(self, elem):
        elem.tag = elem.get('tag', 'li')
        if elem.get('name'):
            elem.set('id', elem.get('name'))
            del elem.attrib['name']                       

    def translate_text(self, elem):
        if self.should_wrap_command(elem):
            self.wrap_command(elem, 'span')
        else:
            self.strip_command(elem)
        
    def translate_heading(self, elem):
        elem.tag = elem.get('tag', 'h2')
        if elem.get('name'):
            elem.set('id', elem.get('name'))
            del elem.attrib['name']        
    
    def translate_graphic(self, elem):
        elem.tag = elem.get('tag', 'img')
        elem.set('src', elem.text.strip())
        elem.set('alt', elem.text.strip())
        elem.text = None
        if elem.get('name'):
            elem.set('id', elem.get('name'))
            del elem.attrib['name']            

    def translate_paragraph(self, elem):
        elem.tag = elem.get('tag', 'p')
        if elem.get('name'):
            elem.set('id', elem.get('name'))
            del elem.attrib['name']           




class SurveyCommandTranslator(CommandTranslator):
    """translate survey commands into html
    """
    
    # IJ: combine this with CommandTranslator?
    # IJ: need lots of tests
    
    def __init__(self, data_dictionary={}, show_validation=True):
        self.data_dictionary = data_dictionary
        self.show_validation = show_validation
    
    def translate(self, elem):
        if isinstance(elem, ET.ElementTree):
            elem = elem.getroot()
        """wholesale override of the superclass translate. This translate
        will iterate in the same order, however it will allow visited elements
        to modify their children before proceding."""
        try:
            method_name = "translate_%s" % (elem.tag.lower())
            method = getattr(self, method_name)
            method(elem)
        except AttributeError, err:
            log.debug("no translator for %s, leaving untouched" % elem.tag)
            pass
        if elem.get('tag'):
            del elem.attrib['tag']
        for child in elem:
            self.translate(child)

    def data_value(self, characteristic_name, question_type=QuestionTypeValues.FILLIN):
        """ get value from the data_dictionary if any"""
        characteristic_value = None
        
        try:
            characteristic_value = self.data_dictionary[characteristic_name]
        except KeyError:
            pass
        except TypeError:
            pass
        
        # Convert multiple response types (checkbox) into list """
        if question_type == QuestionTypeValues.CHECKBOX:
            if characteristic_value is None:
                characteristic_value = []
            else:
                if not isinstance(characteristic_value, list):
                    characteristic_value = unicode(characteristic_value).split(',')
                else:
                    characteristic_value = [unicode(v) for v in characteristic_value]
        else:
            if characteristic_value is not None:
                characteristic_value = unicode(characteristic_value)
                        
                
        log.debug("Converted value = %s" % characteristic_value)
        return characteristic_value
    
    def copy_attributes(self, source, destination):
        for key in source.keys():
            value = source.get(key)
            if value is not None:
                destination.set(key, value)
                                
    def translate_question(self, question):
        """ Method description """
        
        # Get characteristic from dictionary
        characteristic_name = question.get(SourceAttributes.CHARACTERISTIC, u'')

        if has_class(question, ClassValues.GROUP_ITEM):
            question.tag = 'span'
        else:
            question.tag = 'div'
            
        if question.get('name'):
            question.set('id', question.get('name'))
            del question.attrib['name']
        add_class(question, ClassValues.QUESTION)
            
        question_type = question.get(SourceAttributes.QUESTION_TYPE, '')
        
        characteristic_value = self.data_value(characteristic_name, question_type)        
        
        responses_div = ET.Element('div')
        add_class(responses_div, ClassValues.RESPONSES)
        question.append(responses_div)
       
        # make some edits to control textarea versus text HTML tags 
        if question_type == QuestionTypeValues.FILLIN:
            if int(question.get(SourceAttributes.SIZE)) > 100:
                input_element = ET.Element('textarea')
                responses_div.append(input_element)
                input_element.set('name', survey_name(characteristic_name))
                
                if characteristic_value is not None:
                    input_element.text = characteristic_value
            else:
                input_element = ET.Element('input')
                responses_div.append(input_element)
                input_element.set('type', 'text')
                input_element.set('name', survey_name(characteristic_name))
                input_element.set('size', question.get(SourceAttributes.SIZE))
                
                if characteristic_value is not None:
                    input_element.set('value', characteristic_value)
            
        if question_type == QuestionTypeValues.DATE:
            """ For dates, create a div with Month popup, Day fillin and Year fillin. """
            date_div = ET.Element('div')
            responses_div.append(date_div)
            add_class(date_div, ClassValues.RESPONSE)
            
            month_element = ET.Element('html_select')
            date_div.append(month_element)
            month_element.set('name', survey_name(u'%s_month' % characteristic_name))
            
            for month_name in SurveyRenderConstants.ENGLISH_MONTHS_LONG:
                month_option = ET.Element('option')
                month_element.append(month_option)
                month_option.set('value', unicode(SurveyRenderConstants.ENGLISH_MONTHS_LONG.index(month_name) + 1))
                month_option.text = month_name
                
            day_element = ET.Element('input')
            date_div.append(day_element)
            day_element.set('type', 'text')
            day_element.set('name', survey_name(u'%s_day' % characteristic_name))
            day_element.set('maxlength', '2')
            day_element.set('size', '2')
            
            year_element = ET.Element('input')
            date_div.append(year_element)
            year_element.set('type', 'text')
            year_element.set('name', survey_name(u'%s_year' % characteristic_name))
            year_element.set('maxlength', '4')
            year_element.set('size', '4')

        if question_type == QuestionTypeValues.RADIO or \
            question_type == QuestionTypeValues.CHECKBOX:

            others = question.findall(Elements.OTHER_TAG)
            other_values = dict((other.get(SourceAttributes.RESPONSE_VALUE, u''), other)
                            for other in others)
            # find all responses and render as a inputs
            responses = question.findall(Elements.RESPONSE_TAG)
            for response_element in responses:
                response_subelements = list(response_element)
                for subelement in response_subelements:
                    response_element.remove(subelement)
                response_div = ET.Element('div')
                responses_div.append(response_div)
                
                self.copy_attributes(response_element, response_div)
                add_class(response_div, ClassValues.RESPONSE)
                label_element = ET.Element('label')
                response_div.append(label_element)
                
                input_element = ET.Element('input')
                label_element.append(input_element)
                
                input_element.set('type', question_type)
                input_element.set('name', survey_name(characteristic_name))
                response_value = response_element.get(SourceAttributes.RESPONSE_VALUE)
                input_element.set('value', response_value)
                selected_response = False
                if question_type == QuestionTypeValues.CHECKBOX:
                    selected_response = response_value in characteristic_value
                else:
                    selected_response = response_value == characteristic_value
                if selected_response:
                    input_element.set('checked', 'checked')
                        
                if response_value:                         
                    input_element.set('id', survey_name(characteristic_name) + "_" + response_value)
                    label_element.set('for', survey_name(characteristic_name) + "_" + response_value)
                    
                # del response_element.attrib['value']
                
                label_content = ET.Element('span')
                label_element.append(label_content)
                
                for subelement in response_subelements:
                    label_content.append(subelement)
                
                if response_value in other_values:
                    other = other_values[response_value]
                    self.create_other_response(other, label_element, response_div)
                    question.remove(other)
                
                question.remove(response_element)
                
                # response_text = response_element.text
                # if response_text is not None and not response_text.isspace():
                #     label_content.text = response_text
                #     response_element.text = None
                # 
                # if label_content.text is None:
                #     label_content.text = response_value
                
        if question_type == QuestionTypeValues.SCALE:
            scale_table_element = ET.Element('table')
            responses_div.append(scale_table_element)
             
            scale_tbody_element = ET.Element('tbody')
            scale_table_element.append(scale_tbody_element)
            
            scale_tbody_tr_element = ET.Element('tr')
            scale_tbody_element.append(scale_tbody_tr_element)
            
            """ find all responses and render as a inputs """
            responses = question.findall(Elements.RESPONSE_TAG)
            for response in responses:
                response_subelements = list(response)
                for subelement in response_subelements:
                    response.remove(subelement)
                scale_item_element = ET.Element('td')
                self.copy_attributes(response, scale_item_element)

                scale_tbody_tr_element.append(scale_item_element)
                scale_item_element.set('width', '%d%%' % (100 / len(responses)))
                
                add_class(scale_item_element, ClassValues.RESPONSE)
                
                input_element = ET.Element('input')
                
                input_element.set('type', QuestionTypeValues.RADIO)
                input_element.set('name', survey_name(characteristic_name))
                response_value = response.get(SourceAttributes.RESPONSE_VALUE)
                input_element.set('value', response_value)
                if characteristic_value is not None and response_value == characteristic_value:
                    input_element.set('checked', 'checked')
                
                self.create_labeled_response(question, scale_item_element, input_element, response_subelements, 'top')
                question.remove(response)
                
        if question_type == QuestionTypeValues.POPUP:
            """ find first response """
            response = question.find(Elements.RESPONSE_TAG)
            try:
                response_index = list(question).index(response)
            except ValueError:
                response_index = 0
                
            select_element = ET.Element('html_select')
            responses_div.append(select_element)
            select_element.set('name', survey_name(characteristic_name))
            
            """ find all responses and render as a inputs """
            responses = question.findall(Elements.RESPONSE_TAG)
            for response_element in responses:
                response_subelements = list(response_element)
                for subelement in response_subelements:
                    response_element.remove(subelement)
                option_element = ET.Element('option')
                self.copy_attributes(response, option_element)
                select_element.append(option_element)
                
                response_value = response_element.get(SourceAttributes.RESPONSE_VALUE)
                option_element.set('value', response_value)
                if characteristic_value is not None and response_value == characteristic_value:
                    option_element.set('selected', 'selected')
                
                for subelement in response_subelements:
                    option_element.append(subelement)
                
                question.remove(response_element)
                
            
            # Render other if it exists
            others = question.findall(Elements.OTHER_TAG)
            for other in others:
                self.create_other_response(other, select_element, responses_div)
                question.remove(other)

    def create_other_response(self, other, response_element, responses_div):
        other_element = ET.Element('input')
        self.copy_attributes(other, other_element)
        response_element.tail = '&nbsp;'
        responses_div.append(other_element)
        other_element.set('type', 'text')
        other_characteristic_name = other.get(SourceAttributes.CHARACTERISTIC, u'')
        other_element.set('name', survey_name(other_characteristic_name))
        other_value = self.data_value(other_characteristic_name)
        if other_value is not None:
            other_value = unicode(other_value)
        other_element.set('value', other_value)
    
    def create_labeled_response(self, question, question_response_element, input_element, response_text_elements, default_label_location='none'):
        value_label_location = question.get(SourceAttributes.VALUE_LABEL_LOCATION)
        if (value_label_location is None or
                value_label_location.isspace() or
                len(value_label_location) == 0):
           value_label_location = default_label_location

        if value_label_location != 'none':
            # sample generated: <label><input name="InsuranceType" type="radio" value="HMO" /><span>HMO</span></label>
            label_element = ET.Element('label')
            question_response_element.append(label_element)
            
            if input_element.get('value'):
                input_element.set('id', input_element.get('name') + "_" + input_element.get('value'))
                label_element.set('for', input_element.get('name') + "_" + input_element.get('value'))
            
            label_span = ET.Element('span')
            for subelement in response_text_elements:
                label_span.append(subelement)
            
            if value_label_location == 'left':
                label_element.append(label_span)
                label_element.append(input_element)
            elif value_label_location == 'top':
                label_element.append(label_span)
                label_element.append(ET.Element('br'))
                label_element.append(input_element)
            elif value_label_location == 'right':
                label_element.append(input_element)
                label_element.append(label_span)
            elif value_label_location == 'bottom':
                label_element.append(input_element)
                label_element.append(ET.Element('br'))
                label_element.append(label_span)
        else:
            label_element = ET.Element('label')
            question_response_element.append(label_element)
            label_span = ET.Element('span')
            label_span.text = ''
            label_element.append(input_element)
            label_element.append(label_span)

    def translate_matrix(self, matrix):
        """ Render a full-fleshed out matrix element, and all its sub-elements """
        
        # At this point matrix_type can't be None.
        matrix_type = matrix.get(SourceAttributes.QUESTION_TYPE)
            
        matrix.tag = 'div'
        if matrix.get('name'):
            matrix.set('id', matrix.get('name'))
            del matrix.attrib['name']
        add_class(matrix, ClassValues.MATRIX)
        
        subelements = matrix.find(Elements.SUBELEMENTS_TAG)
        
        responses_div = ET.Element('div')
        add_class(responses_div, ClassValues.RESPONSES)
        matrix.append(responses_div)

        """ Get responses """
        responses = matrix.findall(Elements.RESPONSE_TAG)
        
        """ Get questions """
        questions = matrix.findall(Elements.QUESTION_TAG)
        
        table_element = ET.Element('table')
        responses_div.append(table_element)
                
        response_subelements = {}
        
        for response in responses:
            my_subelements = list(response)
            response_subelements[response] = my_subelements
            for subelement in my_subelements:
                response.remove(subelement)
        
        if len(responses) > 0 and matrix_type != QuestionTypeValues.POPUP:
            if len(responses) > 3:
                matrix_item_width = int((100 - SurveyRenderConstants.WIDTH_MATRIX_PROMPT) / len(responses))
            else:
                matrix_item_width = int((100 - SurveyRenderConstants.WIDTH_NARROW_MATRIX_PROMPT) / len(responses))
            matrix_prompt_width = 100 - (matrix_item_width * len(responses))
    
            show_column_header = matrix.get(SourceAttributes.COLUMN_HEADER)
            show_column_header = show_column_header if show_column_header is not None and not show_column_header.isspace() and len(show_column_header) > 0 else 'on'
            
            if show_column_header == 'on':
                # Create the header
                thead_element = ET.Element('thead')
                table_element.append(thead_element)
                add_class(thead_element, ClassValues.MATRIX_ROW0)
                
                thead_tr_element = ET.Element('tr')
                thead_element.append(thead_tr_element)

                thead_prompt_element = ET.Element('th')
                thead_tr_element.append(thead_prompt_element)
                thead_prompt_element.set('width', '%d%%' % matrix_prompt_width)
            
                for response in responses:
                    thead_item_element = ET.Element('th')
                    thead_tr_element.append(thead_item_element)
                    thead_item_element.set('width', '%d%%' % matrix_item_width)
                    for subelement in response_subelements[response]:
                        thead_item_element.append(subelement)
        else:
            matrix_item_width = 100 - SurveyRenderConstants.WIDTH_MATRIX_PROMPT
            matrix_prompt_width = 100 - matrix_item_width
                
        tbody_element = ET.Element('tbody')
        table_element.append(tbody_element)
        
        """ Create each question row """
        question_row_index = 0
        for question in questions:
            characteristic_name = question.get(SourceAttributes.CHARACTERISTIC, u'')
            characteristic_value = self.data_value(characteristic_name, matrix_type)
            
            question_row_element = ET.Element('tr')
            tbody_element.append(question_row_element)
            add_class(question_row_element,
                u'%s%d' % (ClassValues.MATRIX_ROW, question_row_index % 2 + 1 ))
            
            question_prompt_td = ET.Element('td')
            question_row_element.append(question_prompt_td)
            
            question_prompt_span = ET.Element('span')
            question_prompt_td.append(question_prompt_span)
            add_class(question_prompt_span, ClassValues.QUESTION)
            question_prompt_content = question.find(Elements.TEXT_TAG)
            question_prompt_span.text = question_prompt_content.text
            
            # # the above should probably be something along the lines of:
            # question_prompt_span = ET.Element('span')
            # question_prompt_td.append(question_prompt_span)
            # add_class(question_prompt_span, ClassValues.QUESTION)
            # question_prompt_span[:] = question.getchildren()
            
            validator = question.find(Elements.VALIDATE_TAG)
            if validator is not None:
                validator = deepcopy_element(validator);
                question_prompt_td.append(validator)
                self.translate_validate(validator)
                                
            if len(responses) > 0 and matrix_type != QuestionTypeValues.POPUP:
                for response in responses:
                    question_response_td = ET.Element('td')
                    question_row_element.append(question_response_td)
                    question_response_td.set('align', 'center')
                    response_value = response.get(SourceAttributes.RESPONSE_VALUE)
                    
                    if matrix_type == QuestionTypeValues.RADIO or \
                        matrix_type == QuestionTypeValues.CHECKBOX:
                        input_element = ET.Element('input')
                        input_element.set('type', matrix_type)
                        input_element.set('name', survey_name(characteristic_name))
                        input_element.set('value', response_value)
                        
                        if matrix_type == QuestionTypeValues.RADIO:
                            if characteristic_value is not None and response_value == unicode(characteristic_value):
                                input_element.set('checked', 'checked')

                        if matrix_type == QuestionTypeValues.CHECKBOX:
                            if characteristic_value is not None and response_value in unicode(characteristic_value):
                                input_element.set('checked', 'checked')

                        self.create_labeled_response(matrix, question_response_td, input_element, response_subelements[response], 'none') 
            else:
                question_response_td = ET.Element('td')
                question_row_element.append(question_response_td)

                if matrix_type == QuestionTypeValues.FILLIN:
                    input_element = ET.Element('input')
                    question_response_td.append(input_element)
                    input_element.set('type', 'text')
                    input_element.set('name', survey_name(characteristic_name))
                    if characteristic_value is not None:
                        input_element.set('value', characteristic_value)
        
                if matrix_type == QuestionTypeValues.DATE:
                    """ For dates, create a span with Month popup, Day fillin and Year fillin. """
                    month_element = ET.Element('html_select')
                    question_response_td.append(month_element)
                    month_element.set('name', survey_name(u'%s_month' % characteristic_name))
                    
                    for month_name in SurveyRenderConstants.ENGLISH_MONTHS_LONG:
                        month_option = ET.Element('option')
                        month_element.append(month_option)
                        month_option.set('value', unicode(SurveyRenderConstants.ENGLISH_MONTHS_LONG.index(month_name) + 1))
                        month_option.text = month_name
                        
                    day_element = ET.Element('input')
                    question_response_td.append(day_element)
                    day_element.set('type', 'text')
                    day_element.set('name', survey_name(u'%s_day' % characteristic_name))
                    day_element.set('maxlength', '2')
                    day_element.set('size', '2')
                    
                    year_element = ET.Element('input')
                    question_response_td.append(year_element)
                    year_element.set('type', 'text')
                    year_element.set('name', survey_name(u'%s_year' % characteristic_name))
                    year_element.set('maxlength', '4')
                    year_element.set('size', '4')

                if matrix_type == QuestionTypeValues.POPUP:
                    """ find first response """
                    select_element = ET.Element('html_select')
                    question_response_td.append(select_element)
                    select_element.set('name', survey_name(characteristic_name))
                    
                    """ find all responses and render as a inputs """
                    for response in responses:
                        response_value = response.get(SourceAttributes.RESPONSE_VALUE)
                        option_element = ET.Element('option')
                        select_element.append(option_element)
                        
                        option_element.set('value', response_value)
                        if characteristic_value is not None and characteristic_value == response_value:
                            option_element.set('selected', 'selected')
                            
                        for subelement in response_subelements[response]:
                            option_element.append(subelement)
                            
            question_row_index = question_row_index + 1

            matrix.remove(question)
            
        for response in responses:
            matrix.remove(response)
    
    def translate_validate(self, validator):
        if self.show_validation:
            if has_class(validator, ClassValues.GROUP_ITEM):
                validator.tag = 'span'
            else:
                validator.tag = 'div'

            add_class(validator, ClassValues.VALIDATE)
            content_element = validator.get(Elements.CONTENT_TAG)
            if content_element is not None:
                validator.text = content_element.text
        else:
            validator.tag = None # strip this content
            validator.text = None # strip this content
    
    def translate_group(self, group):
        group.tag = 'div'
        add_class(group, ClassValues.GROUP)


#class SurveyCommandTranslatorNoSelection(SurveyCommandTranslator):
#    """translate survey commands to html but without removing unselected
#    elements
#    """
#    def translate_validate(self, validator):
#        if validator.get(ProcessingAttributes.CLASS) == ClassValues.GROUP_ITEM:
#            validator.tag = 'span'
#        else:
#            validator.tag = 'div'
#
#        validator.set(ProcessingAttributes.CLASS, ClassValues.VALIDATE)
#        content_element = validator.get(Elements.CONTENT_TAG)
#        if content_element is not None:
#            validator.text = content_element.text
#            
#    # TODO: handle goto

 
class CommandTranslatorWithAnnotations(SurveyCommandTranslator):
    """Wrap content-bearing elements like text, listitem, and heading in
    a <span> element so they can be styled for debug output.
    """
    # TODO: need tests
    
    def should_wrap_command(self, elem):
        # ... equivalent to 'return True' ??
        return elem.get('msgid') or elem.get('class') or elem.get('name') or elem.get('tag')
        


class CommandTranslatorWithBibleVerse(SurveyCommandTranslator):
    
    # TODO: need tests

    # TODO: override should_wrap_command() to always return True (or
    # just True for text/heading)
    # TODO: override wrap_command() to include bible verse
    
    def translate_text(self, elem):
        newtag = elem.get('tag', 'span')
        if elem.get('msgid') or elem.get('class') or elem.get('name') or elem.get('tag'):
            elem.tag = newtag
            if elem.get('name'):
                elem.set('id', elem.get('name'))
                del elem.attrib['name']
            if elem.get('msgid'):
                bvlink = ET.Element('a', {'class': 'bv-link', 'href': '#id-%s' % elem.get('msgid')})
                bvlink.tail = elem.text
                bvlink.text = elem.get('msgid')
                elem.text = ''
                elem.insert(0, bvlink)
        else:
            elem.tag = None
    
    def translate_heading(self, elem):
        newtag = elem.get('tag', 'h2')
        if elem.get('msgid') or elem.get('class') or elem.get('name') or elem.get('tag'):
            elem.tag = newtag
            if elem.get('name'):
                elem.set('id', elem.get('name'))
                del elem.attrib['name']
            if elem.get('msgid'):
                bvlink = ET.Element('a', {'class': 'bv-link', 'href': '#id-%s' % elem.get('msgid')})
                bvlink.tail = elem.text
                bvlink.text = elem.get('msgid')
                elem.text = ''
                elem.insert(0, bvlink)
        else:
            elem.tag = None


# ------------------------------------------------------------

def RemoveExtraneousContainers(tree):
    """ This function along with removing extraneous containers will 
    recognize the unique nature of content elements and ensure that 
    the tail attribute has at minimum one piece of whitespace so that 
    on later cleanup content elements next together with the assumed 
    one space separating each. eg. text "Hello" text "$firstName" as two 
    text rows will automagically get a space between them this way.  
    """
    def is_extraneous_container(elem):
        if elem.tag == Elements.CONTENT_TAG:
            if elem.tail is None or len(elem.tail) <=0:
                elem.tail = " "
        return elem.tag in [Elements.SUBELEMENTS_TAG, Elements.CONTENT_TAG]
    cleanup(tree.getroot(), lambda e: not is_extraneous_container(e))


def HoistNullTags(tree):
    cleanup(tree.getroot(), lambda e: e.tag)


def RemoveHTMLWrappers(tree):
    """a previous phase may have introduced html 'select' elements --
    but in order that they not conflict with the existing <select>
    message command, they came in as <html_select>. This transform,
    intended to be run after the message command <select> has been
    handled, puts in the <select> input fields.
    """
    for element in tree.getiterator(Elements.HTML_SELECT_TAG):
        element.tag = 'select'


def ReorderSelectChildren(tree):
    # note: handles both <select> and <list> elements
    for select_elem in itertools.chain(tree.getiterator(Elements.SELECT_TAG), 
            tree.getiterator(Elements.LIST_TAG)):
        subelem = select_elem.find(Elements.SUBELEMENTS_TAG)
        select_children = [(int(child.get(ProcessingAttributes.INDEX, '0')), child)
                for child in subelem.getchildren()]
        select_children.sort()
        select_children = [child for i, child in select_children]
        subelem[:] = select_children


def HoistSelectChildren(tree):
    cleanup(tree.getroot(), lambda e: not e.tag == Elements.SELECT_TAG)


#def RenderSelectionAsNote(tree):
#    for elem in tree.getiterator():
#        logic = elem.get(SourceAttributes.IF)
#        if logic is not None:
#            if elem.tag == 'span':
#                logic_element = ET.Element('span')
#            else:
#                logic_element = ET.Element('div')
#            logic_element.set(ProcessingAttributes.CLASS, 'note')
#            logic_element.text = logic.replace('<', '&lt;')
#            elem.insert(-1, logic_element)
        

def RemoveComments(tree):
    evict_nodes(tree, lambda e:e.tag != 'comment')
    

def RemoveNotes(tree):
    evict_nodes(tree, lambda e: e.tag != 'note')


def RemoveSelectionArtifacts(tree):
    """remove attributes added by the selection pipeline"""
    filter_attributes(tree, lambda k, v: k not in SELECTION_ARTIFACTS)


def RemoveControlArtifacts(tree):
    """remove attributes present in the source that should never be in the output"""
    filter_attributes(tree, lambda k, v: k not in CONTROL_ARTIFACTS)


def RemoveSurveyArtifacts(tree):
    """remove attributes present in survey sources that should never be in the output"""
    filter_attributes(tree, lambda k, v: k not in SURVEY_ARTIFACTS)


def RemoveDeadAttributes(tree):
    """remove attributes for which the value is None"""
    filter_attributes(tree, lambda k, v: v is not None)


def RemoveVersionAttributes(tree):
    """remove the docversion and mtsversion attributes on the document root"""
    try:
        del tree.getroot().attrib['docversion']
        del tree.getroot().attrib['mtsversion']
    except KeyError, err:
        pass
    
    
def ModifyListItems(tree):
    """TODO: write description of what this does. I think it's
    concatenating listitem text into <li> elements. [-IJ Nov 09]
    """
    listitems = list(tree.getiterator('listitem'))
    for listelem in listitems:
        content_el = listelem.find(Elements.CONTENT_TAG)
        subelements_el = listelem.find(Elements.SUBELEMENTS_TAG)
        
        if content_el is not None and not isEmpty(content_el.text):
            newtext = ET.Element(Elements.TEXT_TAG) 
            newcontent = ET.Element(Elements.CONTENT_TAG)
            newcontent.text = content_el.text
            newtext.append(newcontent)
            if subelements_el is None:
                subelements_el = ET.Element(Elements.SUBELEMENTS_TAG)
                listelem.append(subelements_el)
            subelements_el.insert(0,newtext)
  
            listelem.remove(content_el)   


def InterpolateTextParagraphs(tree):
    """inspect the .text attribute of every leaf element in the tree and
    insert a new htmlescaped <p/> element wherever there is a run of >=2
    newlines.
    
    Assumes there is no <content> container; it has already been
    hoisted. Also assume there is no mixed content in the tree -- any
    formatting elements like <b> or <i> are still htmlescaped strings.
    """
    for elem in tree.getiterator():
        if not element_is_leaf(elem):
            continue
        if '\n\n' in elem.text.replace("\r\n", "\n"):
            interpolate_p(elem)
    
    
def RemoveWhitespaceText(tree):
    """remove runs of whitespace in all elements"""
    for elem in tree.getiterator():
        if elem.text is not None:
            elem.text = textutil.trim_whitespace(elem.text)
        if elem.tail is not None:
            elem.tail = textutil.trim_whitespace(elem.tail)


def RemoveMsgIDAttributes(tree):
    """remove msgid="xx" attributes from all elements"""
    filter_attributes(tree, lambda k, v: k not in ['msgid'])


def Noop(tree):
    """a transformer that does nothing -- a placeholder"""
    pass

        
def CompositeTransform(*transforms):
    """return a transformer that runs a series of transforms on the same tree"""
    def composite(tree):
        for transform in transforms:
            transform(tree)
    composite.func_name = 'composite: %s' % repr(transforms)
    return composite


# ------------------------------------------------------------
# collections of frequently-applied transforms

IMPLEMENT_SELECTION = CompositeTransform(
    RemoveUnselectedCommands,
    RemoveLimitedCommands,
    ReorderSelectChildren,
)

REMOVE_ARTIFACTS = CompositeTransform(
    ModifyListItems,                  
    RemoveSelectionArtifacts,
    RemoveControlArtifacts,
    RemoveExtraneousContainers,
    RemoveComments,
    RemoveNotes,
)

#REMOVE_ARTIFACTS_EXCEPT_SELECTION = CompositeTransform(
#    ModifyListItems,
#    RemoveControlArtifacts,
#    RemoveExtraneousContainers,
#    RemoveComments,
#    RemoveNotes,
#)

HOIST = CompositeTransform(
    HoistSelectChildren,
    HoistNullTags,
)

CLEANUP = CompositeTransform(
    RemoveHTMLWrappers,
    RemoveWhitespaceText,
    RemoveDeadAttributes,
)


def BasicTransformList(translator_method, remove_msgids=True):
    """return a list of the transforms typically used for producing
    final-output messages.

    translator_method is from your particular command translator
        instance (for example, CommandTranslator().translate)
    
    remove_msgids should be False if the rendered message should still
        have msgid attributes and whitespace, which may be useful for
        debugging.
    """
    return [
        IMPLEMENT_SELECTION,
        REMOVE_ARTIFACTS,
        RemoveVersionAttributes if remove_msgids else Noop,
        translator_method,
        RemoveSurveyArtifacts,
        HOIST,
        CLEANUP,
        RemoveMsgIDAttributes if remove_msgids else Noop,
    ]

#def BasicTransformListNoSelection(translator_method, remove_msgids=True):
#    """return a list of the transforms typically used for producing
#    debug-output messages. Parameters as for BasicTransformList.
#    """
#    return [
#        REMOVE_ARTIFACTS_EXCEPT_SELECTION,
#        translator_method,
#        RemoveSurveyArtifacts,
#        HOIST,
#        RenderSelectionAsNote,
#        CLEANUP,
#        RemoveMsgIDAttributes if remove_msgids else Noop,
#    ]


DEFAULT_TRANSFORMS = BasicTransformList(SurveyCommandTranslator().translate)


#RENDER_HTML_NO_SELECTION_TRANSFORMS = BasicTransformListNoSelection(
#    SurveyCommandTranslatorNoSelection().translate)


# ------------------------------------------------------------
# top-level output renderers. These work on a copy of the tree and return the
# modified copy.    

def RenderHTML(tree, transforms=None):
    """Given a tree that's been through the selection pipeline (ie,
    marked up with 'selected', 'limited', 'index' attributes, etc.),
    return a tree of HTML elements. Do not modify the incoming tree.

    tree is an ET.ElementTree instance that is a marked-up message
    document.
    
    transforms is an optional list of transform functions to apply to
    the tree. If not supplied, the default list of transforms will be
    used.
    """
    log.debug(">>> RenderHTML()")
    if log.isEnabledFor(logging.DEBUG):        
        log.debug("pre-transformed tree = %s" % ET.tostring(tree.getroot()))    
    if transforms is None:
        transforms = DEFAULT_TRANSFORMS
    return Transform(tree, transforms)


def Transform(tree, transforms):
    """apply a list of transform functions to the tree. Do not modify
    the incoming tree.
    
    tree is an ET.ElementTree instance. (Normally it would be a
    selection-marked message doc tree but that's not a requirement, so
    long as the transform functions get the kind of tree they are
    expecting.) A copy is made of the tree object before the transforms
    are applied, so the original tree parameter is not modified.

    transforms is a list of transform functions. Each takes one
    argument, a tree, and returns nothing (they operate by modifying the
    tree).
    
    Return a (tree, errors) tuple where tree is a transformed copy of
    the original tree and errors is a list of ProcessingErrors
    encountered.
    """
    tree = deepcopy_elementtree(tree)
    errors = []
    for transform in transforms:
        log.debug(transform)
        try:
            transform(tree)
        except ProcessingError, err:
            # err.location may get clobbered by later phases, so try to preserve it            
            # IJ Apr 09: Huh? shouldn't we make a deep copy of the _error_?
            err.location = copy.copy(err.location)
            errors.append(err)
        if log.isEnabledFor(logging.DEBUG):
            if hasattr(transform, 'im_class') and hasattr(transform.im_class, 'translate'):
                log.debug("skipping translator.translate")
                continue
            log.debug("after %s" % transform)
            try:
                log.debug(ET.tostring(tree.getroot()))
            except Exception, err:
                # ET.tostring() will choke if any tags have been set to None (as they
                # might have to signal later hoisting). Since this is just debug output,
                # we blithely skip ahead.
                log.warn("error showing debug output for transform %s: %s" % (transform, err))
                log.warn("skipping debug output for %s" % transform)
            log.debug("# ------------------------------------------------------------")
    if log.isEnabledFor(logging.DEBUG):        
        log.debug("post-transformed tree = %s" % ET.tostring(tree.getroot()))
        log.debug("# ------------------------------------------------------------")
    return (tree, errors)


def RenderText(tree):
    """Given a tree that's been through the selection pipeline, return a
    string: the selected tailored output rendered as text. Do not modify
    the incoming tree. Ignore any unescaped markup.
    
    When concatenating markup elements, insert a space character between
    words if one is needed.
    """
    html_tree, errors = RenderHTML(tree)
    buf = StringIO()
    html_tree.write(buf)
    buf.flush()
    text_markup = buf.getvalue()
    buf.close()
    return (textutil.get_text(text_markup), errors)
    

def RenderTable(tree):
    """render output as an html table with four columns, preserving
    selection information, in the style of the old message doc format.
    
    TODO -- steal from tailorweb's testing or coverage pages
    """
    raise NotImplementedError
    

##
# custom HTML escape on output

# for our purposes, meld3._write_xml() needs to take the same number of
# args as _write_html()
_write_xml = functools.partial(meld3._write_xml, pipeline=False, xhtml=False)

# meld3._write_html_no_encoding() also needs to be adapted
def _write_html_no_encoding(write, node, encoding, namespaces):
    # 'encoding' arg is discarded (duh)
    return meld3._write_html_no_encoding(write, node, namespaces)


def tostring(elem, format='html', encoding='utf-8'):
    """Serialize the ET.Element elem as a string with default encoding
    utf-8. Do not escape cdata or attrib values.

    If format is 'html' (the default), render empty elements as matched
    pairs (eg, <div></div> rather than <div />). If format is 'xml',
    render empty elements as singletons.

    Uses output code from the meld3 templating package (now included as
    tailoring2.meld3). Introduced Jan 2010; see #MTS-3269.

    Encoding is now a parameter; default is still utf-8. Pass
    format=None to return a unicode object instead of an encoded string.
    See #MTS-3289.
    """
    def get_output_func(format, encoding):
        if encoding is None:
            if format == 'html':
                return _write_html_no_encoding
            else:
                raise ValueError("encoding=None supported only for format=html")
        try:
            dispatch = dict(
                html=meld3._write_html,
                xml=_write_xml)
            return dispatch[format]
        except KeyError:
            raise ValueError("format '%s' is unsupported" % format)
        
    output_method = get_output_func(format, encoding)
    data = []
    output_method(data.append, elem, encoding, {})
    return ''.join(data)


def tostring_old(elem):
    """modified ET.tostring() to not escape cdata and attrib values. Otherwise
    uses ET.tostring() machinery completely.
    
    Actually implemented as a monkeypatch. ET.tostring() is restored to
    normal when this call is done, but that makes this call very much
    not threadsafe.
    
    Replaced Jan 2010 with meld3-based tostring() above. For more, see
    #MTS-3269. Ok to remove after Kaiser release (spring/summer 2010).
    """
    # monkeypatch ET to not escape entities (this allows <b>, <i>, <u>, etc formatting 
    # markup to be included inline (and escaped) in the message docs)
    old_escape_cdata, old_escape_attrib = ET._escape_cdata, ET._escape_attrib
    noop = lambda t, *args, **kwargs: t
    ET._escape_cdata = noop
    ET._escape_attrib = noop
    result = ET.tostring(elem)
    # undo monkeypatch
    ET._escape_cdata, ET._escape_attrib = old_escape_cdata, old_escape_attrib
    return result
