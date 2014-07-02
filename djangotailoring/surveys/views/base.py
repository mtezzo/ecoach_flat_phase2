from django.views.generic import TemplateView
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect

from tailoring2.subject import Subject
from tailoring2.common import ProcessingAttributes
from surveytracking import manager_from_path
from surveytracking.projectutils import InvalidDataError
from surveytracking.classes import (Page, SurveyManager, GotoDestination,
                                    EndOfSurvey, ValidationError)

from djangotailoring.tailoringrequest import TailoringRequest
from djangotailoring.project import (getproject, project_document_path,
                                     project_tailoring_doc)
from djangotailoring.views.tailoring import UserProfileSubjectMixin

from djangotailoring.surveys.models import SurveyState
from djangotailoring.surveys.views.render import SurveyRenderChunk

class PageNotFound(Exception): pass

class StateNotFound(Exception): pass

class BaseSurveyView(TemplateView):
    survey_manager = None
    survey_id = None
    context_chunk_name = 'chunk'
    
    # ---------- getters ----------
    
    def get_survey_id(self):
        return self.survey_id
    
    def get_user_id(self):
        return ''
    
    def get_survey_manager(self):
        return self.survey_manager
    
    def get_project(self):
        return self.manager.project
    
    def get_subject(self):
        return Subject([''], {'':{}})
    
    def get_request_subject(self):
        return self.subject_with_additional_data(
            self.state_subject_data(self.state))
    
    # -- Passing the source from the manager as the default source
    def get_tailoring_request(self):
        return TailoringRequest(None, source=self.manager.source)
    
    def subject_with_additional_data(self, data):
        subject = self.get_subject()
        source = self.get_active_source()
        project = self.get_project()
        primary_chars = dict((key, dict(val)) for key, val in
            subject.primary_chars.items())
        sourcedict = primary_chars.setdefault(source, {})
        sourcedict.update(data)
        return project.subject_for_primary_chars(primary_chars)
    
    def get_active_source(self):
        treq = self.get_tailoring_request()
        if hasattr(treq, 'default_source'):
            return treq.default_source
        return self.manager.source
    
    def _get_tailoring_context(self, subject=None):
        if subject is None:
            subject = self.request_subject
        treq = self.get_tailoring_request()
        if 'default_source' not in treq:
            treq.default_source = self.manager.source
        return self.get_project().get_eval_factory(treq)(
            subject.selection_chars)
    
    # ---------- traversal handlers ----------
    
    def _can_pass_page(self, page, context, ignore_loose_validation):
        try:
            manager_says_so = self.manager.can_pass_page(page, context,
                ignore_loose_validation)
            return manager_says_so and not self.request_errors
        except GotoDestination:
            return len(self.request_errors) == 0
        except:
            return False
    
    def can_pass_page(self, subject=None):
        if subject is None:
            subject = self.request_subject
        ignore_loose_validation = self.state_has_validation_errors(self.state)
        context = self._get_tailoring_context(subject)
        return self._can_pass_page(self.page, context,
            ignore_loose_validation)
    
    def is_valid_submission(self):
        can_pass = self.can_pass_page()
        if not can_pass:
            self.on_validation_error(self.state)
        return can_pass
    
    def _next_page_with_content(self):
        context = self._get_tailoring_context()
        page = self.manager.next_page_for_context(self.page, context)
        while True:
            if not self._can_pass_page(page, context, True):
                break
            chunk = SurveyRenderChunk(page.tree, self.request_subject,
                self.get_tailoring_request(), {}, False)
            if not chunk.has_content() and not chunk.has_errors():
                page = self.manager.next_page_for_context(page, context)
            else:
                break
        return page
    
    def get_render_chunk(self, show_errors=None):
        treq = self.get_tailoring_request()
        treq.default_source = self.get_active_source()
        if show_errors is None:
            show_errors = getattr(treq, 'show_errors',
                self.state_has_validation_errors(self.state))
        subject = self.request_subject
        return SurveyRenderChunk(self.page.tree, subject, treq,
            self.state.latest_page_data, show_errors, self.request_errors)
    
    # ---------- navigation handlers ----------
    
    def get_base_url(self):
        path = self.request.path_info
        page_id = self.kwargs.get('page_id', '')
        length = len(page_id)
        page_id_index = path.rindex(page_id)
        return '%s%%s%s' % (path[:page_id_index], path[page_id_index + length:])
    
    def url_for_page_id(self, page_id):
        return self.get_base_url() % page_id
    
    def get_previous_url(self):
        previous_page = self.get_previous_page(self.state)
        if previous_page:
            return self.url_for_page_id(
                self.manager.first_unique_msgid_for_page(previous_page))
        return None
    
    def redirect(self, page=None, page_id=None):
        if page_id is not None:
            return redirect(self.url_for_page_id(page_id))
        elif page is not None:
            return redirect(self.url_for_page_id(
                self.manager.first_unique_msgid_for_page(page)))
        return None
    
    def get_current_page(self):
        msgid = self.kwargs.get('page_id')
        page = self.manager.first_page_with_msgid(msgid)
        if page is None:
            raise PageNotFound
        return page
    
    # ---------- request data conversion ----------
    
    def get_request_data(self):
        return self.request.POST
    
    def _request_value_for_chardef(self, chardef):
        request_data = self.get_request_data()
        request_name = ProcessingAttributes.SURVEY_ITEM_PREFIX + chardef.name
        if chardef is None or chardef.is_multivalued:
            return request_data.getlist(request_name)
        return request_data.get(request_name, None)
    
    def _tailoring_value_for_chardef(self, chardef):
        request_value = self._request_value_for_chardef(chardef)
        pytype = chardef.basetype.pytype
        is_multivalued = chardef.is_multivalued
        valid = True
        if is_multivalued and not isinstance(request_value,
                                             (list, tuple, set)):
            if request_value is None:
                request_value = []
            else:
                request_value = [request_value]
        request_value = chardef.basetype_normalize(request_value)
        if request_value is not None and request_value != "":
            if is_multivalued:
                if not all((isinstance(v, pytype) for v in request_value)):
                    valid = False
            elif not isinstance(request_value, pytype):
                valid = False
        if not valid:
            raise InvalidDataError(chardef.name, request_value, pytype)
        return request_value
    
    def get_request_survey_data(self):
        survey_data = {}
        errors = []
        page = self.get_current_page()
        mtsdict = self.get_project().mtsdict
        for char in self.page.characteristics:
            chardef = mtsdict.char_index.get(char)
            if chardef is None:
                continue
            try:
                tailoring_value = self._tailoring_value_for_chardef(chardef)
                if tailoring_value is not None:
                    survey_data[char] = tailoring_value
            except InvalidDataError, e:
                errors.append(e)
        return survey_data, errors
    
    def get_context_data(self, **kwargs):
        context = super(BaseSurveyView, self).get_context_data(**kwargs)
        context[self.context_chunk_name] = self.get_render_chunk()
        context['previous_url'] = self.get_previous_url()
        return context
    
    # ---------- dispatch handlers ----------
    
    def init_locals(self):
        self.manager = self.get_survey_manager()
        self.page = self.get_current_page()
        self.survey_id = self.get_survey_id()
        self.state = self.get_current_state()
        self.request_errors = []
        if self.request.method == 'POST':
            survey_data, errors = self.get_request_survey_data()
            self.set_state_request_data(self.state, survey_data)
            self.request_errors = errors
            self.save_state(self.state)
        self.request_subject = self.get_request_subject()[0]
    
    def get(self, request, *args, **kwargs):
        if not self.can_access_survey():
            return self.handle_bad_page_request()
        try:
            self.init_locals()
        except (PageNotFound, StateNotFound):
            next_state = self.state_for_restart()
            return self.redirect_to_state(next_state)
        self.on_successful_page_request()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        if not self.can_access_survey():
            return self.handle_bad_page_request()
        try:
            self.init_locals()
        except PageNotFound:
            raise Http404
        self.on_successful_page_request()
        if self.is_valid_submission():
            self.on_valid_submission()
            try:
                next_page = self._next_page_with_content()
                next_state = self.create_next_state(next_page)
                return self.redirect_to_state(next_state)
            except EndOfSurvey:
                return self.handle_end_of_survey()
        else:
            self.on_invalid_submission()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def render_to_response(self, context, **response_kwargs):
        """Ensure that clients don't cache pages so that the tailoring is
        always up to date, which is very important for Surveys."""
        response = super(BaseSurveyView, self).render_to_response(context,
            **response_kwargs)
        response['Cache-Control'] = 'no-cache'
        return response
    
    # ---------- view handlers ----------
    
    def can_access_survey(self):
        return True
    
    def handle_bad_page_request(self):
        """Return an HttpResponse that indicates that indicates that a
        page is inaccessible, such as returning a 404 Not Found, or
        redirecting to a valid page."""
        return HttpResponseForbidden()
    
    def handle_end_of_survey(self):
        """Return an HttpResponse that indicates that the survey has been
        completed, such as redirecting to an acknowledgement page."""
        return redirect('/')
    
    def on_successful_page_request(self):
        """Called when a survey controller and associated survey state have
        successfully been found, and can proceed to rendering an actual
        survey page, or handle the survey submission."""
        pass
    
    def on_valid_submission(self):
        """Called when a survey submission is legitimate for the current
        survey state."""
        pass
    
    def on_invalid_submission(self):
        """Called when a survey submission is found to produce errors for the
        current survey state."""
        pass
    
    
    # ---------- state methods ----------
    
    def _get_state_for_page(self, page=None):
        args = dict(user_id=self.get_user_id(), survey_id=self.survey_id,
            valid=True)
        if page is not None:
            all_ids = self.manager.unique_msgids_for_page(page)
            args['page_msgid__in'] = all_ids
        return SurveyState.objects.filter(**args).latest()
    
    def get_current_state(self):
        try:
            return self._get_state_for_page(self.page)
        except SurveyState.DoesNotExist:
            raise StateNotFound
    
    def get_latest_state(self):
        return self._get_state_for_page()

    def apply_testcase_data(self, state, page):
        subject = self.get_subject()
        source_data = subject.selection_chars.get(self.manager.source, {})
        latest_page_data = {}
        for char in page.characteristics:
            if char in source_data:
                latest_page_data[char] = source_data[char]
        state.latest_page_data = latest_page_data
     
    def create_next_state(self, next_page):
        try:
            state = self._get_state_for_page(next_page)
        except SurveyState.DoesNotExist:
            next_page_id = self.manager.first_unique_msgid_for_page(next_page)
            state = SurveyState(user_id=self.get_user_id(),
                survey_id=self.get_survey_id(), page_msgid=next_page_id)
        state.running_subject_data = self.state.current_subject_data()
        state.previous_state = self.state
        self.state.invalidate_descendents()
        state.valid = True
        self.apply_testcase_data(state, next_page)
        state.save()
        return state
     
    def create_initial_state(self):
        state = SurveyState(user_id=self.get_user_id(),
            survey_id=self.get_survey_id())
        page = self.manager.pages[0]
        first_page_id = self.manager.first_unique_msgid_for_page(page)
        state.page_msgid = first_page_id
        self.apply_testcase_data(state, page)
        state.save()
        return state
    
    def state_subject_data(self, state):
        return state.current_subject_data()
    
    def state_has_validation_errors(self, state):
        return state.validation_errors > 0
    
    def on_validation_error(self, state):
        state.validation_errors += 1
    
    def get_previous_page(self, state):
        if state.previous_state is not None:
            return self.manager.first_page_with_msgid(
                state.previous_state.page_msgid)
        return None
    
    def redirect_to_state(self, state):
        return self.redirect(page_id=state.page_msgid)
    
    def set_state_request_data(self, state, data):
        state.latest_page_data = data
    
    def save_state(self, state):
        state.save()
   
    def state_for_restart(self):
        return self.create_initial_state()
        #try:
        #    return self.get_latest_state()
        #except SurveyState.DoesNotExist:

class AutoSaveSubjectDataMixin(object):
    """Calls save_subject when a user submits a valid request on a survey
    page."""
    
    def on_valid_submission(self):
        self.save_subject(self.request_subject)
    

class NoManagerMixin(object):
    """Automatically creates a SurveyManager based on two parameters for use
    in a SurveyView. Simplifies the creation of a survey view down to a single
    subclass with class attributes rather than having to create a manager
    out-of-band.
    """
    survey_document = None
    source = None
    
    _managers = {}
    
    @classmethod
    def build_manager(cls, survey_document=None, source=None):
        if survey_document is None:
            survey_document = cls.survey_document
        if source is None:
            source = cls.source
        return manager_from_path(
            project_document_path(survey_document), project=getproject(),
            source=source)
   
    # jared override this 
    def get_survey_document(self):
        return self.survey_document
    
    def get_source(self):
        return self.source
    
    get_active_source = get_source
    
    def get_survey_manager(self):
        survey_doc = self.get_survey_document()
        source = self.get_source()
        key = (survey_doc, source)
        if key not in self._managers:
            self._managers[key] = self.__class__.build_manager(*key)
        return self._managers[key]
    

class SimpleSurveyView(NoManagerMixin, BaseSurveyView):
    """Subclass to create a self-contained Survey view for the following
    required parameters:
        - survey_document: a path to an MTS survey, optionally relative to the
            current project.
        - source: a string representing the name of the source that survey
            data will be stored.
        - survey_id: a string used to identify the survey in serializing state
            to the database.
    Optionally, provide:
        - context_chunk_name: the name given to the template context object
            for the RenderSurveyChunk.
    """
    pass


class BaseSinglePageSurveyView(BaseSurveyView):
    """
    Assumptions:
    * There is a single page to the survey.
    
    Changes:
    * There is no page_id parameter requirement
    * get_current_page is always that one page.
    """
    def get_current_page(self):
        # The page is always the same
        return self.manager.pages[0]
    
    def redirect(self, page=None, page_id=None):
        # the URL should always be the same, as if there was no page_id
        return super(BaseSinglePageSurveyView, self).redirect(page_id='')
    

class SinglePageSurveyView(NoManagerMixin, BaseSinglePageSurveyView):
    """
    Provides a survey view that assumes that the Survey document consists of a
    single page. This mainly saves some URL configuration noise.
    """
    
    @classmethod
    def build_manager(cls, survey_document=None, source=None):
        if survey_document is None:
            survey_document = cls.survey_document
        if source is None:
            source = cls.source
        return SurveyManager(
            [Page(project_tailoring_doc(survey_document).getroot())],
            project=getproject(),
            source=source)
    
