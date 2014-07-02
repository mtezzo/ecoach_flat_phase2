import functools
import time

from django.contrib.auth.decorators import user_passes_test
from django.utils.functional import wraps
from djangotailoring.tracking import create_event
from djangotailoring.tracking.eventnames import EventNames

def log_page_view(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        user = request.user if request.user.is_authenticated() else None
        response = f(request, *args, **kwargs)
        if response.status_code != 200:
            if response.status_code == 302:
                create_event(EventNames.Redirected, request,
                    note='From: %s \tTo: %s' % (request.path,
                        response['Location']))
            else:
                create_event(EventNames.PageError, request,
                    note='\n'.join([request.path,
                        'Response Code: %d' % response.status_code,]))
        else:
            create_event(EventNames.PageViewed, request)
        return response
    return wrapper

# def _is_withdrawn(profile):
#     return ( profile.withdrawn_reason is not None and
#              profile.withdrawn_reason.strip() != '' )

# has_consented = user_passes_test(
#     lambda u: u.is_authenticated() and u.get_profile().consented)

# is_oriented = user_passes_test(
#     lambda u: u.is_authenticated() and u.get_profile().oriented)

def _in_group(user, groupname):
    return groupname in (group.name for group in user.groups.iterator())

def user_in_group(groupname):
    return user_passes_test(functools.partial(_in_group, groupname=groupname))

def active_participant_test(user):
    # profile = user.get_profile()
    return ( user.is_authenticated() and
             _in_group(user, 'studyparticipants') ) # and
             # not _is_withdrawn(profile) and
             # profile.consented )

is_active_participant = user_passes_test(active_participant_test)
