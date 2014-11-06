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

"""Walk through a parsed message document and substitute subject data
for any $sub tokens embedded in the message elements.
"""

import copy
import logging
log = logging.getLogger(__name__)

from string_template import TailoringTemplate

from common import *

# ------------------------------------------------------------

def sub_variables(text, evalcontext):
    """return string 'text' after running it through variable substitution. Any raised
    exceptions are the responsibility of the caller.

    @param text: a string, the text to perform substitutions on
    @param evalcontext: a dictionary, the namespace to take variable substitutions from
    """
    text = unicode(text)
    if text is not None and text.find("$")>=0:
        tmpl = TailoringTemplate(text)
        try:
            return tmpl.substitute(evalcontext)
        # string_template usually raises KeyError no matter what error it really was [WACK]
        except KeyError, err:
            raise err._realerror
        # except when it doesn't match the "I'm an expression" regexp, in which case it's
        # a ValueError. But those are usually really SyntaxErrors. [WACK]
        except ValueError, err:
            raise SyntaxError(unicode(err))
    else:
        return text


def substitute(messages, evalcontext):
    log.debug('>>> substitute')    
    messages = deepcopy_element(messages)
#    messages = copy_ET(messages)
    parentmap = dict([(c, p) for p in messages.getiterator() for c in p])
    errors = []
    for elem in messages.getiterator('content'):
        for attr in ['text', 'tail']:
            if hasattr(elem, attr):
                val = getattr(elem, attr)
                # some content elements are empty (eg, paragraphs)
                if val is None:
                    continue
                try:
                    setattr(elem, attr, sub_variables(val, evalcontext))
                except Exception, err:
                    # report the parent elem, since the current elem is always going
                    # to be a <content> elem with no msgid or other context
                    parent_elem = parentmap[elem]
                    errors.append(ProcessingError(err, 'substitute', parent_elem,
                            message='%s in %s: %s' % (err, attr, val)))
    return messages, errors
