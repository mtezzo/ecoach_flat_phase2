from django.views.generic import TemplateView

from djangotailoring import getproject, TailoringRequest

class BaseMultipleTailoredDocView(TemplateView):
    """A base for generic views that tailor based on multiple MTS message
    documents.
    
    To use, the following attribute is available for overriding:
      - message_documents ({}): a dictionary-like object that builds at
        mapping of template context names to message document paths.
        For instance, if it is a dict of
            {'treq1': 'Messages/Welcome.messages',
             'treq2': 'Messages/Header.messages'},
        Within the template context, there would be two different
        TailoringRequest instances, which can be rendered using the
        render_section tag found in tailoring2tags as follows:
        {% render_section treq1 <sectionname> %}
        {% render_section treq2 <sectionname> %}
    
    Additionally, subclasses should implement a method `get_subject` that 
    returns a tailoring2 Subject instance.
    """
    message_documents = {}
    
    def get_subject(self):
        return None
    
    def get_message_documents(self):
        return self.message_documents
    
    def get_tailoring_request(self, doc):
        return TailoringRequest(getproject(), doc,
            self.get_subject(), None)
    
    def get_context_data(self, **kwargs):
        context = super(BaseMultipleTailoredDocView, self).get_context_data(
            **kwargs)
        for context_name, docname in self.get_message_documents().items():
            context[context_name] = self.get_tailoring_request(docname)
        return context
    

class BaseTailoredDocView(BaseMultipleTailoredDocView):
    """A base for generic views that tailor MTS message documents.
    
    This is a simplified way of building tailored views with only a single
    document. This is equivalent of having a BaseMultipleTailoredDocView
    with message_documents = {context_treq_name: message_document}.
    
    To use, the following attributes are available for overriding:
      - message_document (None): a path (absolute, or relative to the MTS
        project root) to an MTS .messages document.
      - context_treq_name ('treq'): a string that identifies the context
        variable name for the TailoringRequest instance used in rendering.
    
    In a template, use the
    {% render_section `context_treq_name` <sectionname> %} tag to output the
    tailored HTML.
    """
    message_document = None
    context_treq_name = 'treq'
    
    def get_message_document(self):
        return self.message_document
    
    def get_message_documents(self):
        return {self.context_treq_name: self.get_message_document()}
    

class UserProfileSubjectMixin(object):
    """Connects the subject handlers attached to the
    djangotailoring.UserProfile to a TailoredDocView."""
    
    def get_profile(self):
        return self.request.user.get_profile()
    
    def get_subject(self):
        return self.get_profile().tailoringsubject
    
    def get_user_id(self):
        return self.get_profile().tailoringid
    
    def save_subject(self, subject):
        self.get_profile().tailoringsubject = subject
    

class TailoredDocView(UserProfileSubjectMixin, BaseTailoredDocView):
    """A generic view that renders a single MTS message document to a template
    for the current logged-in user.
    
    Attributes:
      - message_document: a path to an MTS message document, absolute or
        relative to the active MTS project.
      - context_treq_name ('treq'): a string that names the variable assigned
        to the TailoringRequest for the current http request.

    In a template, use the
    {% render_section `context_treq_name` <sectionname> %} tag to output the
    tailored HTML.
    """
    pass

class MultipleTailoredDocView(UserProfileSubjectMixin,
                              BaseMultipleTailoredDocView):
    """A generic view that renders a multiple MTS message documents to a
    template for the current logged-in user.

    Attributes:
     - message_documents ({}): a dictionary-like object that builds at
       mapping of template context names to message document paths.
       For instance, if it is a dict of
           {'treq1': 'Messages/Welcome.messages',
            'treq2': 'Messages/Header.messages'},
       Within the template context, there would be two different
       TailoringRequest instances, which can be rendered using the
       render_section tag found in tailoring2tags as follows:
       {% render_section treq1 <sectionname> %}
       {% render_section treq2 <sectionname> %}
    """
    pass
