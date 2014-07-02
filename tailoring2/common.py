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

"""platform-sensitive conditional imports, plus some constants, errors,
and functions available to all other tailoring modules
"""

##
# conditional imports
#
# Certain names need to be handled differently depending on whether we're
# in CPython, Jython, or IronPython. This section sets up and imports
# those names conditionally in one place so all a caller has to do is
# 'import' the name from this module.

# sets aren't built in for Jython 2.2 and older
try:
    set
except NameError:
    from sets import Set as set
set = set  # export the name

# json/simplejson isn't built-in for Jython 2.5 but is for CPython 2.6+
try:
    import json
except ImportError:
    import simplejson as json

import sys
import logging

##
# monkey-patch for a faster pyexpat than delivered in jython2.5

#   IJ note: do we still need this under Jython 2.5.1??
#   TODO: benchmark with fastexpat and without

# if sys.platform.startswith('java'):
#     major, minor, micro, releaselevel, serial = sys.version_info
#     if (major, minor, micro, releaselevel) == (2, 5, 0, 'beta'):
#         try:
#             import fastexpat
#             sys.modules['xml.parsers.expat'] = fastexpat
#             import xml.parsers
#             xml.parsers.expat = fastexpat
#             sys.modules['expat'] = fastexpat
#             del fastexpat
#         except ImportError:
#             logging.warning("Failed to Monkey-patch FastExpat in Jython 2.5.0")

##
# Each of the different platforms we hope to run under (CPython, Jython,
# IronPython) has a different xml-parse exception class. Sniff the
# platform and set a module-level var so we know what to look for.

try:
    # cpython or jython25
    import xml.parsers.expat
    XMLParseExceptionClass = xml.parsers.expat.ExpatError
except ImportError:
    if 'java' in sys.platform:
        # jython22
        import org.xml.sax.SAXParseException
        XMLParseExceptionClass = org.xml.sax.SAXParseException
    elif 'cli' in sys.platform:
        # ironpython
        import pyexpat
        XMLParseExceptionClass = pyexpat.error
    else:
        raise RuntimeError( "xml parser error class unknown!" )


# once-and-for-all ET omnibus import
try:
    # cpython >= 2.5, jython >= 2.5, ironpython >= 2 (I think)
    import xml.etree.ElementTree as ET
except ImportError:
    # runtimes without etree built-in (ie, anything targeting cpython <2.5,
    # like Jython 2.2 or IronPython 1.x) should install the ElementTree
    # package under the standard effbot package name, as below:
    import elementtree.ElementTree as ET



#
# end conditional imports
##


# ------------------------------------------------------------
# xml format information: element and attribute names



class Elements:
    """element tag names"""
    # containers
    SECTION_TAG = 'section'
    BLOCK_TAG = 'block'
    LIST_TAG = 'list'
    LISTITEM_TAG = 'listitem'
    SELECT_TAG = 'select'

    # non-containers
    TEXT_TAG = 'text'
    PARAGRAPH_TAG = 'paragraph'
    HEADING_TAG = 'heading'
    GRAPHIC_TAG = 'graphic'
    COMMENT_TAG = 'comment'
    NOTE_TAG = 'note'

    # not commands themselved, but contained within commands
    SUBELEMENTS_TAG = 'subelements'
    CONTENT_TAG = 'content'

    # survey containers
    QUESTION_TAG = 'question'
    RESPONSE_TAG = 'response'
    OTHER_TAG = 'other'
    VALIDATE_TAG = 'validate'
    MATRIX_TAG = 'matrix'
    GROUP_TAG = 'group'

    # survey non-containers
    CODE_TAG = 'code'
    GOTO_TAG = 'goto'

    # tags that have an HTML_ prefix to prevent processing by tge tailoring machinery
    HTML_SELECT_TAG = 'html_select'

    CONTAINER_ELEMENTS = set([BLOCK_TAG, SELECT_TAG, SECTION_TAG, LISTITEM_TAG, LIST_TAG, GROUP_TAG])
    LIST_ELEMENTS = set([LISTITEM_TAG, LIST_TAG])

    # be able to ignore stuff like <subelements>, <content>
    CONTENT_PRODUCING_ELEMENTS = set( [SECTION_TAG, BLOCK_TAG, LIST_TAG, LISTITEM_TAG, SELECT_TAG,
            TEXT_TAG, PARAGRAPH_TAG, HEADING_TAG, GRAPHIC_TAG, COMMENT_TAG, QUESTION_TAG, RESPONSE_TAG, OTHER_TAG,
            VALIDATE_TAG, MATRIX_TAG, GROUP_TAG] )

    # stuff that only contains content, not other elements
    LEAF_ELEMENTS = set( [TEXT_TAG, PARAGRAPH_TAG,
            HEADING_TAG, GRAPHIC_TAG, COMMENT_TAG, CODE_TAG, GOTO_TAG] )

class SurveyRenderConstants:
    WIDTH_MATRIX_PROMPT = 20
    WIDTH_NARROW_MATRIX_PROMPT = 40
    WIDTH_FILLIN = 20

    ENGLISH_MONTHS_LONG = ['January', 'February', 'March', 'April', 'May', 'June',
                               'July', 'August', 'September', 'October', 'November', 'December']

class SourceAttributes:
    """message source attributes: present in original source"""

    # name of attribute containing eligibility expression
    IF = 'if'

    # optional attribute to specify a different ordering method like 'random' (default is 'sequential')
    ORDERBY = 'orderby'

    # max number of element's children to allow -- present in source
    LIMIT = "limit"

    # attribute for assigning custom tags
    CUSTOM_TAG_ATTR = 'tag'

    # attribute for setting characteristic of a question
    CHARACTERISTIC = 'characteristic'

    # attribute for setting type of a question
    QUESTION_TYPE = 'questiontype'

    # attribute for setting valueset of a matrix
    MATRIX_VALUESET = 'valueset'

    # attribute for setting value of a response
    RESPONSE_VALUE = 'value'

    # optional attribute for setting the size of the input field
    SIZE = 'size'

    # attribute for directing survey progression to another named segment
    GOTO = 'goto'

    # attribute for turning on and off the header row in a matrix table
    COLUMN_HEADER = 'columnheader'

    # attribute for setting the position of a label in a matrix table cell
    VALUE_LABEL_LOCATION = 'valuelabellocation'

class ProcessingAttributes:
    """message processing attributes: added by processing pipeline"""

    # set true/false on each command during selection processing
    SELECTED = 'selected'

    # set to a counting number on ordered commands during selection/order processing
    INDEX = 'index'

    # set true/false on each command under a 'select' during selection/limit processing
    LIMITED = "limited"

    # cause of a validation
    CAUSE = "cause"

    # class of a rendered item
    CLASS = "class"

    # survey item name prefix
    SURVEY_ITEM_PREFIX = "survey_"

class QuestionTypeValues:

    CHECKBOX = 'checkbox'
    RADIO = 'radio'
    SCALE = 'scale'
    FILLIN = 'fillin'
    DATE = 'date'
    POPUP = 'popup'

class ClassValues:

    QUESTION = 'survey_question'
    VALIDATE = 'survey_error'
    PROMPT = 'survey_prompt'
    RESPONSE = 'survey_response'
    RESPONSES = 'survey_responses'
    MATRIX = 'survey_matrix'
    MATRIX_ROW = 'survey_matrix_row'
    MATRIX_ROW0 = MATRIX_ROW + '0'
    GROUP = 'survey_question_group'
    GROUP_ITEM = 'survey_question_group_item'

# ------------------------------------------------------------

class ProcessingError( Exception ):
    def __init__( self, err, phase, location, message = '' ):
        """@param err: the underlying exception instance
        @param phase: the instance of the Phase the error happened in
        @param location: the element the error happened on
        @param message: other relevant information: will be populated by 'err'
        """
        Exception.__init__( self, message )
        self.err = err
        self.phase = phase
        self.location = location

    def locmsg( self ):
        msgid = self.location.get( 'msgid' )
        if msgid:
            return "<%s msgid=%s>" % ( self.location.tag, msgid )
        else:
            return "<%s>" % self.location.tag

    def __repr__( self ):
        try:
            args = self.err.args
        except AttributeError:
            args = ''
        return "<%s: %s in '%s' at %s>" % \
                ( self.__class__.__name__, self.err, self.location.get( 'if' ), self.locmsg() ) #, args)


class HTMLParsingError( ProcessingError ):
    """raised when escaped HTML in a message doc is revealed upon
    unescape to be bogus
    """
    pass


class SubjectError( Exception ):
    """Generic error that happened sometime during subject generation.
    Use this if there isn't a more specific error.
    """
    def __init__( self, err, message ):
        Exception.__init__( self, message )
        self.err = err


class DeriveError( Exception ):
    """wrap an error that happened in derived characteristic evaluation in some
    useful context info.
    """
    def __init__( self, err, chardef, source, mtsdict, message = '' ):
        """@param err: the underlying exception instance
        @param chardef: the CharacteristicDefinition object where the error occurred
        @param source: the DataSource object where the error occurred
        @param mtsdict: the MTSDictionary object containing the offending chardef
        @param message: other relevant information; will be populated by 'err'
        """
        Exception.__init__( self, message )
        self.err = err
        self.chardef = chardef
        self.mtsdict = mtsdict
        self.source = source

    def __repr__( self ):
        try:
            args = self.err.args
        except AttributeError:
            args = ''
        return "<DeriveError in %s.%s: %s: %s>" % \
            ( self.source.name, self.chardef.name, type( self.err ).__name__, self.err )

    def __str__( self ):
        return self.__repr__()

def get_subelements( question ):
    subelements = question.find( Elements.SUBELEMENTS_TAG )
    if subelements is None:
        subelements = ET.Element( Elements.SUBELEMENTS_TAG )
        question.append( subelements )

    return subelements

def add_class( element, classname, ashead = False ):
    if classname is None:
        return
    if has_class( element, classname ):
        return # already there, mate.
    classes = element.get( ProcessingAttributes.CLASS, '' ).split()
    if ashead:
        classes.insert( 0, classname )
    else:
        classes.append( classname )
    element.set( ProcessingAttributes.CLASS, ' '.join( classes ) )

def remove_class( element, classname ):
    classes = element.get( ProcessingAttributes.CLASS, '' ).split()
    classes.remove( classname )
    element.set( ProcessingAttributes.CLASS, ' '.join( classes ) )

def has_class( element, classname ):
    return classname in element.get( ProcessingAttributes.CLASS, '' ).split()



##
# experiment with exporting different implementations of deepcopy_element


def deepcopy_element(elem):
    oldel = elem

    def generate_elem(oldel):
        newel = ET.Element(oldel.tag)
        if oldel.attrib:
            for key, val in oldel.items():
                newel.set(key, val)

        if oldel.text is not None:
            newel.text = oldel.text
        if oldel.tail is not None:
            newel.tail = oldel.tail
        for e in oldel:
            newel.append(generate_elem(e))

        return newel

    elcopy = generate_elem(oldel)
    return elcopy

# alias
# copy_ET = deepcopy_element


# 1. standard deepcopy
# import copy
# deepcopy_element = copy.deepcopy

# 2. specialized for ET
deepcopy_element = deepcopy_element

# 3.
# ...



def deepcopy_elementtree(elemtree):
    eltree = elemtree.getroot()
    eltreecopy = deepcopy_element(eltree)
    return ET.ElementTree(eltreecopy)
