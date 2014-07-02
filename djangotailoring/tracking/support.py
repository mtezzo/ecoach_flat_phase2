from djangotailoring.tracking.models import Event

class LatestEventMixin(object):
    """A Mixin providing easy access to specific user events on an object with
    a user attribute."""
    def latest_event(self, eventname=None):
        queryset = Event.objects.filter(user=self.user)
        if eventname is not None:
            queryset = queryset.filter(name=eventname)
        try:
            return queryset.latest()
        except Event.DoesNotExist:
            return None
    
    def latest_event_date(self, eventname=None):
        event = self.latest_event(eventname)
        return event.timestamp if event else None
    
