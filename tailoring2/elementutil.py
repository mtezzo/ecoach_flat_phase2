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

"""Helper functions for elementtree Element objects.

for more, see the effbot's collections here:
    http://effbot.org/zone/element-lib.htm

and here:
    http://effbot.org/zone/element-bits-and-pieces.htm

"""

from __future__ import generators

import string
import unittest
import re
import copy
import urlparse
import logging
log = logging.getLogger(__name__)

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
from tailoring2.common import set, ET
from tailoring2.translations import string_concat
ElementTree, XML, Element, tostring = ET.ElementTree, ET.XML, ET.Element, ET.tostring

##
# constants and globals

# xhtml namespace -- tidy tree builder includes this NS in its elements,
# and we usually have to remove the NS prefixes
XHTML_NS = "{http://www.w3.org/1999/xhtml}"
    
##
# elementtree helper funcs

def removeNamespacesFromTree(aTree, ns_prefix=XHTML_NS):
    """modify aTree to remove all namespace prefixes in its element tags"""
    for elem in aTree.getiterator():
        if elem.tag.startswith(ns_prefix):
            elem.tag = elem.tag[len(ns_prefix):]


def firstTableForTree(tree):
    """Find the first <table> element in the given tree [convenience]."""
    return tree.getroot().find('.//table')


def rowsForTable(aTableElement):
    """given a <table> element, extract into a list of rows; each row is
    a list of <td> elements
    """
    if aTableElement.find('tbody'):
        trList = aTableElement.find('tbody').findall('tr')
    else:
        trList = aTableElement.findall('tr')
    return [row.findall('td') for row in trList]
    

def extractedText(element, depth=0):
    """extract all the text from an element and its children, removing tags -- return
    a unicode object
    
    The parameter 'depth' should not be set by the caller -- it's used by internal,
    recursive calls to exclude the outermost element's tail, which properly speaking
    belongs to the original element's parent.
    """
#    log.debug('extracting text from "%s"' % elementRepr(element))
    result = u""
    if element.text:
        result = unicode(element.text)    
    result += u"".join(
            [extractedText(childElem, depth+1) for childElem in element.getchildren()])
    if element.tail and depth > 0:
        result += unicode(element.tail)
    return result


def tagRepr(element):
    """return text representation of the tag for the given element, eg:
            <b>yack</b>  --> "<b>"
            <a href="http://www.google.com">link</a>  -->  '<a href="http://www.google.com">'
    """
    if element.attrib:
        attrib_string = u" ".join(['%s="%s"' % (key, val) for key, val in element.attrib.items()])
        return u'<%s %s>' % (element.tag, attrib_string)
    else:
        return u'<%s>' % element.tag
    
    
def extractedXMLText(element, depth=0):
    """like extracted text except leaves the xml tags intact"""
    log.debug('extracting text from "%s" (depth %i)' % (ET.tostring(element), depth))

    # catch empty elements like <br />
    if not element.text and not element.getchildren():
        return ET.tostring(element)

    result = []
    if depth > 0:
        log.debug("adding begin-tag: <%s>" % element.tag)
        result.append(tagRepr(element))
    if element.text:
        result.append(unicode(element.text))
    result.append(u"".join(
            [extractedXMLText(childElem, depth+1) for childElem in element.getchildren()]))
    if depth > 0:
        log.debug("adding end-tag: </%s>" % element.tag)
        result.append(unicode("</%s>" % element.tag))
    if element.tail and depth > 0:
        result.append(unicode(element.tail))
    return u"".join(result)


def appendText(e, text):
    """append text to the given element"""
    if not text:
        return
    if not e.getchildren():
        if not e.text:
            e.text = ''
        e.text = string_concat(e.text, text)
    else:
        # append to tail of last child
#        print e.getchildren()
        lastchild = e.getchildren()[-1]
        if not lastchild.tail:
            lastchild.tail = ''
        lastchild.tail += text

def appendElement(e1, e2):
    """append contents of e2 to e1 (not the same as appending e2 as a new child of e1)"""
    appendText(e1, e2.text)
    for c in e2.getchildren():
        e1.append(c)
    appendText(e1, e2.tail)


def stringConcat(*strings):
    is_string = lambda s: isinstance(s, basestring)
    if all(is_string(s) for s in strings):
        return u''.join(strings)
    return string_concat(*strings)

# Removing elements

# --------------------------------------------------------------------
# functions deprecated since move to Mozilla Composer from Word HTML

def unwrap_p(p_container):
    """given <td><p>Hello, <b>world!</b></p></td>,
    extract the content of the <p>. Return a modified copy
    of the p_container element.
    
    Returns an unchanged copy of p_container unchanged if it has no <p> element
    to unwrap.
    
    Deprecated since move to Mozilla Composer.
    """
    p_container = copy.copy(p_container)
    
    if p_container.text:
        # shouldn't have anything between the container and the first element
        # except whitespace
        withoutNL = p_container.text.lstrip()
        if withoutNL:
            return p_container
    
    if len(p_container.getchildren()) < 1:
        # has to have something to unwrap
        return p_container
    elif len(p_container.getchildren()) > 1:
        # too many children, might be a deliberate <p> break
        return p_container
    
    if p_container.getchildren()[0].tag != 'p':
        # <p> is special, wouldn't want to unwrap a <b> or other formatting tag
        # no <p> wrapper to unwrap, returning unchanged
        return p_container
        
    element = p_container
    p = element.getchildren()[0]  # save first child

    # clear all children (in order to rebuild them better than before)
    attrib_save = element.attrib.copy()
    element.clear()
    element.attrib = attrib_save
    element.text = p.text
    for i, child in enumerate(p.getchildren()):
        element.append(child)
    return element

NBSP = u"\xa0"
NBSP_NUM = "&#160;"
NBSP_TEXT = "&nbsp;"

def remove_nbsp(element, depth=0):
    """removes any nbsp chars from the element -- modifies the element
        
    Deprecated since move to Mozilla Composer.
    """
    if depth == 0:
        element = copy.deepcopy(element)
    if element.text:
        element.text = element.text.replace(NBSP, ' ')
        element.text = element.text.replace(NBSP_NUM, ' ')
        element.text = element.text.replace(NBSP_TEXT, ' ')
    for child in element.getchildren():
        remove_nbsp(child, depth+1)
    if element.tail and depth > 0:
        element.tail = element.tail.replace(NBSP, ' ')
        element.tail = element.tail.replace(NBSP_NUM, ' ')
        element.tail = element.tail.replace(NBSP_TEXT, ' ')
    return element


def element_depth_iter(elem, depth=0):
    # return items in document order, each item is a tuple of (elem, depth)
    yield (elem, depth)
    for child in elem.getchildren():
        # a generator for each child
        for cn in element_depth_iter(child, depth+1):
            yield cn
    return


# ------------------------------------------------------------
# comparing trees -- compare normalized, serialized formats
# ... from effbot post here: http://mail.python.org/pipermail/xml-sig/2003-November/009997.html

def normalize(a):
    # get rid of whitespace
    # warning: alters input
    for i in a.getiterator():
        if i.text:
            i.text = i.text.strip()
        if i.tail:
            i.tail = i.tail.strip()
#         i.tail = None


def compare(a, b):
    # normalize and compare serializations
    # TODO IJ: write unit tests; does tostring() always serialize attributes in the same order?
    normalize(a)
    normalize(b)
    return tostring(a) == tostring(b)


# from effbotlib

def gettext(elem):
    text = elem.text or ""
    for e in elem:
        text += gettext(e)
        if e.tail:
            text += e.tail
    return text

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

# from http://effbot.org/zone/element-bits-and-pieces.htm

def cleanup(elem, filter):
    """Takes a tree and a filter function, and removes all subelements
    for which the filter returns false.
    
    Note that the top element itself isn't checked; if you need to
    remove that, you have to do that at the application level.
    """
    out = []
    for e in elem:
        cleanup(e, filter)
        if not filter(e):
            if e.text is not None:
                if out:
                    # guard for out[-1].tail being None added 5/16/08 by IJ
                    if out[-1].tail is None:
                        out[-1].tail = ''
                    out[-1].tail = stringConcat(out[-1].tail, e.text)
                else:
                    # guard for elem.text being None added 5/15/08 by IJ
                    if elem.text is None:
                        elem.text = e.text
                    else:
                        elem.text = stringConcat(elem.text, e.text)
            # JYTHON: getchildren() added because Jython complained: apparently
            # Jython's list.extend() isn't completely down with the iterator protocol?
            out.extend(e.getchildren())
            if e.tail:
                if out:
                   if out[-1].tail is None:
                       out[-1].tail = ''
                   out[-1].tail += e.tail
                else:
                    if elem.text is None:
                        elem.text = ''
                    elem.text = stringConcat(elem.text, e.tail)
        else:
            out.append(e)
    elem[:] = out


##
# fixtag() straight from ElementTree.py for Python 2.6 -- was removed in
# Python 2.7 but meld3 depends on it

def fixtag(tag, namespaces):
    # given a decorated tag (of the form {uri}tag), return prefixed
    # tag and namespace declaration, if any
    if isinstance(tag, QName):
        tag = tag.text
    namespace_uri, tag = string.split(tag[1:], "}", 1)
    prefix = namespaces.get(namespace_uri)
    if prefix is None:
        prefix = _namespace_map.get(namespace_uri)
        if prefix is None:
            prefix = "ns%d" % len(namespaces)
        namespaces[namespace_uri] = prefix
        if prefix == "xml":
            xmlns = None
        else:
            xmlns = ("xmlns:%s" % prefix, namespace_uri)
    else:
        xmlns = None
    return "%s:%s" % (prefix, tag), xmlns


def parentmap(elem):
    """return a dict mapping an element to its parent"""
    return dict([(c, p) for p in elem.getiterator() for c in p])
