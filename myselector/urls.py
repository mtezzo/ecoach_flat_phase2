from django.conf.urls.defaults import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin
    #url(r'^admin/', include(admin.site.urls)),

    # login / logout
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout', mylogout_view, name='mylogout'),

    # public pages
    url(r'^about/', about_view, name='about'),
    url(r'^team/', team_view, name='team'),
    url(r'^press/', press_view, name='press'),

    # main
    url(r'^', login_required(course_select_view), name='course_select'),
)

