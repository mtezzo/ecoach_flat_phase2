# -*- encodeing: utf-8 -*-
import os
import tempfile
from shutil import copy2, copystat, Error, rmtree
from itertools import chain

from django.core.management.commands.makemessages import Command as MMCommand
from tailoring2.translations import GetTextContexts

from djangotailoring.project import getproject

def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src) 
    if ignore is not None: 
        ignored_names = ignore(src, names) 
    else: 
        ignored_names = set() 
    try: 
        os.makedirs(dst) 
    except OSError, exc: 
        # XXX - this is pretty ugly 
        if "file already exists" in exc[1]:  # Windows 
            pass 
        elif "File exists" in exc[1]:        # Linux 
            pass 
        else: 
            raise 
    errors = [] 
    for name in names: 
        if name in ignored_names: 
            continue 
        srcname = os.path.join(src, name) 
        dstname = os.path.join(dst, name) 
        try: 
            if symlinks and os.path.islink(srcname): 
                linkto = os.readlink(srcname) 
                os.symlink(linkto, dstname) 
            elif os.path.isdir(srcname): 
                copytree(srcname, dstname, symlinks, ignore) 
            else: 
                copy2(srcname, dstname) 
            # XXX What about devices, sockets etc.? 
        except (IOError, os.error), why: 
            errors.append((srcname, dstname, str(why))) 
        # catch the Error from the recursive copytree so that we can 
        # continue with other files 
        except Error, err: 
            errors.extend(err.args[0]) 
    try: 
        copystat(src, dst) 
    except WindowsError: 
        # can't copy file access times on Windows 
        pass 
    except OSError, why: 
        errors.extend((src, dst, str(why))) 
    if errors: 
        raise Error, errors 


class DictionaryGetTextObject(object):
    pgettext_context = ''
    
    def __init__(self, content):
        self.content = content
    
    def get_context_name(self):
        return self.pgettext_context
    
    def __unicode__(self):
        return u'pgettext(%r, %r)' % (self.get_context_name(), self.content)
    

class SurveyQuestion(DictionaryGetTextObject):
    pgettext_context = GetTextContexts.QUESTION

class RestrictionSetValueGetTextObject(DictionaryGetTextObject):
    
    def __init__(self, content, rsetname):
        super(RestrictionSetValueGetTextObject, self).__init__(content)
        self.rsetname = rsetname
    
    def get_context_name(self):
        sup = super(RestrictionSetValueGetTextObject, self).get_context_name()
        return '|'.join([sup, self.rsetname])
    

class SurveyText(RestrictionSetValueGetTextObject):
    pgettext_context = GetTextContexts.SURVEY_OPTION
    
class SubstitutionText(RestrictionSetValueGetTextObject):
    pgettext_context = GetTextContexts.SUBSTITUTION_TEXT

def get_survey_questions(mtsdict):
    """Walk through an MTS Dictionary and return an iterable of
    SurveyQuestion objects."""
    for char in mtsdict.characteristics:
        if char.question:
            yield SurveyQuestion(char.question)

def get_survey_text(mtsdict):
    """Walk through an MTS Dictionary and return an iterable of
    SurveyText objects."""
    for restrictionset in mtsdict.restrictions:
        for value in restrictionset.values:
            if value.text:
                yield SurveyText(value.text, restrictionset.name)

def get_substitution_text(mtsdict):
    """Walk through an MTS Dictionary and return an iterable of
    SubstitutionText objects."""
    for restrictionset in mtsdict.restrictions:
        for value in restrictionset.values:
            if value.textsub:
                yield SubstitutionText(value.textsub, restrictionset.name)

class Command(MMCommand):
    help = ("Plows through an MTS Dictionary scraping out all text that "
            "should be localized (survey question text and survey value "
            "text) and runs them through django's built-in makemessages "
            "command. ")

    def handle_noargs(self, *args, **options):
        mtsdict = getproject().mtsdict
        tmpdir = tempfile.mkdtemp()
        curdir = os.getcwd()
        new_locale = os.path.join(tmpdir, 'locale')
        os.mkdir(new_locale)
        fn = os.path.join(tmpdir, 'mydictionary.py')
        
        with open(fn, 'w') as f:
            gsq = get_survey_questions(mtsdict)
            gst = get_survey_text(mtsdict)
            gst2 = get_substitution_text(mtsdict)
            for gen in chain([gsq, gst, gst2]):
                for o in gen:
                    f.write(unicode(o).encode('utf-8'))
                    f.write('\n')
                f.write('\n')
        
        os.chdir(tmpdir)
        super(Command, self).handle_noargs(*args, **options)
        os.chdir(curdir)
        
        copytree(new_locale, 'locale')
        
        # delete the temp dir
        rmtree(tmpdir)
    
