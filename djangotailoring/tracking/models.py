import logging

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

logger = logging.getLogger('djangotailoring.tracking.events')

class Event(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, default='')
    related_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = generic.GenericForeignKey('related_content_type', 'related_object_id')
    
    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'timestamp'
    
    def __unicode__(self):
        return u"%s at %s" % ( self.name, self.timestamp )
    
    @classmethod
    def events_related_to(cls, related_object):
        related_ct = ContentType.objects.get_for_model(related_object)
        related_pk = related_object.id
        
        return Event.objects.filter(related_content_type=related_ct,
                                    related_object_id=related_pk)
    

# logging callback
def event_logger(sender, instance=None, created=False, **kwargs):
    if instance is not None and created:
        extra = dict(note=instance.note, timestamp=instance.timestamp,
            user=None, related_object=None, request=None)
        msg = ['%s event created' % instance.name]
        if instance.user is not None:
            extra['user'] = instance.user.username
            msg.append('for user %s' % instance.user.username)
        if instance.related_object is not None:
            extra['related_object'] = instance.related_object
            msg.append('connected to %r' % instance.related_object)
        if hasattr(instance, 'request') and instance.request is not None:
            extra['request'] = instance.request
            msg.append('@ %s' % instance.request.path)
        logger.info(' '.join(msg), extra=extra)

models.signals.post_save.connect(event_logger, sender=Event)
