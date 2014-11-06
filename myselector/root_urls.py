from django.conf.urls.defaults import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

mts_patterns = patterns('',
    # admin
    url(r'^admin/', include(admin.site.urls)),

    # staff apps
    url(r'^staff/',         include('mypublisher.urls', namespace='mystaff')),
    url(r'^publisher/',     include('mypublisher.urls', namespace='mypublisher')),
    url(r'^upload/',        include('myloader.urls', namespace='myloader')),
    url(r'^export/',        include('myexporter.urls', namespace='myexporter')),
    url(r'^nts/',           include('nts.urls', namespace='nts')),
    url(r'^emailer/',       include('myemailer.urls', namespace='myemailer')),
    url(r'^usage/',         include('myusage.urls', namespace='myusage')),
    url(r'^logger/',        include('mylogger.urls', namespace='mylogger')),

    # message project
    url(r'^',               include('mytailoring.urls', namespace='mytailoring')),
)

urlpatterns = patterns('',
    url(r'^coachX/',        include(mts_patterns)), # invisable via Apache (only so reverse works)
    url(r'^coaches/',       include('myselector.urls', namespace='myselector')),
    url(r'^',               redirect_to, {'url': '/coaches/'})
)

