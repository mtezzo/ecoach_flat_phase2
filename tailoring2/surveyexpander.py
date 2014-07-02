# COPYRIGHT (c) 2008
# THE REGENTS OF THE UNIVERSITY OF MICHIGAN
# ALL RIGHTS RESERVED
#  
# PERMISSION IS GRANTED TO USE, COPY, CREATE DERIVATIVE WORKS AND REDISTRIBUTE 
# THIS SOFTWARE AND SUCH DERIVATIVE WORKS FOR NONCOMMERCIAL EDUCATION AND RESEARCH 
# PURPOSES, SO LONG AS NO FEE IS CHARGED, AND SO LONG AS THE COPYRIGHT NOTICE 
# ABOVE, THIS GRANT OF PERMISSION, AND THE DISCLAIMER BELOW APPEAR IN ALL COPIES 
# MADE; AND SO LONG AS THE NAME OF THE UNIVERSITY OF MICHIGAN IS NOT USED IN ANY 
# ADVERTISING OR PUBLICITY PERTAINING TO THE USE OR DISTRIBUTION OF THIS SOFTWARE 
# WITHOUT SPECIFIC, WRITTEN PRIOR AUTHORIZATION.
#  
# THIS SOFTWARE IS PROVIDED AS IS, WITHOUT REPRESENTATION FROM THE UNIVERSITY OF 
# MICHIGAN AS TO ITS FITNESS FOR ANY PURPOSE, AND WITHOUT WARRANTY BY THE 
# UNIVERSITY OF MICHIGAN OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT 
# LIMITATION THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
# PARTICULAR PURPOSE. THE REGENTS OF THE UNIVERSITY OF MICHIGAN SHALL NOT BE 
# LIABLE FOR ANY DAMAGES, INCLUDING SPECIAL, INDIRECT, INCIDENTAL, OR 
# CONSEQUENTIAL DAMAGES, WITH RESPECT TO ANY CLAIM ARISING OUT OF OR IN CONNECTION 
# WITH THE USE OF THE SOFTWARE, EVEN IF IT HAS BEEN OR IS HEREAFTER ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGES.
from tailoring2.util import isList
from tailoring2.dictionary import SurveyValueIterator
from tailoring2 import basetype

"""Survey docs may use an abbreviated form for some features; before
rendering to HTML, all elements should be expanded to the canonical
form.
"""

import os
import copy
import re
import ConfigParser
import sys
import itertools
import operator
from StringIO import StringIO
import logging
log = logging.getLogger(__name__)

from tailoring2.common import Elements, SourceAttributes, SurveyRenderConstants, ClassValues,\
    ProcessingAttributes, QuestionTypeValues, has_class, add_class,\
    remove_class, get_subelements, ET
from tailoring2.basetype import Basetype, IntBasetype, DatetimeBasetype,\
    StringBasetype, DecimalBasetype
from tailoring2.authorutil import isEmpty
from tailoring2.textutil import parwrap, conjunctionize, conjunctionize_list

try:
    # attempt to bring in the django translation subsystem, if it's available. 
    from django.utils.translation import string_concat, lazy, ugettext_lazy as _
except ImportError:
    # it appears that it isn't, so let's stub it out for now
    string_concat = lambda *strings: u''.join(unicode(s) for s in strings)
    _ = lambda s: unicode(s)
    lazy = lambda func, *resultclasses: func

lazy_format = lazy(lambda a, b: operator.mod(a, b), unicode)

try:
    next
except NameError:
    # Python 2.6+ has 'next()', earlier versions do not
    class __NoDefault(object): pass
    _NoDefault = __NoDefault()
    def next(iterator, default=_NoDefault):
        try:
            return iterator.next()
        except StopIteration:
            if default is not _NoDefault:
                return default
            raise

class ErrorMessages(object):
    values_only_validation = _('Please make sure your response matches %(value_errmsgs)s')
    ranges_only_validation = _('Please make sure your response is %(range_errmsgs)s')
    values_and_ranges_validation = _('Please make sure your response is %(range_errmsgs)s or matches %(value_errmsgs)s')
    min_range_fragment = _('%(min)d or more')
    max_range_fragment = _('%(max)d or less')
    full_range_fragment = _('between %(min)d and %(max)d')
    
    min_length_validation = _('Please make sure the length of your response is %(lmin)d or more')
    max_length_validation = _('Please make sure the length of your response is %(lmax)d or less')
    full_length_validation = _('Please make sure the length of your response is between %(lmin)d and %(lmax)d characters')
    
    option_validation = _('You must choose the other option if you fill in this field.')
    date_validation = _('You must choose a valid date.')
    required_validation = _('Please provide an answer to this question.')

class SurveyExpander():
#     DEFAULT_VALIDATION_CONFIG = StringIO("""
# [en]
# min_range_validation = Please make sure your response is greater than ${min}.
# max_range_validation = Please make sure your response is less than ${max}.
# full_range_validation = Please make sure your response is greater than ${min} and less than ${max}.
# min_length_validation = Please make sure the length of your response is greater than ${min} characters.
# max_length_validation = Please make sure the length of your response is less than ${max} characters.
# full_length_validation = Please make sure the length of your response is between ${min} and ${max} characters.
# option_validation = You must choose the other option if you fill in this field.
# date_validation = Please select a valid date.
# required_validation = You must provide a response for this question.
# """)
    
    def __init__(self, mtsdict):
        self.mtsdict = mtsdict
        self.hasValidation = False

        # self.validation_messages = ConfigParser.ConfigParser()
        # self.validation_messages.readfp(self.DEFAULT_VALIDATION_CONFIG)
        # self.validation_messages.read(os.path.join(os.path.dirname(__file__), 'validation.strings'))
        

    def expand(self, passed_elt):
        """"Look at all of the elements in a tree and expand them to
        their long form before translating to HTML
        """
        try:
            element = passed_elt.getroot()
        except:
            #must be an element
            element = passed_elt
                        
        method_name = "expand_%s" % (element.tag.lower())
        try:
            method = getattr(self, method_name)
            method(element)
        except AttributeError:
            log.debug("no expander for %s, leaving untouched" % element.tag)
#            subels = element.find(Elements.SUBELEMENTS_TAG)
#            if subels:
#                for subel in subels:
#                    self.expand(subel)
#            else:
            for subel in element.getchildren():
                self.expand(subel)

            pass
        except:
            raise

        return self.hasValidation

    def expand_document(self, document):
        """Sections are unchanged.
        """
        sections = document.findall(Elements.SECTION_TAG)
        for section in sections:
            self.expand(section)

    def expand_group(self, group):
        """Groups are unchanged too.
        """
        self.mark_class(group.find(Elements.SUBELEMENTS_TAG), ClassValues.GROUP_ITEM)
        subels = group.find(Elements.SUBELEMENTS_TAG)
        if subels:
            for subel in subels:
                self.expand(subel)

    def mark_class(self, tree, value):
        try:
            elements = list(tree.getroot())
        except:
            elements = list(tree.getchildren())
        
        for element in elements:
            add_class(element, value)

    def expand_question(self, question, expand_responses=True, restrictionset=None):
        """
        The completely short form has no children at all:
        <question msgid="3" characteristic="FirstName"/>
        
        This expands to:
        <question msgid="3" characteristic="FirstName">
            <subelements>
                <text>
                    <content>
                        What is your first name? (assuming the dictionary has a survey question
                    </content>
                </text>
                (No responses since this one has no values)
            </subelements>
        </question>
        """
        
        """ Get characteristic from dictionary """
        characteristicName = question.get(SourceAttributes.CHARACTERISTIC)
        characteristic = self.mtsdict.char_index.get(characteristicName)
        restrictionset = characteristic.restrictionset if characteristic is not None else restrictionset
        is_multivalued = characteristic.is_multivalued if characteristic is not None else False
        basetype = characteristic.basetype if characteristic is not None else StringBasetype
        
        """ Create or find the subelements """
        subelements = get_subelements(question)
        
        """ Convert any top level content to an item in subelements """
        toplevel_content = question.find(Elements.CONTENT_TAG)
        if toplevel_content is not None:
            if toplevel_content.text is not None:
                text = ET.Element(Elements.TEXT_TAG)
                subelements.insert(0, text)
                content = ET.Element(Elements.CONTENT_TAG)
                text.append(content)
                content.text = toplevel_content.text
                add_class(text, ClassValues.PROMPT)
                text.set(SourceAttributes.CUSTOM_TAG_ATTR, 'div')
            question.remove(toplevel_content)
            
        """ generate missing survey prompts if needed """
        """ TODO: This assume prompts are always in a text/content hierarchy. What about graphical prompts? """
        
        result = subelements.find(Elements.TEXT_TAG + '/' + Elements.CONTENT_TAG)        
        if result is None or isEmpty(result.text):
            self.create_prompt(question, characteristic)
        else:
            add_class(subelements.find(Elements.TEXT_TAG), ClassValues.PROMPT)
        
        """ Add type if needed, based on dictionary"""
        if question.get(SourceAttributes.QUESTION_TYPE) == None:
            valid_value_count = characteristic.valid_value_count() 
            if is_multivalued:
                if valid_value_count > 0:
                    question.set(SourceAttributes.QUESTION_TYPE, QuestionTypeValues.CHECKBOX)
            else:
                if basetype == DatetimeBasetype:
                    question.set(SourceAttributes.QUESTION_TYPE, QuestionTypeValues.DATE)
                elif basetype == DecimalBasetype:
                    question.set(SourceAttributes.QUESTION_TYPE, QuestionTypeValues.FILLIN)                    
                elif restrictionset is not None and valid_value_count > 0 and valid_value_count <= 50:                           
                    if valid_value_count > 20:
                        question.set(SourceAttributes.QUESTION_TYPE, QuestionTypeValues.POPUP)
                    else:
                        question.set(SourceAttributes.QUESTION_TYPE, QuestionTypeValues.RADIO)
                else:
                    question.set(SourceAttributes.QUESTION_TYPE, QuestionTypeValues.FILLIN)
                    
        """ Set width for text fields if none is provided """
        if question.get(SourceAttributes.QUESTION_TYPE) == QuestionTypeValues.FILLIN:
            size = question.get(SourceAttributes.SIZE)
            if size is None:
                maxsize = 0
                minsize = 1
                for range_restriction in characteristic.restrictionset.ranges:
                    if basetype == IntBasetype:
                        max_length = len(str(int(range_restriction.max)))
                    else:
                        max_length = len(str(range_restriction.max))
                        
                    if range_restriction.is_unbounded_upper():
                        max_length = SurveyRenderConstants.WIDTH_FILLIN
                        
                    maxsize = max(max_length, maxsize)
                for length_restriction in characteristic.restrictionset.lengths:
                    maxsize = max(int(length_restriction.max), maxsize)
                if maxsize > 0:
                    question.set(SourceAttributes.SIZE, str(max(minsize, maxsize)))
                else:
                    question.set(SourceAttributes.SIZE, str(SurveyRenderConstants.WIDTH_FILLIN))
            
        """ Add responses as needed """
        question_type = question.get(SourceAttributes.QUESTION_TYPE)
        if expand_responses and (question_type == QuestionTypeValues.CHECKBOX or \
                                 question_type == QuestionTypeValues.RADIO or \
                                 question_type == QuestionTypeValues.SCALE or \
                                 question_type == QuestionTypeValues.POPUP):
            self.create_responses(question, restrictionset, basetype.pytype)
        
        """ if there are no existing validators, add them """
        if subelements.find(Elements.VALIDATE_TAG) is None:
            self.create_validators(question, characteristic)
            
    def expand_matrix(self, matrix):
        """
        The completely short form has only questions as children:
        <matrix msgid="3" valueset="BarrierRisk">
            <subelements>
                <question characteristic="BarBarrierRisk" if="'Bar' in Barriers"/>
                <question characteristic="PartyBarrierRisk if='Party' in Barriers"/>
            </subelements>
        </matrix>

        This expands to:
        <martrix msgid="3" valueset="BarrierRisk">
            <subelements>
                <question characteristic="BarBarrierRisk" if="'Bar' in Barriers">
                    <content>
                        at the bar
                    </content>
                </question>
                <question characteristic="PartyBarrierRisk if='Party' in Barriers">
                    <content>
                        at parties
                    </content>
                </question>
                <response value="1"/>
                <response value="2"/>
                <response value="3"/>
                <response value="4"/>
                <response value="5"/>
                <response value="6"/>
                <response value="7"/>
            </subelements>
        </question>
        """
        
        # Get valueset from dictionary
        valuesetName = matrix.get(SourceAttributes.MATRIX_VALUESET)
        valueset = self.mtsdict.restriction_index.get(valuesetName) if valuesetName is not None else None
        

        """ Create or find the subelements """
        subelements = get_subelements(matrix)

        pytype = StringBasetype.pytype
        """ Expand questions """
        for question in subelements.findall(Elements.QUESTION_TAG):
            self.expand_question(question, False, valueset)
            characteristicName = question.get(SourceAttributes.CHARACTERISTIC)
            characteristic = self.mtsdict.char_index.get(characteristicName)
            basetype = characteristic.basetype if characteristic is not None else StringBasetype
            pytype = basetype.pytype
        
        matrix_type = matrix.get(SourceAttributes.QUESTION_TYPE)
        if matrix_type is None:
            matrix.set(SourceAttributes.QUESTION_TYPE, QuestionTypeValues.RADIO)

        """ Expand responses """
        self.create_responses(matrix, valueset, pytype)
        
    def expand_validate(self, validate):
        self.hasValidation = True
        validation_cause = validate.get(SourceAttributes.IF)
        validate.set(ProcessingAttributes.CAUSE, validation_cause)
    
    def expand_goto(self, goto):
        return
    
    def expand_comment(self, comment):
        return
    
    def create_prompt(self, question, characteristic):
        if characteristic is not None:
            prompt_contents = characteristic.question
        # This is the case where the user has put a characteristic in the question but has not put it in the dictionary
        else:
            prompt_contents = question.get(SourceAttributes.CHARACTERISTIC)
        
        if prompt_contents is not None:
            subelements = get_subelements(question)
                    
            text = ET.Element(Elements.TEXT_TAG)
            subelements.insert(0, text)
            add_class(text, ClassValues.PROMPT)
            # force tailoring engine to render as a div
            text.set(SourceAttributes.CUSTOM_TAG_ATTR, 'div')
            
            contents = ET.Element(Elements.CONTENT_TAG)
            text.append(contents)
            contents.text = prompt_contents
                          
    def check_response_content(self, response, value_text):
        subelements = get_subelements(response)
        subcontents = next((ce for se in subelements
                               for ce in se.findall(Elements.CONTENT_TAG)), None)
        if subcontents is not None:
            # there exists something within this response that at least 
            # pretends to produce content, so we shouldn't be doing things.
            return
        response_content = response.find(Elements.CONTENT_TAG)
        if response_content is None:
            response_content = ET.Element(Elements.CONTENT_TAG)
            response.append(response_content)
        
        if response_content.text is None:
            response_content.text = value_text
                
    def create_responses(self, question, restrictionset, pytype):
        """ Get characteristic from dictionary """
#        characteristicName = question.get(SourceAttributes.CHARACTERISTIC)
#        characteristic = self.mtsdict.char_index.get(characteristicName)
#        restrictionset = characteristic.restrictionset if characteristic is not None else None
        pytype = pytype if pytype is not None else StringBasetype.pytype     
        """ Create or find the subelements """
        subelements = get_subelements(question)

        if restrictionset is not None:
            iter = SurveyValueIterator(restrictionset, pytype)  
            for value in iter:
                response_text = unicode(value.get('response_text')) if value.get('response_text') is not None else '' 
                response_value = unicode(value.get('response_value')) if value.get('response_value') is not None else '' 
                # is there a response for this value already?
                response = next((response for response in subelements.findall(Elements.RESPONSE_TAG) \
                                 if response.get(SourceAttributes.RESPONSE_VALUE) == response_value), None)
                if response is None:
                    response = ET.Element(Elements.RESPONSE_TAG)
                    subelements.append(response)                    
                    response.set(SourceAttributes.RESPONSE_VALUE, response_value)

                    response_content = ET.Element(Elements.CONTENT_TAG)
                    response.append(response_content)
                    response_content.text = response_text if not isEmpty(response_text) else response_value
                else:
                    # Make sure the content of the response is good
                    self.check_response_content(response, response_text if not isEmpty(response_text) else response_value)                
        
            #transform content rows into text rows
            for response in subelements.findall(Elements.RESPONSE_TAG):
                rsubelements = get_subelements(response)
                existing_response_content = response.find(Elements.CONTENT_TAG)
                if existing_response_content is not None:
                    new_text = ET.Element(Elements.TEXT_TAG)
                    rsubelements.insert(0, new_text)
                    content = ET.SubElement(new_text, Elements.CONTENT_TAG)
                    content.text = existing_response_content.text
                    response.remove(existing_response_content)        
    
    def create_validators(self, question, characteristic):
        if characteristic is not None:
            subelements = get_subelements(question)
            characteristicName = question.get(SourceAttributes.CHARACTERISTIC)
            question_type = question.get(SourceAttributes.QUESTION_TYPE)
            restrictset = characteristic.restrictionset
            validator_created = False
            
            if question_type == QuestionTypeValues.FILLIN and characteristic.basetype == IntBasetype:          
                self.create_numeric_validator(question, characteristic)
                
            if question_type == QuestionTypeValues.FILLIN:          
                self.create_length_validator(question, characteristic)                
                                
            # Handling Other
            other_elements = subelements.findall(Elements.OTHER_TAG)
            for other_element in other_elements:
                other_characteristic = other_element.get(SourceAttributes.CHARACTERISTIC)
                other_value = other_element.get(SourceAttributes.RESPONSE_VALUE)
                
                if other_characteristic is not None and other_value is not None:
                    # validator should be selected (True) when all of the following are true:
                    #   - Other is not selected
                    #   - OtherFillIn is not empty
                    # This is due to the requirement that the other text be specified.
                    # The logic is therefore:
                    #   otheroption not in Characteristic and not isEmpty(OtherFillIn)
                    validator = ET.Element(Elements.VALIDATE_TAG)
                    self.hasValidation = True
                    validator_created = True
                    subelements.append(validator)
                    if characteristic.is_multivalued:
                        comparitor = 'not in'
                        typed_other_value = characteristic.basetype_normalize([other_value])[0]
                    else:
                        comparitor = '!='
                        typed_other_value = characteristic.basetype_normalize(other_value)
                    if_attribute = "%(typed_other_value)r %(comparitor)s %(characteristicName)s and not isEmpty(%(other_characteristic)s)" % locals()
                    validator.set(SourceAttributes.IF, if_attribute)
                    validator_content = ET.Element(Elements.CONTENT_TAG)
                    validator.append(validator_content)
                    validator_content.text = ErrorMessages.option_validation
                    if has_class(question, ClassValues.GROUP_ITEM):
                        add_class(validator, ClassValues.GROUP_ITEM)
            
            if characteristic.is_required:
                validator = ET.Element(Elements.VALIDATE_TAG)
                self.hasValidation = True
                validator_created = True
                subelements.append(validator)
                if not characteristic.is_multivalued:
                    if_attribute = "isEmpty(" + characteristicName + ")"
                else:
                    if_attribute = characteristicName + " == None or len(" + characteristicName + ") == 0"
                validator.set(SourceAttributes.IF, if_attribute)
                validator_content = ET.Element(Elements.CONTENT_TAG)
                validator.append(validator_content)
                validator_content.text = ErrorMessages.required_validation
                
    def create_numeric_validator(self, question, characteristic):
        restrictset = characteristic.restrictionset
        if restrictset:
            if len(restrictset.ranges) > 0 or len(restrictset.values)>0:
                self.hasValidation = True
                subelements = get_subelements(question)
                validator = ET.Element(Elements.VALIDATE_TAG)
                subelements.append(validator)
                
                if_attribute = restrictset.expression(characteristic.name, characteristic.basetype.pytype, False)
                if characteristic.is_required:
                    if_attribute = 'not %s' % parwrap(if_attribute)
                else:
                    if_attribute = 'not (isEmpty(%s) or %s)' % (characteristic.name, parwrap(if_attribute))
                validator.set(SourceAttributes.IF, if_attribute)
                validator_content = ET.Element(Elements.CONTENT_TAG)
                validator.append(validator_content)
                                           
                value_errors = ''
                range_errors = ''
                
                valid_values = conjunctionize(_('or'), [v.symbol for v in restrictset.values], False)
                
                range_msgs = []
                
                for range in restrictset.ranges:
                    d = dict(min=range.min, max=range.max)
                    hasmin = range.min != (-sys.maxint - 1)
                    hasmax = range.max != sys.maxint
                    if hasmax and not hasmin:
                        range_msgs.append(lazy_format(ErrorMessages.max_range_fragment, d))
                    elif not hasmax and hasmin:
                        range_msgs.append(lazy_format(ErrorMessages.min_range_fragment, d))
                    else:
                        range_msgs.append(lazy_format(ErrorMessages.full_range_fragment, d))    
                
                range_msgs = string_concat(*conjunctionize_list(_('or'), range_msgs, False))
                
                msgs = dict(value_errmsgs=valid_values, range_errmsgs=range_msgs)
                
                if len(valid_values) == 0:
                    error = lazy_format(ErrorMessages.ranges_only_validation, msgs)
                elif len(range_msgs) == 0:
                    error = lazy_format(ErrorMessages.values_only_validation, msgs)
                else:
                    error = lazy_format(ErrorMessages.values_and_ranges_validation, msgs)
                
                validator_content.text = error
                if has_class(question, ClassValues.GROUP_ITEM):
                    add_class(validator, ClassValues.GROUP_ITEM)
                    
    def create_length_validator(self, question, characteristic):
        restrictset = characteristic.restrictionset
        if restrictset and len(restrictset.lengths) > 0:     
            self.hasValidation = True
                                    
            lmin = 0
            lmax = 0                                
            for length in restrictset.lengths:
                try:
                    new_max = int(length.max)
                    if new_max > lmax:
                        lmax = new_max
                    new_min = int(length.min)    
                    if new_min < lmin:
                        lmin = new_min                                
                except:
                    pass    
                    
            lmin = int(lmin)
            lmax = int(lmax)
            ld = dict(lmin=lmin, lmax=lmax)
            hasmin = lmin != (-sys.maxint - 1)     
            hasmax = lmax != sys.maxint                                   
            if hasmax and not hasmin:
                error = lazy_format(ErrorMessages.max_length_validation, ld)
            elif not hasmax and hasmin:
                error = lazy_format(ErrorMessages.min_length_validation, ld)
            else:
                error = lazy_format(ErrorMessages.full_length_validation, ld)
            
            subelements = get_subelements(question)
            validator = ET.Element(Elements.VALIDATE_TAG)
            subelements.append(validator)
            
            if_attribute = 'not (%s <= len(unicode(%s)) <= %s)' % (str(lmin), characteristic.name, str(lmax))
            validator.set(SourceAttributes.IF, if_attribute)
            validator_content = ET.Element(Elements.CONTENT_TAG)
            validator.append(validator_content)                
            validator_content.text = error
            if has_class(question, ClassValues.GROUP_ITEM):
                add_class(validator, ClassValues.GROUP_ITEM)           
                   
