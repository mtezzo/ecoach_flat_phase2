from surveytracking import manager_from_path
from djangotailoring import SurveyController, project_document_path, getproject
from djangotailoring.surveyview import BaseSurveyView


# TODO: modify as necessary, pulling the ID from the session or the DB.
# This simple constant will let you get started with a single user.
def get_userid(request):
    return '{{app_name|slugify}}'


class {{controller_class_name}}(SurveyController):

    # TODO: modify as necessary for every survey you want to publish. First
    # tuple item is the short name of the survey as it will appear in the url;
    # the second item is the path to the corresponding survey file (the path
    # is relative to the MTS project).
    surveys = {{ survey_tuples|safe }}
    
    managers_map = dict((key, manager_from_path(
            project_document_path(value),
            getproject()),
    ) for key, value in surveys)
    
    reverse_managers_map = dict((v, k) for k, v in managers_map.items())
    
    @classmethod
    def manager_for_id(cls, surveyid):
        return cls.managers_map[surveyid]

    @classmethod
    def id_for_manager(cls, manager):
        return cls.reverse_managers_map[manager]

    def state_for_http_request(self, request):
        surveyid = self.kwargs['surveyid']
        msgid = self.kwargs['msgid']
        userid = get_userid(request)
        return self.state_for_params(userid, surveyid, msgid)

{% for survey_name, survey_path, view_class_name in mts_project_surveys %}
class {{view_class_name}}(BaseSurveyView):
    survey_controller_class = {{controller_class_name}}
    template = 'survey.html'
    
    # modify this to match your survey short name
    surveyid = '{{ survey_name }}'

    def handle_start_or_restart(self, request):
        try:
            state = self.get_survey_restart_state(request)
        except Exception:
            subject, errors = getproject().subject_for_primary_chars({})
            state = self.survey_controller_class.new_initial_state_for(
                self.get_tailoring_id(request), self.surveyid, subject)
            state.save()
        return self._redirect(state.pagemsgid)

    def get_tailoring_id(self, request):
        return get_userid(request)

    def get_subject(self, request):
        # TODO: modify as necessary. This line will get you a blank dummy subject.
        subject, errors = getproject().subject_for_primary_chars({})
        return subject
    
    def on_valid_submission(self, request, controller):
        controller.update_current_subject()
        controller.save_for_next_page()
    
{% endfor %}
