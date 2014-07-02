# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from {{ app_name }}.survey import {{ survey_view_classes|join:", " }}

{% for survey_name, survey_view_class in survey_view_pairs %}
def {{ survey_name }}_survey(request, msgid):
    view = {{ survey_view_class }}({{ survey_name }}_survey)
    return view(request, msgid)
{% endfor %}
