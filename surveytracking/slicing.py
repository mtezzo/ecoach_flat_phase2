import operator

from allnames import get_names
from formatutils import command_iterator, get_next_command, parent_map
from formatutils import WHOLE_CONTAINERS, build_parallel
from itertools import izip, tee, chain

BEFORE = -1
AFTER = 1

def segment_tree(tree, from_node, to_node):
    return build_parallel(tree, from_node, to_node)

def pairwise_padded(iterator, pad=None):
    one, two = tee(iterator, 2)
    one, two = chain([None], one), chain(two, [None])
    return izip(one, two)

class SurveySlicer(object):
    
    def __init__(self, tree):
        self.tree = tree
        self.parentage = parent_map(tree)
        self.decision_points = set()
        self.decision_tests = [self.is_pagebreak, self.is_section]
    
    def find_decision_points(self):
        decision_responses = frozenset([BEFORE, AFTER])
        for command in command_iterator(self.tree):
            for test in self.decision_tests:
                response = test(command)
                if response in decision_responses:
                    self.add_decision_point(command, response)
    
    def add_decision_point(self, element, beforeorafter=BEFORE):
        self.decision_points.add((element, beforeorafter))
    
    def cut_points(self):
        parentage = self.parentage
        cut_points = set()
        self.find_decision_points()
        for decision_point, beforeorafter in self.decision_points:
            parent = parentage[decision_point]
            while parent is not None and parent.tag not in WHOLE_CONTAINERS:
                parent = parentage[parent]
            cut_point = parent if parent is not None else decision_point
            if beforeorafter == AFTER:
                cut_point = get_next_command(cut_point, parentage)
            if cut_point is not None:
                cut_points.add(cut_point)
        return [cp for cp in self.tree.getiterator() if cp in cut_points]
    
    def tree_segments(self):
        cut_points = self.cut_points()
        return [segment_tree(self.tree, from_, to_) for from_, to_ in
            pairwise_padded(cut_points)]
    
    def is_section(self, command):
        if command.tag == 'section':
            return AFTER
        return None
    
    def is_pagebreak(self, command):
        if command.tag == 'pagebreak':
            return AFTER
        return None
    

class OnePerPageSlicer(SurveySlicer):
    
    def __init__(self, tree):
        super(OnePerPageSlicer, self).__init__(tree)
        self.decision_tests.append(self.is_whole_container)
    
    def is_whole_container(self, command):
        if command.tag in WHOLE_CONTAINERS:
            return AFTER
        return None
    

class ClassicSlicer(SurveySlicer):
    
    def __init__(self, tree):
        super(ClassicSlicer, self).__init__(tree)
        self.seennames = set()
        self.destinations = set()
        self.decision_tests.extend([self.in_destinations, self.in_seennames,
            self.is_goto, self.is_section,
            self.add_seennames])
    
    def parent_container(self, element):
        parent = element
        while parent is not None:
            parent = self.parentage.get(parent, None)
            if parent is not None and parent.tag in WHOLE_CONTAINERS:
                return parent
        return None
    
    def add_decision_point(self, element, beforeorafter=BEFORE):
        super(ClassicSlicer, self).add_decision_point(element, beforeorafter)
        self.seennames.clear()
        # in the case that the break comes before the current command, and
        # the current command is a member of an unbreakable container (a
        # question, in this instance), it should remember that the current
        # characteristic is still 'seen'.
        if beforeorafter == BEFORE:
            container = self.parent_container(element)
            if container is not None:
                self.add_seennames(container)
    
    def in_destinations(self, command):
        name = command.get('name')
        if name is not None and name in self.destinations:
            return BEFORE
        return None
    
    def in_seennames(self, command):
        if get_names(command.get('if')) & self.seennames and \
           command.tag != 'validate':
            return BEFORE
        return None
    
    def is_goto(self, command):
        if 'goto' in command.attrib:
            goto = command.get('goto').strip()
            if goto != '':
                self.destinations.add(goto)
                return AFTER
        return None
    
    def add_seennames(self, command):
        char = command.get('characteristic')
        if char is not None:
            self.seennames.add(char)
        return None
    

class DependencySlicer(ClassicSlicer):
    
    def __init__(self, tree, dependencymap={}):
        self.depmap = dependencymap
        super(DependencySlicer, self).__init__(tree)
        # place this test before the add_seennames 'test'
        self.decision_tests.insert(-1, self.in_dependencymap)
    
    def _reduce_to_bare_dependencies(self, names):
        if not names: return set()
        depmap = self.depmap
        return reduce(operator.or_, (depmap.get(n, set([n])) for n in names))
    
    def in_dependencymap(self, command):
        char = command.get('characteristic')
        ifdeps = self._reduce_to_bare_dependencies(get_names(
            command.get('if')))
        if ifdeps & self.seennames and command.tag != 'validate':
            return BEFORE
        return None
    

# def find_decision_points_opp(tree):
#     points = set()
#     for command in command_iterator(tree):
#         if command.tag in WHOLE_CONTAINERS:
#             points.add((command, AFTER))
#     return points
# 
# def find_decision_points(tree):
#     points = set()
#     seennames = set()
#     destinations = set()
#     def add_point(elem, beforeorafter):
#         points.add((elem, beforeorafter))
#         seennames.clear() # is this necessary and/or harmful?
#     for command in command_iterator(tree):
#         characteristic = command.get('characteristic')
#         if characteristic and characteristic in destinations:
#             add_point(command, BEFORE)
#         if get_names(command.get('if')) & seennames and command.tag != 'validate':
#             add_point(command, BEFORE)
#         if 'goto' in command.attrib:
#             goto = command.get('goto').strip()
#             if goto != '':
#                 destinations.add(goto)
#                 add_point(command, AFTER)
#         if command.tag == 'pagebreak':
#             add_point(command, AFTER)
#         if command.tag == 'section':
#             add_point(command, AFTER)
#         seennames.add(command.get('characteristic'))
#     return points
# 
# def find_cut_points(tree, decision_points):
#     parentage = parent_map(tree)
#     cut_points = set()
#     for decision_point, beforeorafter in decision_points:
#         parent = parentage[decision_point]
#         while parent is not None and parent.tag not in WHOLE_CONTAINERS:
#             parent = parentage[parent]
#         cut_point = parent if parent is not None else decision_point
#         if beforeorafter == AFTER:
#             cut_point = get_next_command(cut_point, parentage)
#         if cut_point is not None:
#             cut_points.add(cut_point)
#     return [cp for cp in tree.getiterator() if cp in cut_points]
# 
# def make_tree_segments(tree, cut_points):
#     return [segment_tree(tree, from_, to_) for from_, to_ in
#         zip([None] + cut_points, cut_points + [None])]
# 