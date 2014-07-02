import logging

from django.db import models

from djangotailoring.surveys.fields import JSONField

logger = logging.getLogger(__name__)

class SurveyState(models.Model):
    user_id = models.CharField(max_length=40, verbose_name="Unique user id")
    survey_id = models.TextField(verbose_name="Unique survey id")
    page_msgid = models.CharField(max_length=40,
        verbose_name="Unique msgid for the related survey page")
    running_subject_data = JSONField(
        verbose_name="Survey data for subject as of this page.", default="{}")
    latest_page_data = JSONField(verbose_name="page-relevant data "
        "from the latest form submission", default="{}")
    validation_errors = models.IntegerField(default=0,
        verbose_name="Number of cumulative errors on this page.")
    previous_state = models.ForeignKey('self', related_name="followed_by_set",
        null=True, blank=True)
    valid = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        get_latest_by = 'modified'
    
    def invalidate_descendents(self):
        for state in self.followed_by_set.all():
            state.valid = False
            state.save()
            state.invalidate_descendents()
    
    def rebuild_running_subject_data(self):
        logger.info('Rebuilding running subject data for %s on %s:%s',
            self.user_id, self.survey_id, self.page_msgid)
        if self.previous_state is not None:
            running_data = self.previous_state.rebuild_running_subject_data()
        else:
            running_data = self.running_subject_data.copy()
        running_data.update(self.latest_page_data)
        logger.debug('Running Data: %s', running_data)
        return running_data
    
    def current_subject_data(self):
        logger.info('Getting current subject data for %s on %s:%s',
            self.user_id, self.survey_id, self.page_msgid)
        data = self.running_subject_data.copy()
        data.update(self.latest_page_data)
        logger.debug('Current Data: %s', data)
        return data
    
