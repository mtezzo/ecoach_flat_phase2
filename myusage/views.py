from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.conf import settings
from djangotailoring.views import TailoredDocView
from djangotailoring.project import getsubjectloader
from mynav.nav import main_nav, tasks_nav
from .steps import steps_nav
from mylogger.models import ELog

# Create your views here.

@staff_member_required
def your_tail_view(request):
    headers = [f.name for f in ELog._meta.fields]
    tail = ELog.objects.filter(who=request.user).order_by('-mwhen').values_list()[0:20]
    return render(request, 'myusage/log_tail.html', {
        "main_nav": main_nav(request.user, 'staff_view'),
        "tasks_nav": tasks_nav(request.user, 'usage'),
        "steps_nav": steps_nav(request.user, 'your_tail'),
        "headers": headers,
        "tail": tail
    })

@staff_member_required
def everyone_tail_view(request):
    headers = [f.name for f in ELog._meta.fields]
    tail = ELog.objects.order_by('-mwhen').values_list()[0:20]
    return render(request, 'myusage/log_tail.html', {
        "main_nav": main_nav(request.user, 'staff_view'),
        "tasks_nav": tasks_nav(request.user, 'usage'),
        "steps_nav": steps_nav(request.user, 'eveyone_tail'),
        "headers": headers,
        "tail": tail
    })

@staff_member_required
def usage_vector_view(request):
    """
    comps = ELog.objects.all().values_list('url', 'category', 'action', 'label', 'value')
    vectors = []
    for cc in comps:
        vectors.append('..jared..'.join([unicode(aa) for aa in cc]))
    uniqs = set(vectors)
    vcnts = []
    for qq in uniqs:
        vcnts.append([vectors.count(qq)] + qq.split('..jared..'))
    """
    from django.db import connection
    query = """
        SELECT 
            count(ee.id) as cnt, 
            ee.url,
            ee.category, 
            ee.action, 
            ee.label, 
            ee.value 
        from mydata_source1 as ss
        inner join mylogger_elog as ee on
            ss.user_id = ee.who
        where Reg_Enrolled=1
        group by concat(ee.url, ee.category, ee.action, ee.label, ee.value) 
        order by ee.url, ee.category, ee.action, cnt desc
    """
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    vcnts = [[rr[0], rr[1], rr[2], rr[3], rr[4], rr[5]] for rr in res] 
    return render(request, 'myusage/usage_vector.html', {
        "main_nav": main_nav(request.user, 'staff_view'),
        "tasks_nav": tasks_nav(request.user, 'usage'),
        "steps_nav": steps_nav(request.user, 'usage_vector'),
        "vectors": vcnts
    })




