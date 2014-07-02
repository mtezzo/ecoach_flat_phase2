from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

# Create your views here.
def what_log_view(request):
    import datetime
    rwhen = datetime.datetime.now()
    try:
        # expect all of these to be defined by logging wrapper
        url = request.GET['url'] 
        category = request.GET['category'] 
        action = request.GET['action'] 
        label = request.GET['label'] 
        value = request.GET['value'] 
        json = request.GET['json'] 
    except:
        url = 'null' 
        category = 'null' 
        action = 'null' 
        label = 'null' 
        value = -1
        json = 'null' 
    log = ELog(who=request.user, mwhen=rwhen, url=url, category=category, action=action, label=label, value=value, json=json)
    log.save()
    return HttpResponse("Event record made.")
 

