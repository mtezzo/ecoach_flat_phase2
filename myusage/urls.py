from django.conf.urls.defaults import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin
    #url(r'^admin/', include(admin.site.urls)),

    # staff app
    url(r'^your_tail/', login_required(your_tail_view), name='your_tail'),
    url(r'^everyone_tail/', login_required(everyone_tail_view), name='everyone_tail'),
    url(r'^usage_vector/', login_required(usage_vector_view), name='usage_vector'),
    url(r'^', login_required(your_tail_view), name='default'),

)

