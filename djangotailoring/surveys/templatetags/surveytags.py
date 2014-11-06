try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import traceback

from django import template

from djangotailoring.templatetags.tailoring2tags import (get_t2debug,
    nowrapper, tostring, errors2html)

register = template.Library()

class RenderSurveySegment(template.Node):
    def __init__(self, request):
        self.request = template.Variable(request)
    
    def render(self, context):
        t2debug = get_t2debug(context)
        try:
            request = self.request.resolve(context)
            result, errors = request.render_segment()
            resultxml = nowrapper(tostring(result), 'document')
            if t2debug and errors:
                resultxml += errors2html(errors)
            return resultxml
        except Exception, e:
            if t2debug:
                out = StringIO()
                traceback.print_exc(file=out)
                return "<pre>%s</pre>" % out.getvalue()
            return ''
    

@register.tag
def render_survey_segment(parser, token):
    try:
        tag_name, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires a survey chunk argument' % token.contents.split()[0]
    return RenderSurveySegment(request)

