import itertools
from tailoring2.common import ET
from tailoring2.util import Bunch

MSGID_SERIAL = 0

def get_msgid():
    global MSGID_SERIAL
    MSGID_SERIAL += 1
    return 'missing-%d' % MSGID_SERIAL

WHOLE_CONTAINERS = frozenset(['question', 'matrix', 'group'])

def command_iterator(tree):
    for elem in tree.getchildren():
        yield elem
        for container in elem.findall('subelements'):
            for child in command_iterator(container):
                yield child

def tree_has_content(tree):
    for elem in tree.getiterator():
        if elem.text is not None and len(elem.text.strip()) > 0:
            return True
    return False

def _parent_map(command_element, parent=None):
    my_map = {command_element: parent}
    for container in command_element.findall('subelements'):
        for child in container:
            my_map.update(_parent_map(child, command_element))
    return my_map

def parent_map(command_tree):
    if command_tree.tag == 'document':
        m = {}
        for child in command_tree.getchildren():
            m.update(_parent_map(child))
            m[child] = command_tree
        m[command_tree] = None
        return m
    return _parent_map(command_tree)

def get_next_command(this, parent_map):
    if this is None:
        return None
    parent = parent_map[this]
    if parent is None:
        return None
    if parent.tag == 'document':
        children = parent.getchildren()
    else:
        children = []
        for subelements in parent.findall('subelements'):
            children.extend(subelements.getchildren())
    index = children.index(this)
    if index >= len(children) - 1:
        return get_next_command(parent, parent_map)
    else:
        return children[index + 1]
    return None

def node_in_subtree(node, subtree):
    for elem in subtree.getiterator():
        if elem == node:
            return True
    return False

def msgidify(tree):
    skipthese = frozenset(('document','subelements','content'))
    for elem in tree.getiterator():
        if elem.tag not in skipthese and 'msgid' not in elem.attrib:
            elem.attrib['msgid'] = get_msgid()
    return tree

def first_command_of_type(tree, types):
    for command in command_iterator(tree):
        if command.tag in types:
            return command
    return None

def msgids_in_tree(tree, types=None):
    if types is not None:
        s = (command.get('msgid') for command in command_iterator(tree)
            if command.tag in types)
    else:
        s = (command.get('msgid') for command in command_iterator(tree))
    return [m for m in s if m is not None]

def enclosing_command_of_type(tree, command, tagname):
    parentage = parent_map(tree)
    parent = parentage[command]
    while parent is not None:
        if parent.tag == tagname:
            return parent
        parent = parentage[parent]
    return None

def build_parallel(root, from_node, to_node):
    """return a copy of an element tree with segments before from_node and
    to_node and after removed.

    If from_node and to_node are None, return a deep copy of the root node.
    
    TODO items for testing:
        - is this always a deep copy under CPython ET, cET, and lxml?
        - is this always a deep copy under Jython ET?
        - can the copy handle a tree nested, say, 200 elements deep?
            (sys.getrecursionlimit() is 1000 on OS X Leopard + Jython2.5/CPython2.6)
        - full deep node copy when from_ and to_ are None

    TODO refactor:
        - move this into tailoring2.elementutil
        - make a new function in elementutil called copy_element() using one of
            these forms:

            def copy_element(root):
                return build_parallel(root, None, None)
                
            import functools
            copy_element_2 = functools.partial(build_parallel, from_node=None, to_node=None)        
    """
    newtree = ET.Element('parent')
    noticeboard = Bunch(startfound=from_node is None, endfound=False)
    def clone_tree_branch(parent, branch, nb):
        tagattr = branch.get('tag', None)
        me = ET.SubElement(parent, branch.tag, branch.attrib)
        if tagattr:
            me.set('tag', tagattr)
        me.text = branch.text
        me.tail = branch.tail
        for child in branch:
            if child == from_node:
                nb.startfound = True
            if child == to_node:
                nb.endfound = True
                return
            
            if not nb.startfound and node_in_subtree(from_node, child):
                clone_tree_branch(me, child, nb)
            elif nb.startfound and not nb.endfound:
                clone_tree_branch(me, child, nb)
    clone_tree_branch(newtree, root, noticeboard)
    return newtree[0]

def tree_segment(root, from_node, to_node):
    # XXX: Don't use. This likely works, but is slow. Consider build_parallel
    # above
    """return a copy of an element tree with segments before from_node and
    to_node and after removed."""
    # To accomplish this task, we first copy the tree. Then we go about
    # removing irrelevant portions of the tree.
    # To do that, we recursively walk through the tree.
    #   - If we've yet to find from_node, and it does not exist in the current
    #     branch, we remove the branch from the parent.
    #   - If we've yet to find from_node, and it does exist in the current
    #     branch, keep it, and recurse.
    #   - If we find from_node, note it, and keep recursing.
    #   - If to_node is None, return
    #   - If we haven't found to_node, and it's not in the current branch,
    #     move on.
    #   - If we haven't found to_node, and it's in the current branch, recurse
    #   - If we've found to_node, start removing everything we encounter on
    #     the way back out.
    import copy
    newtree = copy.deepcopy(root)
    noticeboard = Bunch(startfound=from_node is None, endfound=False)
    for old, new in itertools.izip(root.getiterator(), newtree.getiterator()):
        if from_node == old:
            from_node = new
        elif to_node == old:
            to_node = new
            break
    class DoneWithFun(Exception):
        pass
    def check_tree_branch(branch, nb):
        for child in branch[:]:
            if child == from_node:
                nb.startfound = True
                if to_node is None:
                    raise DoneWithFun()
            if child == to_node:
                nb.endfound = True
                
            if not nb.startfound:
                if node_in_subtree(from_node, child):
                    check_tree_branch(child, nb)
                else:
                    branch.remove(child)
            if not nb.endfound:
                if node_in_subtree(to_node, child):
                    check_tree_branch(child, nb)
            else:
                branch.remove(child)
        
    try:
        check_tree_branch(newtree, noticeboard)
    except DoneWithFun:
        pass
    return newtree

# gratuitiously adapted from the effbot original at:
# http://effbot.python-hosting.com/file/stuff/sandbox/elementlib/clone.py
def make_factory(elem, from_node, to_node):
    b = Bunch(startfound=False, endfound=False)
    if from_node is None:
        b.startfound = True

    def generate_elem(append, elem, level):
        if elem == from_node:
            b.startfound = True
        if elem == to_node:
            b.endfound = True
            return
        var = "e" + str(level)
        arg = repr(elem.tag)
        tagattr = None
        if elem.attrib:
            tagattr = elem.attrib.pop('tag', None)
            arg += ", **%r" % elem.attrib
        if level == 1:
            append(" e1 = Element(%s)" % arg)
        else:
            append(" %s = SubElement(e%d, %s)" % (var, level-1, arg))
        if tagattr is not None:
            append(" %s.set('tag', %r)" % (var, tagattr))
        if b.startfound:
            if elem.text:
                append(" %s.text = %r" % (var, elem.text))
        if elem.tail:
            append(" %s.tail = %r" % (var, elem.tail))
        for e in elem:
            if b.startfound or node_in_subtree(from_node, e):
                generate_elem(append, e, level+1)
            if b.endfound:
                return
    # generate code for a function that creates a tree
    output = ["def element_factory():"]
    generate_elem(output.append, elem, 1)
    output.append(" return e1")
    # setup global function namespace
    namespace = {"Element": ET.Element, "SubElement": ET.SubElement}
    # create function object
    exec "\n".join(output) in namespace
    return namespace["element_factory"]

def eq_trees(t1, t2):
    import itertools
    class Difference(Exception): pass
    try:
        for e1, e2 in itertools.izip(t1.getiterator(), t2.getiterator()):
            if e1.tag != e2.tag or e1.attrib != e2.attrib:
                raise Difference()
            for e in (e1, e2):
                if e.text is None:
                    e.text = ''
                if e.tail is None:
                    e.tail = ''
            if e1.text.strip() != e2.text.strip() or \
               e1.tail.strip() != e2.tail.strip():
                raise Difference()
            if len(e1) != len(e2):
                raise Difference()
    except (Difference, AttributeError):
        return False
    return True

def testsegment():
    a = ET.XML("""
    <a>
      <b>one</b>
      <c>two</c>
      <d>
        <e>three</e>
      </d>
      <f>four</f>
    </a>
    """)
    b = a.getchildren()[0]
    c = a.getchildren()[1]
    d = a.getchildren()[2]
    e = d.getchildren()[0]
    f = a.getchildren()[3]
    
    t1 = tree_segment(a, b, d)
    t2 = tree_segment(a, c, e)
    t3 = tree_segment(a, None, b)
    t4 = tree_segment(a, e, None)
    
    assert eq_trees(t1, ET.XML("""<a><b>one</b><c>two</c></a>"""))
    assert eq_trees(t2, ET.XML("""<a><c>two</c><d></d></a>"""))
    assert eq_trees(t3, ET.XML("""<a></a>"""))
    assert eq_trees(t4, ET.XML("""<a><d><e>three</e></d><f>four</f></a>"""))

def testbuild_parallel():
    a = ET.XML("""
    <a>
      <b>one</b>
      <c>two</c>
      <d>
        <e>three</e>
      </d>
      <f>four</f>
    </a>
    """)
    b = a.getchildren()[0]
    c = a.getchildren()[1]
    d = a.getchildren()[2]
    e = d.getchildren()[0]
    f = a.getchildren()[3]
    
    t1 = build_parallel(a, b, d)
    t2 = build_parallel(a, c, e)
    t3 = build_parallel(a, None, b)
    t4 = build_parallel(a, e, None)
    
    assert eq_trees(t1, ET.XML("""<a><b>one</b><c>two</c></a>"""))
    assert eq_trees(t2, ET.XML("""<a><c>two</c><d></d></a>"""))
    assert eq_trees(t3, ET.XML("""<a></a>"""))
    ET.dump(t4)
    assert eq_trees(t4, ET.XML("""<a><d><e>three</e></d><f>four</f></a>"""))

def testfactory():
    a = ET.XML("""
    <a>
      <b>one</b>
      <c>two</c>
      <d>
        <e>three</e>
      </d>
      <f>four</f>
    </a>
    """)
    b = a.getchildren()[0]
    c = a.getchildren()[1]
    d = a.getchildren()[2]
    e = d.getchildren()[0]
    f = a.getchildren()[3]
    
    t1 = make_factory(a, b, d)()
    t2 = make_factory(a, c, e)()
    t3 = make_factory(a, None, b)()
    t4 = make_factory(a, e, None)()
    
    assert eq_trees(t1, ET.XML("""<a><b>one</b><c>two</c></a>"""))
    assert eq_trees(t2, ET.XML("""<a><c>two</c><d></d></a>"""))
    assert eq_trees(t3, ET.XML("""<a></a>"""))
    assert eq_trees(t4, ET.XML("""<a><d><e>three</e></d><f>four</f></a>"""))

def testpairs():
    a = ET.XML("""
    <a>
      <b>one</b>
      <c>two</c>
      <d>
        <e>three</e>
      </d>
      <f>four</f>
    </a>
    """)
    b = a.getchildren()[0]
    c = a.getchildren()[1]
    d = a.getchildren()[2]
    e = d.getchildren()[0]
    f = a.getchildren()[3]
    
    t1 = make_factory(a, b, d)()
    t2 = make_factory(a, c, e)()
    t3 = make_factory(a, None, b)()
    t4 = make_factory(a, e, None)()
    
    p1 = build_parallel(a, b, d)
    p2 = build_parallel(a, c, e)
    p3 = build_parallel(a, None, b)
    p4 = build_parallel(a, e, None)
    
    assert eq_trees(t1, p1)
    assert eq_trees(t2, p2)
    assert eq_trees(t3, p3)
    assert eq_trees(t4, p4)
    

def gettext(elem):
    text = [elem.text or ""]
    for e in elem:
        text.append(gettext(e))
        if e.tail:
            text.append(e.tail)
    return "".join(text)
