import os.path
import re
import cgi
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import traceback

from django import template
from django.template.defaultfilters import stringfilter
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from tailoring2.render import tostring

from djangotailoring.project import getprojectroot
from djangotailoring.tailoringrequest import TailoringRequestError
from djangotailoring.util import nowrapper

register = template.Library()

register.filter(stringfilter(nowrapper))

def errors2html(errors):
    if not errors:
        return ''
    errorshtml = [('<li>%s</li>' % cgi.escape(repr(error)))
                  for error in errors]
    return '<ul class="tailoringerrors">%s</ul>' % '\n'.join(errorshtml)

def get_t2debug(context):
    try:
        return context.t2debug
    except AttributeError:
        pass
    try:
        return settings.TAILORING2_DEBUG
    except AttributeError:
        pass
    return False

class RenderRequestSection(template.Node):
    def __init__(self, request, sectionname, nowrapper=False):
        self.request = template.Variable(request)
        self.sectionname = sectionname
        self.nowrapper = nowrapper
    
    def render(self, context):
        t2debug = get_t2debug(context)
        sectionname = self.sectionname
        try:
            request = self.request.resolve(context)
            if sectionname[0] in ('"', "'"):
                sectionname = sectionname.strip(sectionname[0])
            else:
                sectionname = template.Variable(sectionname).resolve(context)
            result, errors = request.render_section(sectionname)
            resultxml = tostring(result)
            if self.nowrapper:
                output = nowrapper(resultxml)
            else:
                output = resultxml
            if t2debug and errors:
                output += errors2html(errors)
            if t2debug:
                project_root = getprojectroot()
                user = template.Variable('user').resolve(context)
                try:
                    tailoringid = user.get_profile().tailoringid
                except AttributeError:
                    return output
                docpath = request.docpath[len(project_root)+1:-len('.messages')]
                try:
                    url = reverse('djangotailoring.views.messagedebugtable',
                        kwargs=dict(docpath=docpath, sectionname=sectionname))
                except NoReverseMatch:
                    pass
                else:
                    tag = '<a href="%s?subject=%s" class="%s">%s</a>'
                    docname = os.path.basename(docpath)
                    label = '<p>%s /</p><p>%s</p>' % (docname, sectionname)
                    output += tag % (url, tailoringid, 'debuglink', label.encode('utf-8'))
            return output
        except TailoringRequestError, e:
            if t2debug:
                return '<div class="tailoringerror">%s</div>' % e.message
        except Exception:
            if t2debug:
                out = StringIO()
                traceback.print_exc(file=out)
                return "<pre>%s</pre>" % out.getvalue()
        return ''
    

class SetTailoringDebug(template.Node):
    def __init__(self, onoff):
        self.onoff = onoff
    
    def render(self, context):
        context.t2debug = self.onoff == 'on'
        return ''
    

@register.tag
def render_section(parser, token):
    tag_name = 'render_section'
    myargs = token.split_contents()[1:]
    if len(myargs) < 2:
        raise template.TemplateSyntaxError, '%r tag requires at least two arguments' % tag_name
    request, sectionname = myargs[:2]
    nowrap = False
    if len(myargs) > 2:
        if myargs[-1] == 'nowrap':
            nowrap = True
        else:
            raise template.TemplateSyntaxError, '%r tag has only one optional argument: nowrap' % tag_name
    if sectionname[0] in ('"', "'") and sectionname[0] != sectionname[-1]:
        raise template.TemplateSyntaxError, "%r tag's section name argument should be in matched quotes" % tag_name
    return RenderRequestSection(request, sectionname, nowrap)


@register.tag
def render_section_nowrap(parser, token):
    try:
        tag_name, request, sectionname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires exactly two arguments' % token.contents.split()[0]
    if sectionname[0] in ('"', "'") and sectionname[0] != sectionname[-1]:
        raise template.TemplateSyntaxError, "%r tag's section name argument should be in matched quotes" % tag_name
    return RenderRequestSection(request, sectionname, True)

@register.tag
def tailoring2_debug(parser, token):
    try:
        tag_name, onoff = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires one argument: `on` or `off`' % token.contents.split()[0]
    onoff = onoff.lower()
    if onoff not in ('on', 'off'):
        raise template.TemplateSyntaxError, '%r tag requires one argument: `on` or `off`' % token.contents.split()[0]
    return SetTailoringDebug(onoff)
