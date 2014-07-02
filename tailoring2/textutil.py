# COPYRIGHT (c) 2008
# THE REGENTS OF THE UNIVERSITY OF MICHIGAN
# ALL RIGHTS RESERVED
#
# PERMISSION IS GRANTED TO USE, COPY, CREATE DERIVATIVE WORKS AND
# REDISTRIBUTE THIS SOFTWARE AND SUCH DERIVATIVE WORKS FOR NONCOMMERCIAL
# EDUCATION AND RESEARCH PURPOSES, SO LONG AS NO FEE IS CHARGED, AND SO
# LONG AS THE COPYRIGHT NOTICE ABOVE, THIS GRANT OF PERMISSION, AND THE
# DISCLAIMER BELOW APPEAR IN ALL COPIES MADE; AND SO LONG AS THE NAME OF
# THE UNIVERSITY OF MICHIGAN IS NOT USED IN ANY ADVERTISING OR PUBLICITY
# PERTAINING TO THE USE OR DISTRIBUTION OF THIS SOFTWARE WITHOUT SPECIFIC,
# WRITTEN PRIOR AUTHORIZATION.
#
# THIS SOFTWARE IS PROVIDED AS IS, WITHOUT REPRESENTATION FROM THE
# UNIVERSITY OF MICHIGAN AS TO ITS FITNESS FOR ANY PURPOSE, AND WITHOUT
# WARRANTY BY THE UNIVERSITY OF MICHIGAN OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE REGENTS OF THE
# UNIVERSITY OF MICHIGAN SHALL NOT BE LIABLE FOR ANY DAMAGES, INCLUDING
# SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, WITH RESPECT TO
# ANY CLAIM ARISING OUT OF OR IN CONNECTION WITH THE USE OF THE SOFTWARE,
# EVEN IF IT HAS BEEN OR IS HEREAFTER ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGES.

"""Helper functions for chunks of text -- that is, sentences and
sentence fragments, with caps, punctuation, etc. -- as opposed to on any
old strings.
"""

import re
import itertools
import string
from HTMLParser import HTMLParser


# ------------------------------------------------------------

# run of whitespace characters
WHITESPACE_RUN_RE = re.compile(r'[ \n\r\t]+')

# an alphanumeric, then a space, then a punctuation char
LETTER_SPACE_PUNC = re.compile(r'(\w+)( {1})([.,!?])')

def trim_whitespace(text):
    """Given a chunk of text (a string), remove the excess whitespace (the kind a browser
    wouldn't display). Attempt to intelligently string together words and punctuation.
    
    >>> trim_whitespace(" hello ")
    'hello'
    >>> trim_whitespace("Hello , world ! ")
    'Hello, world!'
    >>> trim_whitespace("Hello    ,    world    !    ")
    'Hello, world!'
    >>> trim_whitespace("Hello, world!")
    'Hello, world!'
    >>> trim_whitespace("???")
    '???'
    >>> trim_whitespace(_EXAMPLE1)
    'We are here to help. As members of the Project Quit team at Group Health Cooperative, it is our pleasure to provide you with what you need to take control of your health.'
    >>> trim_whitespace('We are here to help. As members...')
    'We are here to help. As members...'
    >>> trim_whitespace('!We  are  here  to  help .    As members , is it awfully    important to belong  ?')
    '!We are here to help. As members, is it awfully important to belong?'
    >>> trim_whitespace('')
    ''
    >>> trim_whitespace(None)
    Traceback (most recent call last):
        ...
    AttributeError: 'NoneType' object has no attribute 'strip'
    >>> trim_whitespace('?#$^%%^@')
    '?#$^%%^@'
    """
    text = text.strip()
    text = WHITESPACE_RUN_RE.sub(' ', text)
    text = LETTER_SPACE_PUNC.sub(r'\1\3', text)
    return text


# ------------------------------------------------------------
# get plain text out of html-style marked-up text
# ... copied from mpower/engine/character_count.py

class TextGetter(HTMLParser):
    """World's lamest HTMLParser subclass just accumulates data elements
    in ivar list 'data' (for later count by client)
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []

    def handle_data(self, d):
        self.data.append(d)


def get_text(s, interpolate_spaces=True, strip_whitespace=True):
    """Given string 's' that may contain tags, return the text between
    those tags. Ignore everything in the markup except the text nodes.
    Optionally insert a single space between data elements. Strip
    all-whitespace text nodes by default.
    
    >>> get_text('hello, world!')
    'hello, world!'
    >>> get_text('<p>hello</p>')
    'hello'
    >>> get_text('goodbye <i>cruel</i> world')
    'goodbye cruel world'
    >>> get_text('<p><p>hello</p><p>goodbye</p></p>')
    'hello goodbye'
    >>> get_text('<p><p>hello</p><p>goodbye</p></p>', interpolate_spaces=False)
    'hellogoodbye'
    >>> get_text('<p>hello, <b>world!</b> try not to blow it <i>this</i> time.</p>')
    'hello, world! try not to blow it this time.'
    >>> get_text('   <p>   hello   </p>   ')
    '   hello   '
    >>> get_text('   <p>   hello   </p>   ', strip_whitespace=False)
    '      hello      '
    >>> get_text('\\n<p>hello</p>\\n')
    'hello'
    >>> get_text('\\n<p>hello</p>\\n', strip_whitespace=False)
    '\\nhello\\n'
    """
    textgetter = TextGetter()
    textgetter.feed(s)
    textgetter.close()
    if strip_whitespace:
        textgetter.data = [item for item in textgetter.data if not item.isspace()]
    if interpolate_spaces:
        return space_join(textgetter.data)
    else:
        return ''.join(textgetter.data)


def get_text_len(s, strip_whitespace=True):
    """given a string 's' that may contain tags, return the length ignoring tags.
    Optionally, and by default, strip leading and trailing whitespace.
    
    >>> get_text_len('hello')
    5
    >>> get_text_len('<b>hello</b>')
    5
    >>> get_text_len('<p>hello, <b>world!</b> try not to blow it <i>this</i> time.</p>')
    43
    >>> get_text_len('   <p>   hello   </p>   ', strip_whitespace=True)
    5
    """
    text = get_text(s)
    if strip_whitespace:
        text = text.strip()
    return len(text)


def padnone(seq):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.
    """
    return itertools.chain(seq, itertools.repeat(None))


# copied directly from standard library's itertool recipes
# except for the padnone() call
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    # without padnone(), if iterable has an odd number of elements, the last
    # element will never be yielded
    b = padnone(b)
    try:
        b.next()
    except StopIteration:
        pass
    return itertools.izip(a, b)

def parwrap(s, skipempty=True):
    """returns a string wrapped in matching parentheses if it's not already.
    If skipempty is True (the default), if `s` is the empty string, it is not
    wrapped in parentheses. Otherwise, a pair of parens will be returned.
    
    >>> parwrap('True')
    '(True)'
    >>> parwrap('(True)')
    '(True)'
    >>> parwrap('(this and that) or theother')
    '((this and that) or theother)'
    >>> parwrap('function(call)')
    '(function(call))'
    >>> parwrap('(True or False) and (False or True)')
    '((True or False) and (False or True))'
    >>> parwrap('')
    ''
    >>> parwrap('', True)
    ''
    >>> parwrap('', False)
    '()'
    """
    if (not s and skipempty) or isparened(s):
        return s
    return '(%s)' % s

def isparened(s):
    """return True iff the string has balanced parentheses and that the first
    parenthesis is paired with the last parenthesis.
    
    >>> isparened('()')
    True
    >>> isparened('(a)')
    True
    >>> isparened('(a()')
    False
    >>> isparened('(a())')
    True
    >>> isparened('(a) and (b)')
    False
    >>> isparened('')
    False
    >>> isparened('a()')
    False
    >>> isparened('(x) * 1')
    False
    """
    if len(s) > 0 and s[0] == '(' and s[-1] == ')':
        count = 0
        length = len(s)
        for i, char in enumerate(s):
            if char in '()':
                count += 1 if char == '(' else -1
                if count == 0:
                    return i == length - 1
    return False

def maybe_append_space(item, advice=None):
    if not advice:
        return item
    if item[-1] in string.whitespace or advice[0] in string.whitespace:
        return item
    return '%s ' % item


def space_join(seq):
    """Given sequence of strings, return a single string of the joined sequence. Intelligently
    insert spaces into the final string.
    
    >>> space_join(['goodbye ', 'cruel', ' world'])
    'goodbye cruel world'
    >>> space_join(['goodbye', 'cruel', 'world'])
    'goodbye cruel world'
    >>> space_join([])
    ''
    >>> space_join(['goodbye'])
    'goodbye'
    >>> space_join([' goodbye', 'cruel', ' world '])
    ' goodbye cruel world '
    """
    spaced = [maybe_append_space(current, advice=next) for current, next in pairwise(seq)]
    return ''.join(spaced)

def conjunctionize_list(conjunction, vals, oxford_comma=True):
    """Produce a list of strings from `vals` with unicode commas in between
    them, and `conjunction` between the final two vals. If oxford_comma is
    True, there will be a comma before the conjunction. The resulting list
    should be ''.join()-able to create an english-like sentence fragment."""
    if not vals or len(vals) == 1:
        return vals
    if len(vals) == 2:
        lst = [vals[0], ' ', conjunction, ' ', vals[1]]
        if oxford_comma:
            lst.insert(1, ',')
        return lst
    lst = []
    extend = lst.extend
    head, tail = vals[:-1], vals[-1]
    for v in head:
        extend([v, ', '])
    if not oxford_comma:
        lst.pop()
        extend([' ']) # remove the last one and drop in a space
    extend([conjunction, ' ', tail])
    return lst

def conjunctionize(conjunction, vals, oxford_comma=True):
    """Join the strings in iterable `vals` by commas, inserting `conjunction`
    before the final string. oxford_comma dictates whether there is a comma
    before the insertion of the conjunction.
    
    >>> numbers = ('one', 'two', 'three')
    >>> conjunctionize('or', numbers)
    'one, two, or three'
    >>> conjunctionize('and', numbers)
    'one, two, and three'
    >>> conjunctionize('or', numbers, oxford_comma=False)
    'one, two or three'
    >>> conjunctionize('and', numbers, oxford_comma=False)
    'one, two and three'
    >>> conjunctionize('or', numbers[:2])
    'one, or two'
    >>> conjunctionize('or', numbers + ('four',))
    'one, two, three, or four'
    """
    return ''.join(conjunctionize_list(conjunction, vals, oxford_comma))

# ------------------------------------------------------------

# a real example of something that came out of the tailoring engine... used in doctest
_EXAMPLE1 = """
We are here to help. As members of the Project Quit team
                            
    
    
        
            
                
                    at Group Health Cooperative
                
            
            
    
    
        
            , it is our pleasure to provide you with what you need to take control of your health.
"""

# ------------------------------------------------------------

if __name__ == '__main__':
    import doctest, textutil
    doctest.testmod(textutil)  # old-school doctest invocation needed for jython 2.2
    
