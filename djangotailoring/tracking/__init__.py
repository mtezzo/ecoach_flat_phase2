import sys

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from djangotailoring.tracking.models import Event
from djangotailoring.tracking.eventnames import EventNames

def create_event(name, request=None, user=None, note=None, related_object=None):
    """Make an event record for a given set of parameters. If request is
    given, the user is pulled from the request, and in the absense of a note,
    the note is set to the request path."""
    if request is not None:        
        if user is None and hasattr(request, 'user') and request.user.is_authenticated():
            user = request.user
        if note is None:
            note = request.path
    e = Event(name=name)
    if user is not None and user.is_authenticated():
        e.user = user
    if related_object is not None:
        e.related_object = related_object
    if note is not None:
        e.note = note
    # the following attribute is not stored in the database, but it's useful
    # for the logger function in djangotailoring.tracking.models.
    e.request = request
    e.save()
    return e

def _get_user(kwargs):
    user = kwargs.get('user')
    if user is None:
        user = getattr(kwargs.get('request'), 'user', None)
    return user

@receiver(user_logged_in)
def user_logged_in_callback(sender, **kwargs):
    user = _get_user(kwargs)
    if user is not None:
        create_event(EventNames.UserLoggedIn, user=user,
            request=kwargs.get('request'))

@receiver(user_logged_out)
def user_logged_out_callback(sender, **kwargs):
    user = _get_user(kwargs)
    if user is not None:
        create_event(EventNames.UserLoggedOut, user=user,
            request=kwargs.get('request'))

