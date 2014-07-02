from django.conf import settings
from django.template.response import SimpleTemplateResponse
from django.utils.translation import activate, deactivate

from djangotailoring.views.tailoring import (BaseTailoredDocView,
                                             BaseMultipleTailoredDocView,
                                             UserProfileSubjectMixin)

class LocalizedDocFinder(object):
    
    def find_localized(self, docmap):
        langcode = self.request.LANGUAGE_CODE
        baselangcode = langcode.split('-')[0]
        resolution_order = [langcode, baselangcode, settings.LANGUAGE_CODE,
            'en', '', None]
        for option in resolution_order:
            if option in docmap:
                if option:
                    self.foundlangcode = option
                return docmap[option]
        return None
    
    def get(self, request, *args, **kwargs):
        response = super(LocalizedDocFinder, self).get(request, *args,
            **kwargs)
        if hasattr(self, 'foundlangcode') and hasattr(response, 'render'):
            activate(self.foundlangcode)
            response.render()
            deactivate()
        return response
    

class BaseLocalizedTailoredDocView(LocalizedDocFinder, BaseTailoredDocView):
    """A base for generic views that tailor MTS message documents based on a
    user's locale.
    
    To use, the following attribute is available for overriding:
      - localized_documents ({}): a dict-like object that maps locale names
        to message doc paths (relative or absolute).
      - context_treq_name ('treq'): as described in `BaseTailoredDocView`
    
    Documents are chosen based on the following resolution order:
      - request.LANGUAGE_CODE
      - the base language of request.LANGUAGE_CODE
      - settings.LANGUAGE_CODE
      - 'en'
      - ''
      - None
    For instance, if `localized_documents` = { 'en' : docA, 'es': docB ) and
    the user had their locale set to 'es-mx' for Spanish/Mexican, docB would
    be chosen, because a match was found for the base language of
    request.LANGUAGE_CODE. If the user had their locale set to 'fr', docA
    would be chosen, as the final attempt option is 'en'. Having something set
    to the locale of '' will allow for a final fall-through. Useful
    for times where the message document is language agnostic.
    """
    localized_documents = {}
    
    def get_localized_documents(self):
        return self.localized_documents
    
    def get_message_document(self):
        return self.find_localized(self.get_localized_documents())
    

class BaseMultipleLocalizedTailoredDocView(LocalizedDocFinder,
                                           BaseMultipleTailoredDocView):
    """A base for generic views that tailor multiple MTS message documents
    based on a user's locale.

    Override message_documents as in `BaseMultipleTailoredDocView`, but
    instead of message doc paths, the values should be dict-like objects as
    defined in `BaseLocalizedTailoredDocView.localized_documents`.
    E.g.: {'treq1': {'en': docA, 'es': docB}, 'treq2': {'': docC}}.
    In the above example, treq1 will be assigned docA or docB as appropriate
    for the request, while treq2 will always result in docC being chosen.
    """
    def get_message_documents(self):
        sup = super(BaseMultipleLocalizedTailoredDocView, self)
        docs = sup.get_message_documents()
        find_locs = self.find_localized
        return dict((c, find_locs(d)) for c, d in docs.items())
    
class LocalizedTailoredDocView(UserProfileSubjectMixin,
                               BaseLocalizedTailoredDocView):
    """A generic views that tailor MTS message documents for the
    logged-in user, based on their locale.

    To use, the following attribute is available for overriding:
     - localized_documents ({}): a dict-like object that maps locale names
       to message doc paths (relative or absolute).
     - context_treq_name ('treq'): as described in
       `djangotailoring.views.TailoredDocView`

    Documents are chosen based on the following resolution order:
     - request.LANGUAGE_CODE
     - the base language of request.LANGUAGE_CODE
     - settings.LANGUAGE_CODE
     - 'en'
     - ''
     - None
    For instance, if `localized_documents` = { 'en' : docA, 'es': docB ) and
    the user had their locale set to 'es-mx' for Spanish/Mexican, docB would
    be chosen, because a match was found for the base language of
    request.LANGUAGE_CODE. If the user had their locale set to 'fr', docA
    would be chosen, as the final attempt option is 'en'. Having something set
    to the locale of '' will allow for a final fall-through. Useful
    for times where the message document is language agnostic.
    """
    pass

class MultipleLocalizedTailoredDocView(UserProfileSubjectMixin,
                                       BaseMultipleLocalizedTailoredDocView):
    """A base for generic views that tailor multiple MTS message documents
    for the logged-in user, based on their locale.

    Override message_documents as in
    `djangotailoring.views.MultipleTailoredDocView`, but
    instead of message doc paths, the values should be dict-like objects as
    defined in `LocalizedTailoredDocView.localized_documents`.
    E.g.: {'treq1': {'en': docA, 'es': docB}, 'treq2': {'': docC}}.
    In the above example, treq1 will be assigned docA or docB as appropriate
    for the request, while treq2 will always result in docC being chosen.
    """
    pass
