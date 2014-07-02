# Most code in this module comes originally from the Python 2.4 standard
# library and is covered by the Python license:
#     <http://www.python.org/download/releases/2.4.5/license/>
# 
# The local modification is the addition of the TailoringTemplate class.

"""String templating and token substitution using shell-style $token
syntax instead of python-style %s or %(token)s. Except for
TailoringTemplate, this code was ripped intact out of the Python 2.4
library. It works fine in Python 2.3 and Jython 2.2.
"""

import unittest, logging
import re as _re
log = logging.getLogger(__name__)

# --------------------------------------------------------------------
# string Template code ripped out of Python 2.4's 'string' module

class _multimap:
    """Helper class for combining multiple mappings.

    Used by .{safe_,}substitute() to combine the mapping and keyword
    arguments.
    """
    def __init__(self, primary, secondary):
        self._primary = primary
        self._secondary = secondary

    def __getitem__(self, key):
        try:
            return self._primary[key]
        except KeyError:
            return self._secondary[key]


class _TemplateMetaclass(type):
    pattern = r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
      (?P<named>%(id)s)      |   # delimiter and a Python identifier
      {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    """

    def __init__(cls, name, bases, dct):
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = _TemplateMetaclass.pattern % {
                'delim' : _re.escape(cls.delimiter),
                'id'    : cls.idpattern,
                }
        cls.pattern = _re.compile(pattern, _re.IGNORECASE | _re.VERBOSE)


class Template:
    """A string class for supporting $-substitutions."""
    __metaclass__ = _TemplateMetaclass

    delimiter = '$'
    idpattern = r'[_a-z][_a-z0-9]*'

    def __init__(self, template):
        self.template = template

    # Search for $$, $identifier, ${identifier}, and any bare $'s

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' %
                         (lineno, colno))

    def lookup(self, mapping, key):
        """subclasses must raise KeyError even if their own error is something else"""
        return unicode(mapping[key])
        
    def substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]
        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                val = self.lookup(mapping, named)
                # We use this idiom instead of str() because the latter will
                # fail if val is a Unicode containing non-ASCII characters.
                return '%s' % val
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)

    def safe_substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]
        # Helper function for .sub()
        def convert(mo):
            named = mo.group('named')
            if named is not None:
                try:
                    # We use this idiom instead of str() because the latter
                    # will fail if val is a Unicode containing non-ASCII
                    return '%s' % self.lookup(mapping, named)
                except KeyError:
                    return self.delimiter + named
            braced = mo.group('braced')
            if braced is not None:
                try:
                    return '%s' % self.lookup(mapping, braced)
                except KeyError:
                    return self.delimiter + '{' + braced + '}'
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                return self.delimiter
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)

# --------------------------------------------------------------------
# Py2.4-inspired/-based system for templating and string replacements

class TailoringTemplate(Template):
    """A Template that understands function calls and arguments as well as
    simple key lookups.
    """
    
    # new pattern recognizes function arguments: 'func(arg)'
    # now also recognizes simple.dotted.expressions, though not arbitrary expressions
    idpattern = r'([_a-z][_a-z0-9.]*\b(\(.*?\))?)'
    
    def lookup(self, mapping, key):
        """eval()-based lookup. Any error in the eval will, however, be expressed as
        a KeyError
        """
        try:
            return unicode(eval(key, globals(), mapping))
        except Exception, err:
            # as part of the subclass contract, we have to raise KeyError
            # even if the error is something else. but we can save the 
            # underlying error as _realerror.
            keyerr = KeyError(key)
            keyerr._realerror = err
            raise keyerr

# -------------------------------------------------------------------------
# main

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('').setLevel(logging.WARNING)
    from tailoring.test import test_string_template
    unittest.main(test_string_template)
