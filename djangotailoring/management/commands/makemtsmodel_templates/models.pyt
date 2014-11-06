from django.db import models
from djangotailoring.models import SubjectData
{% for choicesname, choicesset in choices.items %}
{{ choicesname|safe }} = {{ choicesset|safe }}
{% endfor%}
{% for classname, fields in modelclasses.items %}
class {{ classname|safe }}(SubjectData):
{% for field in fields %}    {{ field|safe }}
{% empty %}    pass
{% endfor %}{% endfor %}
