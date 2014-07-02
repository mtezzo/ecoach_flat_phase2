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

"""High-level interface to making messages.
"""

import sys
import os.path
import itertools
import __builtin__
import types

from tailoring2.common import ET
from tailoring2 import selection, substitute, render, util, evaluationcontext
from tailoring2.dictionary import DataSource, MTSDictionary

# ------------------------------------------------------------
# function compositions to make creating a pipeline more pleasant

def partial_phase(phase, evalcontext=None):
    """return call-function that takes (messages, errors) as parameters,
    always passing same evalcontext; the returned function itself
    returns a (newmessages, newerrors) tuple.
    """
    return lambda messages: phase(messages, evalcontext=evalcontext)


def make_pipeline(phases, evalcontext):
    """given a list of phases and an evalcontext, return a function to
    run all those phases in sequence, aggregating any errors
    encountered. The returned function takes one argument, a message
    instance, and returns a (result, errors) tuple.
    """
    def callall(messages):
        result = messages
        allerrors = []
        for phase in phases:
            result, errors = phase(result, evalcontext)
            allerrors.extend(errors)
        return result, allerrors
    return callall


def SelectionPipeline(evalcontext):
    """return a pipeline function, callable with a message doc, to
    process the document with each standard selection phase and return a
    modified copy of the document along with a list of errors
    encountered during processing:
        def mypipeline(messages) --> (new_messages, errors)
    @param selection_eval_context: the characteristics and processing functions
        to select commands with
    """
    # call each of these functions, in order, on the message doc
    return make_pipeline(
            [selection.select, selection.order, selection.limit, selection.default],
            evalcontext)
    

# ------------------------------------------------------------

class Pipeline(object):
    """knit together one message, one subject, one set of responses and errors.
    """
    
    def __init__(self, message, subject,
                make_evaluation_context=evaluationcontext.flat_evaluation_context,
                render_transforms=None):
        """message is an ET Element that represents the start of processing
                for this pass. Typically this will be a <section>, but it can be
                any message command element.
            subject is a Subject object
            make_evaluation_context is a one-arg callable that returns a mapping object
                with all the subject data, authorutil functions, source
                hoisting, and whatever customization the application may
                need. The default is the evaluationcontext module's
                flat_evaluation_context.
            render_transforms is a list of tree-modifying functions used to provide the
                final rendered output from the pipeline. If not present, a default html
                renderer will be used.
        """
        self.message = message
        self.subject = subject
        assert callable(make_evaluation_context), make_evaluation_context
        self.make_evaluation_context = make_evaluation_context
        self.render_transforms = render_transforms or render.BasicTransformList(
            render.CommandTranslator().translate)
        self.errors = []
    
    def select_phase(self, message=None):
        """returns a (result, errors) tuple where result is an ET.Element and errors
        is a list of ProcessingErrors
        """
        if message is None:
            message = self.message
        sel_chars = self.make_evaluation_context(self.subject.selection_chars)
        sel_pipeline = SelectionPipeline(sel_chars)
        return sel_pipeline(message)

    def substitute_phase(self, selected_message):
        """returns a (result, errors) tuple"""
        message_chars = self.make_evaluation_context(self.subject.message_chars)
        return substitute.substitute(selected_message, message_chars)
        
    def render_phase(self, selected_message):
        """returns a (result, errors) tuple.
        selected_message is an ET.Element -- usually it will have been
                substituted before calling render(), but not necessarily. It
                does need to have been selected already, though.

        TODO: the underlying RenderHTML API is inconsistent with the API
            for select and substitute. It wants an ET.ElementTree instead of
            an ET.Element and it returns just a result, not a (result, errors) tuple.
        """
        # render wants a tree, not an Element. But we'll eventually
        # return an Element.
        tree = ET.ElementTree(selected_message)
        result, errors = render.Transform(tree, self.render_transforms)
        return (result.getroot(), errors)

    def run(self):
        """starting from scratch, run select_phase(), sub_phase(), and
        render_phase(), and return an HTML-ified ET.Element
        """
        selected_message, sel_errors = self.select_phase(self.message)
        subbed_message, sub_errors = self.substitute_phase(selected_message)
        rendered_message, render_errors = self.render_phase(subbed_message)
        return rendered_message, list(itertools.chain(sel_errors, sub_errors, render_errors))

    # alias
#     def render_from_scratch(self):
#         import warnings
#         warnings.warn("use pipeline.run() instead of render_from_scratch()", DeprecationWarning)
#         return self.run()
