from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.generic import TemplateView
from mynav.selector_nav import *
#from myselector.nav_info import NavInfo
#from myselector.models import RSSLog, ELog

def mylogout_view(request):
    return HttpResponseRedirect("https://weblogin.umich.edu/cgi-bin/logout")

def mylogin(request, **kwargs):
    return render_to_response('django.contrib.auth.views.login')

def test1(request, **kwargs):
    return HttpResponse("You're looking at the selector test page")

def course_select_view(request, **kwargs):
    
    return render(request, 'myselector/mycourse.html', {
        "main_nav": selector_main_nav(request.user, 'coaches')
    })

def about_view(request, **kwargs):
    
    return render(request, 'myselector/about.html', {
        "main_nav": selector_main_nav(request.user, 'static_linkback')
    })

def team_view(request, **kwargs):
    
    return render(request, 'myselector/team.html', {
        "main_nav": selector_main_nav(request.user, 'static_linkback')
    })

def press_view(request, **kwargs):
    
    return render(request, 'myselector/press.html', {
        "main_nav": selector_main_nav(request.user, 'static_linkback')
    })


