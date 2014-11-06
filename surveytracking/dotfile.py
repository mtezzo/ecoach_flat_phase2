import itertools
from surveytracking import pages_from_path

def dict_to_dot(options):
    attrs = ','.join("%s=%s" % (k, v) for k, v in options.items())
    return '[%s]' % attrs

def quote(s):
    return '"%s"' % (s.replace('"', '\\"'))

class DotObject(object):
    def options(self):
        return {}
    
    def to_dot(self):
        components = [self.name]
        options = self.options()
        if options:
            components.append(dict_to_dot(options))
        return '%s;' % ' '.join(components)

class Graph(object):
    def __init__(self, name=""):
        self.name = name
        self.edges = set()
        self.nodes = set()
        self.edgestyle = {}
        self.nodestyle = {}
    
    def styles_to_dot(self):
        styles = []
        if self.edgestyle:
            styles.append("edge %s" % dict_to_dot(self.edgestyle))
        if self.nodestyle:
            styles.append("node %s" % dict_to_dot(self.nodestyle))
        return styles
    
    def to_dot(self):
        dotted = lambda s: (do.to_dot() for do in s)
        return "digraph %s {\n\t%s\n}" % (self.name, '\n\t'.join(
            itertools.chain(self.styles_to_dot(), dotted(self.edges),
                dotted(self.nodes))))

class Node(DotObject):
    def __init__(self, name):
        self.name = name
    

class Edge(DotObject):
    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to
    
    @property
    def name(self):
        return '%s -> %s' % (self.from_, self.to)
    

class PageEdge(Edge):
    def __init__(self, from_page, to_page):
        self.from_page = from_page
        self.to_page = to_page
        self.from_ = 'page_' + from_page.id
        if to_page:
            self.to = 'page_' + to_page.id
        else:
            self.to = 'None'

class ConditionalEdge(PageEdge):
    def __init__(self, from_page, to_page, condition):
        super(ConditionalEdge, self).__init__(from_page, to_page)
        self.condition = condition
    
    def options(self):
        opts = dict(super(ConditionalEdge, self).options())
        opts['label'] = quote(self.condition.replace('\n', '\\n'))
        return opts
    

class PageNode(Node):
    def __init__(self, page):
        super(PageNode, self).__init__("page_" + page.id)
        self.page = page
    
    def options(self):
        opts = dict(super(PageNode, self).options())
        label = quote('\\n'.join(self.page.characteristics))
        if label == '""' and self.page.names:
            label = '"[%s]"' % list(self.page.names)[0]
        opts['label'] = label
        return opts
    

def page_with_name(pages, name):
    try:
        return [page for page in pages if name in page.names][0]
    except IndexError:
        return None

def survey_to_dot(survey_path, dictionary):
    graph = Graph()
    pages = pages_from_path(survey_path, dictionary)
    previous_page = None
    
    graph.nodestyle['shape'] = 'record'
    
    for page in pages:
        n = PageNode(page)
        graph.nodes.add(n)
        absolute_goto_exists = False
        for c in page.goto_conditions():
            goto_page = page_with_name(pages, c.destination)
            ce = ConditionalEdge(page, goto_page, c.condition)
            graph.edges.add(ce)
            if c.condition == '( True )':
                absolute_goto_exists = True
            if c.command.tag == 'goto' and not c.command.get('goto'):
                absolute_goto_exists = True
        if previous_page and not absolute_goto_exists:
            e = PageEdge(previous_page, page)
            graph.edges.add(e)
        previous_page = page
    
    return graph.to_dot()
