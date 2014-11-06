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

"""Helper functions to make subject output easier (as for tailor.py)
"""


import cStringIO
import operator

from tailoring2.dictionary import CharacteristicDefinition

# ------------------------------------------------------------

class CharacteristicValue(object):

    def __init__(self, chardef, selval, msgval):
        self.chardef = chardef
        self.selval = selval
        self.msgval = msgval


def SubjectReprIntermediate(subject, mtsdict, data_sources=None):
    """before dumping to text or html or whatever, put together
    collect the subject info in a useful intermediate format suitable
    for quick conversion into some tabular form.

    returned data structure is a dict of sources. Each source is a
    dict of characteristic name to a CharacteristicValue instance.

    allchars[source] = {charname: CharacteristicValue()}
    """
    allchars = {}
    data_sources = data_sources or subject.data_sources \
        or mtsdict.sources or ['']
    for source in data_sources:
        allchars[source] = {}
        selchars = subject.selection_chars.get(source, {})
        msgchars = subject.message_chars.get(source, {})
        for key, value in selchars.items():
            try:
                chardef = mtsdict.char_index[key]
            except KeyError:
                chardef = CharacteristicDefinition.synthesize(key, value)
            allchars[source][key] = CharacteristicValue(
                chardef, selchars[key], msgchars[key])
    return allchars


def deunicode(s):
    """s is a unicode string but doesn't necessarily contain any unicode
    characters -- try to convert it to a plain string. Return the plain
    string version if conversion was possible, the original unicode if
    not.
    """
    if isinstance(s, unicode):
        try:
            s = str(s)
        except UnicodeDecodeError:
            pass
    return s


class SubjectRepr(object):
    """helper class for a subject that provides useful debugging output
    """
    
    def __init__(self, subject, mtsdict, maxcolwidth=30):
        self.subject = subject
        self.mtsdict = mtsdict
        self.maxcolwidth = maxcolwidth
        
    def dump(self, data_sources=None):
        """return a string, a table showing all the subject's
        selection_chars, one per row alphabetically.
        
        Derived characteristics are denoted by a D. Multiple-response
        characteristics are denoted by a +. Values that are different in
        message_chars are shown in the rightmost column. For visual
        clarity, characteristic values are converted from unicode to
        plain strings where possible.
        """
        # lines accumulator -- first row is header
        lines = [['Source', 'Name', 'Selection', 'Message']]
        data_sources = data_sources or self.mtsdict.sources or ['']
        subjectinfo = SubjectReprIntermediate(self.subject,
            self.mtsdict, data_sources)
        for source in data_sources:
            lines.append([repr(source), '', '', ''])
            key_order = self.subject.selection_chars[source].keys()
            key_order.sort()
            for key in key_order:
                charval = subjectinfo[source][key]
                chardef, selval, msgval = charval.chardef, charval.selval, charval.msgval
                if source not in chardef.sources:
                    # not really in source -- exclude from output
                    continue

                lineitems = ['  ']
                name_col = chardef.name
                if chardef.is_multivalued:
                    name_col += " [+]"
                if chardef.is_derived:
                    name_col += " [D]"
                lineitems.append("%s" % name_col)
                
                selvalrepr = repr(deunicode(selval))
                lineitems.append(selvalrepr)
                
                if msgval == selval:
                    lineitems.append('')
                else:
                    lineitems.append("%s" % (repr(msgval)))

                lines.append(lineitems)
        wrapper = lambda t: wrap_onspace(t, self.maxcolwidth)
        return indent(lines, hasHeader=True, wrapfunc=wrapper)

    def __repr__(self):
        return "<SubjectRepr for %s on %s>" % (self.subject, self.mtsdict)


# ------------------------------------------------------------
# table-presentation function by George Sakkis:
#   http://code.activestate.com/recipes/267662/

def indent(rows, hasHeader=False, headerChar='-', delim=' | ', justify='left',
           separateRows=False, prefix='', postfix='', wrapfunc=lambda x: x):
    """Indents a table by column.
       - rows: A sequence of sequences of items, one sequence per row.
       - hasHeader: True if the first row consists of the columns' names.
       - headerChar: Character to be used for the row separator line
         (if hasHeader==True or separateRows==True).
       - delim: The column delimiter.
       - justify: Determines how are data justified in their column. 
         Valid values are 'left','right' and 'center'.
       - separateRows: True if rows are to be separated by a line
         of 'headerChar's.
       - prefix: A string prepended to each printed row.
       - postfix: A string appended to each printed row.
       - wrapfunc: A function f(text) for wrapping text; each element in
         the table is first wrapped by this function."""
    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row):
        newRows = [wrapfunc(item).split('\n') for item in row]
        return [[substr or '' for substr in item] for item in map(None, *newRows)]
    # break each logical row into one or more physical ones
    logicalRows = [rowWrapper(row) for row in rows]
    # columns of physical rows
    columns = map(None, *reduce(operator.add, logicalRows))
    # get the maximum of each column by the string length of its items
    maxWidths = [max([len(str(item)) for item in column]) for column in columns]
    rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths) + \
                                 len(delim)*(len(maxWidths)-1))
    # select the appropriate justify method
    justify = {'center': str.center, 'right': str.rjust, 'left': str.ljust}[justify.lower()]
    output=cStringIO.StringIO()
    if separateRows:
        print >> output, rowSeparator
    for physicalRows in logicalRows:
        for row in physicalRows:
            print >> output, \
                prefix \
                + delim.join([justify(str(item), width) for (item, width) in zip(row, maxWidths)]) \
                + postfix
        if separateRows or hasHeader:
            print >> output, rowSeparator
            hasHeader=False
    return output.getvalue()

# written by Mike Brown
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
def wrap_onspace(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line[line.rfind('\n')+1:])
                         + len(word.split('\n', 1)[0]) >= width)],
                   word),
                  text.split(' '))

import re
def wrap_onspace_strict(text, width):
    """Similar to wrap_onspace, but enforces the width constraint:
       words longer than width are split."""
    wordRegex = re.compile(r'\S{'+str(width)+r',}')
    return wrap_onspace(wordRegex.sub(
        lambda m: wrap_always(m.group(), width), text), width)

import math
def wrap_always(text, width):
    """A simple word-wrap function that wraps text on exactly width characters.
       It doesn't split the text in words."""
    return '\n'.join([text[width*i: width*(i+1)] \
                       for i in xrange(int(math.ceil(1.*len(text)/width)))])
    
if __name__ == '__main__':
    labels = ('First Name', 'Last Name', 'Age', 'Position')
    data = \
    '''John,Smith,24,Software Engineer
       Mary,Brohowski,23,Sales Manager
       Aristidis,Papageorgopoulos,28,Senior Reseacher'''
    rows = [row.strip().split(',')  for row in data.splitlines()]

    print 'Without wrapping function\n'
    print indent([labels]+rows, hasHeader=True)
    # test indent with different wrapping functions
    width = 10
    for wrapper in (wrap_always, wrap_onspace, wrap_onspace_strict):
        print 'Wrapping function: %s(x,width=%d)\n' % (wrapper.__name__, width)
        print indent([labels]+rows, hasHeader=True, separateRows=True,
                     prefix='| ', postfix=' |',
                     wrapfunc=lambda x: wrapper(x, width))
    
    # output:
    #
    #Without wrapping function
    #
    #First Name | Last Name        | Age | Position         
    #-------------------------------------------------------
    #John       | Smith            | 24  | Software Engineer
    #Mary       | Brohowski        | 23  | Sales Manager    
    #Aristidis  | Papageorgopoulos | 28  | Senior Reseacher 
    #
    #Wrapping function: wrap_always(x,width=10)
    #
    #----------------------------------------------
    #| First Name | Last Name  | Age | Position   |
    #----------------------------------------------
    #| John       | Smith      | 24  | Software E |
    #|            |            |     | ngineer    |
    #----------------------------------------------
    #| Mary       | Brohowski  | 23  | Sales Mana |
    #|            |            |     | ger        |
    #----------------------------------------------
    #| Aristidis  | Papageorgo | 28  | Senior Res |
    #|            | poulos     |     | eacher     |
    #----------------------------------------------
    #
    #Wrapping function: wrap_onspace(x,width=10)
    #
    #---------------------------------------------------
    #| First Name | Last Name        | Age | Position  |
    #---------------------------------------------------
    #| John       | Smith            | 24  | Software  |
    #|            |                  |     | Engineer  |
    #---------------------------------------------------
    #| Mary       | Brohowski        | 23  | Sales     |
    #|            |                  |     | Manager   |
    #---------------------------------------------------
    #| Aristidis  | Papageorgopoulos | 28  | Senior    |
    #|            |                  |     | Reseacher |
    #---------------------------------------------------
    #
    #Wrapping function: wrap_onspace_strict(x,width=10)
    #
    #---------------------------------------------
    #| First Name | Last Name  | Age | Position  |
    #---------------------------------------------
    #| John       | Smith      | 24  | Software  |
    #|            |            |     | Engineer  |
    #---------------------------------------------
    #| Mary       | Brohowski  | 23  | Sales     |
    #|            |            |     | Manager   |
    #---------------------------------------------
    #| Aristidis  | Papageorgo | 28  | Senior    |
    #|            | poulos     |     | Reseacher |
    #---------------------------------------------
