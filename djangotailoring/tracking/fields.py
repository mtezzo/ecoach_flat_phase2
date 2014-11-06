from django.db import models
from django.db.models.signals import post_save

from djangotailoring.tracking.models import Event

class DenormalizedEventFieldMixin(object):
    """Provides a bridge between a model field definition and an event set
    and a model with a .user reference. It will listen for the creation of the
    specified event, and set its value to that returned by get_value()."""
    
    def get_value(self, event):
        """Override this to return the value that the field will be assigned
        upon the triggering of the specified event."""
        return None
    
    def __init__(self, eventname=None, *args, **kwargs):
        self.eventname = eventname
        super(DenormalizedEventFieldMixin, self).__init__(*args, **kwargs)
    
    def contribute_to_class(self, cls, *args, **kwargs):
        super(DenormalizedEventFieldMixin, self).contribute_to_class(cls,
            *args, **kwargs)
        self.model = cls
        post_save.connect(self.post_save_handler, sender=Event, weak=False)
    
    def post_save_handler(self, sender, instance, created, **other):
        event = instance
        if event.name == self.eventname:
            model_objects = self.model.objects.filter(user=event.user)
            for model_object in model_objects:
                setattr(model_object, self.attname, self.get_value(event))
                model_object.save()
    


def denormalize_event_data_for_type(fieldtype):
    """Generates a Field class that effectively is a mashup of the field type
    and the DenormalizedEventFieldMixin, setting the value of the field to the
    return value of the decorated function."""
    def decorator(f):
        class _DenormalizedEventField(DenormalizedEventFieldMixin, fieldtype):
            def get_value(self, event):
                return f(event)
        _DenormalizedEventField.__name__ = f.__name__
        _DenormalizedEventField.__module__ = f.__module__
        _DenormalizedEventField.__doc__ = f.__doc__
        return _DenormalizedEventField
    return decorator

class DenormalizedEventTimestampField(DenormalizedEventFieldMixin, models.DateTimeField):
    """Maintains a datetime value on a model object whenever the specified
    event is fired for the associated user."""
    
    def get_value(self, event):
        return event.timestamp
    

@denormalize_event_data_for_type(models.PositiveIntegerField)
def DenormalizedEventCountField(event):
    """Maintains a count of the specified events for the associated user."""
    return Event.objects.filter(name=event.name, user=event.user).count()

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([],
        ["^djangotailoring\.tracking\.fields\.DenormalizedEventTimestampField",
         "^djangotailoring\.tracking\.fields\.DenormalizedEventCountField"])
except ImportError:
    # failures due to South not being installed are not errors.
    pass
