import logging

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from djangotailoring.tracking.support import LatestEventMixin
from djangotailoring.project import getsubjectloader
from djangotailoring.subjects import SubjectDoesNotExist

logger = logging.getLogger(__name__)

class BaseUserProfile(LatestEventMixin, models.Model):
    subjectloaderclass = getsubjectloader()
    
    user = models.ForeignKey(User, unique=True)
    accepted_consent = models.NullBooleanField(blank=True)
    withdrawn_reason = models.CharField(max_length=64, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def is_active_participant(self):
        return (self.accepted_consent and
                (self.withdrawn_reason is None or
                 len(self.withdrawn_reason) == 0))
    
    @property
    def tailoringid(self):
        return str(self.user.id)
    
    def _get_tailoringsubject(self):
        if not hasattr(self, '_tailoringsubject'):
            logger.info('Getting tailoring subject for user %s.',
                self.user)
            try:
                s = self.subjectloaderclass.get_subject(self.tailoringid)[0]
            except SubjectDoesNotExist:
                logger.debug('Could not load subject. Creating a new one.')
                s = self.subjectloaderclass.empty_subject()[0]
            self._tailoringsubject = s
            logger.info('Tailoring subject retrieved.')
        return self._tailoringsubject
    def _set_tailoringsubject(self, subject):
        logger.info('Saving tailoring subject for user %s.', self.user)
        self._tailoringsubject = subject
        self.subjectloaderclass.store_subject(self.tailoringid, subject)
        logger.info('Tailoring subject saved.')
    def _delete_tailoringsubject(self):
        logger.info('Deleting tailoring subject for user %s.', self.user)
        self.subjectloaderclass.delete_subject(self.tailoringid)
        del self._tailoringsubject
        logger.info('Tailoring subject deleted.')
    tailoringsubject = property(_get_tailoringsubject, _set_tailoringsubject,
        _delete_tailoringsubject, "Access and modify a tailoring2.Subject "
        "tied to the associated user.")
    
    def characteristic_value(self, valuename, source=''):
        split_val = valuename.split('.')
        if len(split_val) == 2:
            source, value = split_val
        else:
            value = valuename
        tsub = self.tailoringsubject.selection_chars
        sourcedict = tsub.get(source, {})
        return sourcedict.get(value, None)
    
    def __unicode__(self):
        return '%s' % self.user
    
    class Meta:
        abstract = True
    

_handler_registry = set()
def register_profile_post_save_handler(profileclass):
    if profileclass not in _handler_registry:
        logger.info('Registering User Profile class post-save creation for %s',
            profileclass.__name__)
        _handler_registry.add(profileclass)
        def on_user_creation(sender, instance, created, **other):
            if created:
                logger.debug('Generating new %s instance for %s.',
                    profileclass.__name__, instance)
                profileclass.objects.create(user=instance)
        
        post_save.connect(on_user_creation, sender=User, weak=False)

