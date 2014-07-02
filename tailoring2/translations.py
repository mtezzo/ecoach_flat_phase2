# -*- encoding: utf-8 -*-
import operator

from tailoring2.common import ClassValues

# constants

class GetTextContexts(object):
    QUESTION = 'mts|question'
    SURVEY_OPTION = 'mts|option'
    SUBSTITUTION_TEXT = 'mts|substitution'

try:
    # attempt to bring in the django translation subsystem, if it's available. 
    from django.utils.translation import *
    from django.utils.functional import lazy
    try:
        pgettext
    except NameError:
        pgettext = lambda _, s: ugettext(s)
        npgettext = lambda _, s: ungettext(s)
        pgettext_lazy = lambda _, s: ugettext_lazy(s)
        npgettext_lazy = lambda _, s: ungettext_lazy(s)
except ImportError:
    # it appears that it isn't, so let's stub it out for now
    noop = lambda s: unicode(s)
    pnoop = lambda _, s: unicode(s)
    
    string_concat = lambda * strings: u''.join(unicode(s) for s in strings)
    lazy = lambda func, *resultclasses: func
    
    gettext_noop = noop
    ugettext_noop = noop
    gettext = noop
    ngettext = noop
    ugettext = noop
    ungettext = noop
    pgettext = pnoop
    npgettext = pnoop
    ngettext_lazy = noop
    gettext_lazy = noop
    ungettext_lazy = noop
    ugettext_lazy = noop
    pgettext_lazy = pnoop
    npgettext_lazy = pnoop
    
def _is_string(s):
    return isinstance(s, basestring)

def _format(a, b):
    return operator.mod(a, b)

lazy_format = lazy(_format, unicode)

def _join(pivot, strings):
    return pivot.join(unicode(s) for s in strings)

lazy_join = lazy(_join, unicode)

def maybe_lazy_join(pivot, strings):
    if all(_is_string(s) for s in strings):
        return _join(pivot, strings)
    return lazy_join(pivot, strings)

def i18n_survey_tree(tree, mtsdict):
    for question in tree.findall("//question"):
        char = mtsdict.char_index.get(question.get('characteristic'))
        if char is None:
            continue
        restrictionset_name = char.restrictionset.name
        survey_option_context = '|'.join(
            [GetTextContexts.SURVEY_OPTION, restrictionset_name])
        for text in question.findall('.//text'):
            if text.get('class') == ClassValues.PROMPT:
                for content in text.findall('.//content'):
                    if content.text is not None:
                        content.text = pgettext_lazy(
                            GetTextContexts.QUESTION, content.text)
        for response in question.findall('.//response'):
            for content in response.findall('.//content'):
                if content.text is not None:
                    content.text = pgettext_lazy(survey_option_context,
                        content.text)

    for matrix in tree.findall('//matrix'):
        restrictionset_name = matrix.get('valueset')
        if restrictionset_name is None:
            continue
        survey_option_context = '|'.join([GetTextContexts.SURVEY_OPTION, restrictionset_name])
        for response in matrix.findall('.//response'):
            for content in response.findall('.//content'):
                if content.text is not None:
                    content.text = pgettext_lazy(survey_option_context,
                                                 content.text)
