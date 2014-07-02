from django.conf.urls.defaults import *

urlpatterns = patterns('djangotailoring.views',
    (r'^(?P<docpath>.+)/(?P<sectionname>[_a-zA-Z0-9]+)$', 'messagedebugtable'),
)
