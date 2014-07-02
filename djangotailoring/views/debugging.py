import os

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe

from djangotailoring import getsubjectloader
from djangotailoring import getproject, TailoringRequest

class MessageDocRow(object):
    
    def __init__(self, command, selected, limited, depth=0):
        self.depth = depth
        self.command = command
        self.selected = selected == u'true'
        self.limited = limited == u'true'
        self.content = ''
        self.msgid = ''
        self.name = ''
        self.limit = ''
        self.note = ''
        self.logic = ''
        self.orderby = ''
        self.children = []
    
    def apply_visibility_attr(self, parent_visible=True):
        self.visible = self.selected and not self.limited and parent_visible
        for child in self.children:
            child.apply_visibility_attr(self.visible)
    
    @classmethod
    def for_element(cls, elem, depth=0):
        row = cls(elem.tag, elem.get('selected'), elem.get('limited'), depth)
        try:
            row.content = elem.find('./content').text
        except AttributeError:
            pass
        row.logic = elem.get('if', '')
        row.msgid = elem.get('msgid', '')
        row.name = elem.get('name', '')
        row.limit = elem.get('limit', '')
        row.orderby = elem.get('orderby', '')
        try:
            row.note = elem.find('./note').text
        except AttributeError:
            pass
        for child in elem.findall('./subelements/*'):
            row.children.append(MessageDocRow.for_element(child, depth+1))
        return row



def annotation_for_row(row):
    annotations = []
    if row.selected:
        annotations.append('s')
    if row.limited:
        annotations.append('l')
    if row.visible:
        annotations.append('v')
    return ' '.join(annotations)

def css_class_for_row(row):
    classes = [
        'notselected' if not row.selected else None,
        'limited' if row.limited else None,
        'notvisible' if not row.visible else None,
        row.command
    ]
    return ' '.join(cls for cls in classes if cls is not None)


def command_cell(row):
    depthdots = '..' * row.depth
    depthdots = '<span class="depthdots">%s</span>' % depthdots
    command = row.command
    limitstr = (' limit(%s)' % row.limit) if row.limit else ''
    return mark_safe('%s%s%s' % (depthdots, command, limitstr))

class SectionTable(object):
    
    def __init__(self, sectionel):
        def walker(row):
            yield row
            for row in row.children:
                for walked in walker(row):
                    yield walked
        self.toplevel = [MessageDocRow.for_element(sectionel)]
        for row in self.toplevel:
            row.apply_visibility_attr()
        self.rows = [row for toplevelrow in self.toplevel for row in walker(toplevelrow)]
    
    def as_bunches(self):
        bunches = []
        for row in self.rows:
            bunches.append(
                dict(
                    msgid=row.msgid,
                    command=command_cell(row),
                    name=row.name,
                    logic=row.logic,
                    message=mark_safe(row.content),
                    note=row.note,
                    flags=annotation_for_row(row),
                    cssclass=css_class_for_row(row),
                )
            )
        return bunches



def messagedebugtable(request, docpath, sectionname):
    try:
        subjectid = request.GET.get('subject', None)
        subject, e = getsubjectloader().get_subject(subjectid)
        treq = TailoringRequest(getproject(), '%s.messages' % docpath, subject,
            None)
        pipeline = treq.pipeline_for_section(sectionname)
        selected_tree, errors = pipeline.select_phase()
        e.extend(errors)
        doctable = SectionTable(selected_tree)
        rows = doctable.as_bunches()
        title = "%s (for ID %s)" % (os.path.basename(docpath), subjectid)
    except:
        raise Http404
    return render_to_response("djangotailoring/message_doc_table.html",
        dict(rows=rows, errors=e, title=title), context_instance=RequestContext(request))

