import os
import re
import operator

from django.utils.functional import lazy

def _format(s, f):
    return operator.mod(s, f)

lazyformat = lazy(_format, unicode)

def nowrapper(value, tagnames=None):
    """
    Given a Unicode or String object `value`, locate a surrounding
    html/xml-style tag surrounding `value`, and remove it.
    tagnames: a list of tag names that are qualified for removal. Tags found
        with names not in the list are left intact. If the list is empty, or
        not provided, tags with any name are removed.
    """
    if tagnames is not None:
        if isinstance(tagnames, (str, unicode)):
            tagnames = [name.strip() for name in tagnames.split(',')]
        tagnames = '|'.join(tagnames)
    else:
        tagnames = r'\w+'
    m = re.match(r'<(%s)[^>]*?>(.*)</\1>$' % tagnames, value)
    if m:
        return m.group(2)
    return value


def namebase(pth):
    """return pth without its extension and without its enclosing path:
    
    >>> namebase('/Users/waldo/mysecret.txt')
    'mysecret'    
    """
    return os.path.splitext(os.path.basename(pth))[0]

