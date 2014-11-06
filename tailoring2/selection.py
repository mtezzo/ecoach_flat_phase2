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

"""Given a parsed message document, select the appropriate messages for
the subject's data.
"""
import sys
import optparse
import copy
import random
import itertools
from pprint import pprint
import logging
log = logging.getLogger(__name__)

from common import *
from tailoring2.util import string2bool, bool2attrib

# ------------------------------------------------------------
# utils

def children_in_order(elem):
    """return elem's children in an ordered list. Order is applied
    by using the 'sortedposition' int attribute of each child.
    
    Assume the presence of a container child, <subelements>, and
    evaluate the children of that container instead of elem's direct
    children.
    """
    children = [(int(child.get(ProcessingAttributes.INDEX, '0')), child)
            for child in elem.find(Elements.SUBELEMENTS_TAG).getchildren()]
    children.sort()
    return [child for i, child in children]

# ------------------------------------------------------------
# phases

def select(messages, evalcontext=None):
    """return modified copy of messages
    @param messages: an ET.Element, a tailored message fragment or document
    @param evalcontext: a dictionary to be used as a namespace for expression
        evaluation. It is a required parameter for select.
    """
    log.debug(">>>select")
#    messages = copy_ET(messages)
    messages = deepcopy_element(messages)    
    errors = []
    assert evalcontext is not None, "must pass evalcontext"
    def select_elem(elem, errors):
        log.debug(">>>select.select_elem(%s)" % elem)
        selected = True
        if errors is None:
            errors = []
        if elem.tag in Elements.CONTENT_PRODUCING_ELEMENTS:
            log.debug("is content producing elem, checking for if presence")
            if_attr = elem.get(SourceAttributes.IF)
            if if_attr:
                # issue 3882 -- CPython and Jython need to treat \r and \n the same way
                # (that is, as newlines)
                if_attr = if_attr.replace('\r', '\n')
                log.debug("evaluating if attr: %s" % if_attr)
                try:
                    selected = eval(if_attr, globals(), evalcontext)
                except Exception, err:
                    log.warn("error evaluating '%s': %s" % (if_attr, err))
                    selected = False
                    proc_err = ProcessingError(err, 'select', elem,
                            message="%s in if='%s'" % (err, if_attr))
                    errors.append(proc_err)
            else:
                log.debug("no if attr")
            log.debug("%s selected? %s" % (elem, selected))
            elem.set(ProcessingAttributes.SELECTED, bool2attrib(selected))
        for child in elem:
            select_elem(child, errors)
        return elem, errors
    return select_elem(messages, errors)


# Note: a no-op stub has been inserted here because the 'default' command
# is not documented or used (as of 7/3/08). May return in post-workshop
# release.
#
def default(messages, evalcontext=None): return (messages, [])
        
   
def order(messages, evalcontext=None):
    """evalcontext is ignored"""
    log.debug(">>>order")
    messages = deepcopy_element(messages)
    errors = []
    def get_order_policy(orderby_str):
        return eval('orderby_%s' % orderby_str, globals(), locals())    
    # both 'select' and 'list' containers can be ordered
    for parent_elem in itertools.chain(
            messages.getiterator(Elements.SELECT_TAG), messages.getiterator(Elements.LIST_TAG)):
        try:
            orderby_method = get_order_policy(
                    parent_elem.get(SourceAttributes.ORDERBY, 'sequential'))
            orderby_method(parent_elem)
        except Exception, err:
            errors.append(ProcessingError(err, 'order', parent_elem))
    return messages, errors


def orderby_sequential(parent_elem):
    for i, child in enumerate(parent_elem.find(Elements.SUBELEMENTS_TAG).getchildren()):
        child.set(ProcessingAttributes.INDEX, unicode(i+1))

        
def orderby_random(parent_elem):
    children = list(parent_elem.find(Elements.SUBELEMENTS_TAG).getchildren())
    random.shuffle(children)
    for i, child in enumerate(children):
        child.set(ProcessingAttributes.INDEX, unicode(i+1))


def limit(messages, evalcontext=None):
    log.debug(">>>limit")
    messages = deepcopy_element(messages)
#    messages = copy_ET(messages)    
    errors = []
    # both 'select' and 'list' containers can be limited
    for select_elem in itertools.chain(
            messages.getiterator(Elements.SELECT_TAG), messages.getiterator(Elements.LIST_TAG)):
        try:
            children = children_in_order(select_elem)
            limit = int(select_elem.get(SourceAttributes.LIMIT, sys.maxint))
            count = 0
            for child in children:
                if count >= limit:
                    child.set(ProcessingAttributes.LIMITED, 'true')
                else:
                    child.set(ProcessingAttributes.LIMITED, 'false')
                    child_is_selected = string2bool(child.get(ProcessingAttributes.SELECTED), 'true')
                    if child_is_selected:
                        count += 1
        except Exception, err:
            errors.append(ProcessingError(err, 'limit', select_elem))
    return messages, errors
    

# ------------------------------------------------------------

    
    
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = optparse.OptionParser()
    # add options here
    # ...
    opts, args = parser.parse_args(argv)
    
    # dummy run-through
    import lxml.etree as ET
    from subject import Subject
    logging.basicConfig()
#     log.setLevel(logging.DEBUG)
    
    # noisy error callback
    def raise_err(err):
        raise err.err
        
    subject = Subject.forpath('source/Case2.txt')
    errors = []
    messages = ET.parse(args[0]).getroot()
    messages_savedcopy = deepcopy_element(messages)
    
    # TODO: following is out of date
#     pipeline = SelectionPipeline(subject, errors)
#     processed_messages = pipeline(messages)

    if errors:
        print "Errors:"
        pprint(errors)
        return 1
    print ET.tostring(processed_messages)
    
    # TEMP sanity check
    from tailoring.elementutil import normalize
    def compare(a, b):
        # normalize and compare serializations
        normalize(a)
        normalize(b)
        return ET.tostring(a) == ET.tostring(b)
    assert compare(messages, messages_savedcopy)
    assert not compare(messages, processed_messages)

if __name__ == '__main__':
    sys.exit(main())
