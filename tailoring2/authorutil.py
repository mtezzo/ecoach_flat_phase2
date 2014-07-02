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

"""Utility functions for message authors -- usable in the 'logic' and
'message' columns of message docs and in the derived characteristics in
the MTS dictionary.
"""

import datetime
import math
import re
import operator

from tailoring2 import util
from tailoring2.common import set
from tailoring2.characteristics import Gender, Noun
from tailoring2.translations import lazy_format, maybe_lazy_join

##
# constants

UNDEFINED = set(['', "Undefined", -1, -99.9, None])

##
# utility functions

def isEmpty(char):
    """try to figure out whether the characteristic is None or empty
    """
    try:
        if char in UNDEFINED:
            return True
    except TypeError:
        pass
    try:
        # catch 0 before it goes to operator.truth(). Also catches boolean False.
        x = int(char)
        return False
    except Exception:
        pass
    return not operator.truth(char)


def intersection(set1, set2):
    """return any items from set1 that are also in set2. (In messages,
    usually used as a boolean -- ie, are there any common elements?
    If the return value is a non-empty set, that's equivalent to boolean True.
    """
    for arg in [set1, set2]:
        if util.isString(arg):
            raise TypeError("cannot test bare strings: %s" % arg)
    return set(set1).intersection(set2)


def subset(userlist, messagelist):
    """subset() restricts the acceptable elements of QuitPositiveCoping
    (if, say, you don't want to include "shoot heroin" in the message)
    -- in the comparison list for subset(), you have to supply the TEXT
    SUBSTITUTED values -- this may change someday)
    
    Typical usage:
    >>> QuitPositiveCoping = ['Stress', 'Smoke']
    >>> subset(QuitPositiveCoping, ['Stress', 'Meal'])
    ['Stress']
    """
    restriction_set = set(userlist)
    return [item for item in messagelist if item in restriction_set]

    
def containsOnly(char, *values):
    """true if char has no items that are not present in arguments in 'values'
    """
    char = set(adaptToList(char))
    values = set(util.flatten(values))
    return char.issubset(values)


def containsAll(char, *values):
    """true if every item in char is present in values, and
    every item in values is present in char
    
    that is, they are equivalent (order and duplicates aside)
    """
    char = set(adaptToList(char))
    values = set(util.flatten(values))
    return char == values


def charAsList(listChar):
    """given a comma-delimited string (ie, a survey list char),
    return a python list
    """
    try:
        if listChar is not None and listChar != '':
            return listChar.split(',')
        else:
            return []
    except AttributeError, err:
        raise TypeError("%s not splittable (ie, a string)" % (listChar))

    
def listAsChar(aList):
    """given a python list, return a comma-delimited string
    (ie, a survey list char)
    """
    if aList is not None:
        return ','.join(aList)
    else:
        return ""


def adaptToList(item):
    """make item into a python list if at all possible
            - if a list or list-like already, return it (a string doesn't pass isList())
            - if it's a string, see if it's a survey list
                - if a survey list, make it a real list
                - if just a string, wrap it in a list
            - otherwise, assume it's a scalar and wrap it in a list
    """
    if util.isList(item):
        return item
    if util.isString(item):
        return charAsList(item)
    return [item]


def count(aListChar):
    """return number of items in the survey list char"""
    if isinstance(aListChar, list):
        return len(aListChar)
    else:
        return len(charAsList(aListChar))
    

def englishList(lst, min, max):
    """given a list characteristic (comma-separated or a python list)
    return an end-user readable list with proper placement of commas and
    the word "and."
    
    For example,
    >>> unicode(englishList("One,Two,Three,Four", 1, 3))
    u'One, Two and Three'

    See test_authorutil.py:test_englishList() for more examples.
    """
    if not util.isList(lst):
        lst = charAsList(lst)
    if not lst: return ""
    if min < 1: return lst[0]
    if len(lst) == 1: return lst[0]
    lst = lst[:max]
    if len(lst) == 1: return lst[0]
    head, tail = [unicode(s) for s in lst[:-1]], unicode(lst[-1])
    headtext = maybe_lazy_join(u", ", head)
    return lazy_format(u"%s and %s", (headtext, tail))

# ------------------------------------------------------------
# ordinal numbers

# index of this list is the suffix to apply
_ordinal_table = 'th st nd rd th th th th th th'.split()


def ordinal_suffix(num):
    """Inspect num and return the appropriate ordinal suffix.
    
    wikipedia has a nice enough writeup:
            http://en.wikipedia.org/wiki/Names_of_numbers_in_English#Ordinal_numbers
    """
    tens = num / 10
    if tens == 1:
        return "th"
    ones = num % 10
    return _ordinal_table[ones]


def ordinal_symbol(num):
    """return a string, the ordinal number symbol of the given integer.
    That is, 'num' with the appropriate ordinal suffix.

    For example:
    >>> ordinal(1)
    '1st'
    >>> ordinal(2)
    '2nd'
    >>> ordinal(7)
    '7th'
    >>> ordinal(12)
    '12th'
    >>> ordinal(23)
    '23rd'
    """
    return "%s%s" % (num, ordinal_suffix(num))

# TODO: might have an ordinal_name() someday (where
# the number is spelled out, like 'first' or 'eighteenth'). Until
# then, 'ordinal' will mean ordinal_symbol()
ordinal = ordinal_symbol
# ------------------------------------------------------------

def charsMatchingName(allchars, namePattern):
    """search allchars dict for keys matching the given pattern (a regexp)
            - return a subdict
    """
    matches = [(key, value) for key, value in allchars.items() if namePattern.search(key)]
    return dict(matches)


def splitCharLines(lines):
    '''return a list from a string with one char name on each line, eg:
        """
            ReasonsEatOwnHealth
            ReasonsEatPhysHealth
            ReasonsEatValue
            ReasonsEatBelieve
            ReasonsEatLifeGoals
            ReasonsEatDecRiskDis
            ReasonsEatWeight
        """
    - whitespace before and after the list, and before and after each item, is stripped
    '''
    return [line.strip() for line in lines.strip().split("\n")]
    
# --------------------------------------------------------------------
# date manipulation functions -- originally from TGA project

def days(numDays=1):
    """returns total seconds in the given number of days
    (ie, days * seconds-in-a-day)
    """
    return numDays * 86400 # 86400 = 60s * 60m * 24h


def dayString(timeInSecs):
    """returns a string formatted with the given time:
    "fullweekdayname, fullmonthname dayofmonth" -- eg, "Wednesday, December 19"

    for format string docs, see
        http://www.python.org/doc/current/lib/module-time.html#l2h-1288
    """
    return time.strftime("%A, %B %d", time.localtime(timeInSecs))
    

def timestampString():
    """returns a bare-bones timestamp string of the current moment:
            '01/09/02 16:47:11'
    """
    return time.strftime("%x %X", time.localtime())
    
# next group of functions (today, yesterday) all return a time (ie, seconds since the epoch)
# to get a useful string, run the result through dayString

def today():
    """returns the time, in seconds since the epoch"""
    # a little sloppy -- should properly use timestamp characteristic
    # (but it's a string right now, not a date, so we'd have to convert
    # back and forth)
    return time.time()


def yesterday():
    """exactly one day earlier than today(), in seconds"""
    return today() - days(1)


ALL_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', \
        'July', 'August', 'September', 'October', 'November', 'December']


def last12MonthsMenuItems(notSelectedText='Choose a month'):
    """Returns a comma-separated string (ie, a list characteristic in
    the survey style). Elements are month-year pairs ('July 2002,August 2002,
    September 2002,...,July 2003').
    
    The notSelectedText arg is inserted as the first item in the list.
    """
    months = ["%s %i" % (ALL_MONTHS[m-1], y) for m, y in last12Months()]
    months.reverse()
    months.insert(0, notSelectedText)
    return listAsChar(months)


def last12Months(now=None):
    """Returns characteristic-style list of the 12 months previous to this one
    and this one. (For example, this is written in July 2003, so this function's
    return value would start with July 2002 and end with July 2003.)
    
    Return value is a list of tuples. The tuples are (month, year) where both
    are integers. Month is a 1-index integer (where 1=Jan)
    
    Optional 'now' argument is a time tuple for when to start calculating from.
    Default is the current time as returned by time.localtime().
    """
    if now is None:
        now = time.localtime()
    thisYear = now[0]
    thisMonthZeroIndex = now[1] - 1 # zero-index, where 0=Jan
    
    months = [] # month/year tuples
    for aMonth in range(thisMonthZeroIndex - 12, thisMonthZeroIndex + 1):
        m = (aMonth % 12) + 1 # back to 1-index
        y = thisYear
        if aMonth < 0:
            y -= 1
        months.append((m, y))
    return months
    

def calcAge(month, day_of_month, year):
    """given a person's birth month, day, and year (all coercable to ints),
    return the age of the person as an integer
    
    - will raise ValueError if the three args can't be coerced to ints
    """
    month, day_of_month, year = int(month), int(day_of_month), int(year)
    birthdate = datetime.date(year, month, day_of_month)
    agedelta = datetime.date.today() - birthdate
    return int(math.floor(agedelta.days / 365.25))

# --------------------------------------------------------------------
# categories

class Category(object):
    """simple container for handling integer ranges"""

    def __init__(self, min, max, name):
        """(min, max, name)
            where min and max are the bounds of the category (inclusive) and
            name is a string that represents the category
            
            min and max must be integers due to an implementation detail (namely,
            that the class uses a range() internally to test inclusion)
        """
        self.min = min
        self.max = max
        self._range = set(range(min, max+1))
        self.name = name

    def __contains__(self, item):
        return item in self._range

    
class CategoryCollection:
    
    def __init__(self, categories):
        """catranges is a list of Category objects"""
        self.categories = categories
        
    def select(self, item, default=None):
        for cat in self.categories:
            if item in cat:
                return cat.name
        if default is None:
            raise ValueError("couldn't find category for %s" % item)
        else:
            return default
            
# --------------------------------------------------------------------
# javascript code generator -- popup window

class JSModalWindow:
    """code generator for a link (<a> tag) that triggers a popup window"""
    
    defaults = dict(
        toolbar='no',
        location='no',
        status='no',
        menubar='no',
        resizable='yes',
        scrollbars='no',
        width='550',
        height='600',
    )
    
    def __init__(self, url, name, **features):
        """parameters mirror the standard javascript window.open() method
                - url is the url of the new window's content
                - name is the title of the new window (and, in this implementation,
                    the name of the link)
                - features is a dict of other browser window features. reasonable
                    defaults are supplied.
        """
        self.url = url
        self.name = name
        # if name isn't a valid js identifier(?), IE6 doesn't set window size correctly
        self.target_name = util.noSpacePunc(name)
        self.features = self.defaults.copy()
        self.features.update(features)

    def features_as_string(self):
        # only trick is not to quote values (ie, don't use repr())
        return ",".join(['%s=%s' % (key, val) for key, val in self.features.items()])
        
    def as_javascript(self):
        url, name, target_name = self.url, self.name, self.target_name
        features_str = self.features_as_string()
        return """<a target="%(target_name)s" onclick="window.open('%(url)s', '%(target_name)s', '%(features_str)s'); return false" href="%(url)s">%(name)s</a>""" % locals()

# ------------------------------------------------------------
# pronoun substitution and possessives

# TODO: document

def _cap(stringfunc):
    """wrap a function that returns a string in order to capitalize the result"""
    def _cap(*args, **kwargs):
        return stringfunc(*args, **kwargs).capitalize()
    return _cap

def _with_cap(stringfunc):
    """given a string-returning function, return a 2-tuple of the
    original function and a wrapped version that returns its result
    capitalized
    """
    return (stringfunc, _cap(stringfunc))
    
    
##
# all of the gender-dependent pronoun pickers take one argument, a gender
# string. 'm'/'f' and 'male'/'female' are accepted case-insensitively.
# (Other values might be added someday.) Unrecognized values raise
# ValueError.

heshe, HeShe = _with_cap(Gender.picker_for('heshe'))
hisher, HisHer = _with_cap(Gender.picker_for('hisher'))
himher, HimHer = _with_cap(Gender.picker_for('himher'))
himselfherself, HimselfHerself = _with_cap(Gender.picker_for('himselfherself'))
manwoman, ManWoman = _with_cap(Gender.picker_for('manwoman'))
menwomen, MenWomen = _with_cap(Gender.picker_for('menwomen'))

# ------------------------------------------------------------


def possessive(name, apos_char="'", nountype="singular"):
    """Return the noun given in 'name' along with its possessive
    apostrophe. For the common case of a character's name, the rule is
    to append 's (apostrophe+s) unless the name ends with -s, in which
    case only an apostrophe is appended.
        
    The 'apos_char' parameter is for using a character other than a
    plain tick mark (for instance, a curly single quote).    
    
    For nountypes other than "singular", there are different
    apostrophization rules. Right now only singular is implemented;
    other values of 'nountype' raise ValueError.
    For much more, see wikipedia:
        http://en.wikipedia.org/wiki/Apostrophe#General_principles_for_the_possessive_apostrophe
    """
    try:
        noun = Noun.forstring(nountype)(name)
        return noun.possessive(apos_char)
    except AttributeError:
        raise ValueError(name)


