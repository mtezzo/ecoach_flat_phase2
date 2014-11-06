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

"""Factory functions for creating different types of message documents, whether
classic tailored-message docs or survey docs.

Each factory function takes a file path and possibly other parameters (depending on
the document type) and returns an ET.ElementTree instance.
"""

from tailoring2.common import ET, SourceAttributes, ProcessingAttributes
from tailoring2.surveyexpander import SurveyExpander
from tailoring2.translations import i18n_survey_tree


def MessageDocument(filepath):
    """Given the path to a message document, return an ET.ElementTree
    instance representing the message doc.
    """
    return ET.parse(filepath)


def SurveyDocument(filepath, mtsdict):
    """Given the path to a survey document and an mtsdict instance,
    return an expanded ET.ElementTree instance representing
    the survey.
    """
    tree = ET.parse(filepath)
    survey_expander = SurveyExpander(mtsdict)
    survey_expander.expand(tree)
    i18n_survey_tree(tree, mtsdict)
    return tree


def isSurveyDocument(doc):
    if doc:
        return len(doc.findall("//question"))>0


def decorateNoSelection(doc):
    if doc:
        for elem in doc.getiterator('question'):
            if elem.get(SourceAttributes.IF):
                logic = elem.get(SourceAttributes.IF)                    
                if logic is not None:
                    logic_element = ET.Element('div')
                    logic_element.set(ProcessingAttributes.CLASS, 'note')
                    logic_element.text = logic.replace('<', '&lt;')
                    elem.insert(-1, logic_element)
                del elem.attrib[SourceAttributes.IF]
            for child in elem.getiterator():
                if child.get(SourceAttributes.IF):
                    logic = child.get(SourceAttributes.IF)                    
                    if logic is not None:
                        logic_element = ET.Element('div')
                        logic_element.set(ProcessingAttributes.CLASS, 'note')
                        logic_element.text = logic.replace('<', '&lt;')
                        child.insert(-1, logic_element)                        
                    del child.attrib[SourceAttributes.IF]


def section_index(message, section_tag="section", index_attr="name"):
    """return a dictionary of name->section for every section element in
    the message
    """
    return dict((section.get(index_attr), section) for section in message.getiterator(section_tag))


def msgidmunge(elem, tail, attr="msgid"):
    """walk through elem, modifying any msgid attributes by appending 'tail'
    """
    msgid = elem.get(attr)
    if msgid:
        elem.set(attr, "%s%s" % (msgid, tail))
    for child in elem:
        msgidmunge(child, tail)

