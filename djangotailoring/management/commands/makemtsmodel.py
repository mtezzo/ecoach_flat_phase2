import os

import django.conf
from django.template import Context
from django.template.loaders import filesystem
from django.core.management.base import CommandError, NoArgsCommand

from djangotailoring import getproject
from djangotailoring.subjects import db_names_for_chardef

class Command(NoArgsCommand):
    can_import_settings = True
    requires_model_validation = False
    help = "Generates a models.py file for the current project's dictionary"
    
    def handle_noargs(self, **options):
        project = getproject()
        mtsdict = project.mtsdict
        model_dict = model_dict_for_dictionary(mtsdict)
        restrictions_dict = restrictions_dict_for_dictionary(mtsdict)
        
        thisdir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(thisdir, 'makemtsmodel_templates')
        
        template, _ = filesystem.Loader().load_template('models.pyt',
            template_dirs=[templates_dir])
        context = Context(dict(modelclasses=model_dict,
            choices=restrictions_dict))
        print template.render(context)
    

_pytype_to_type = {
    bool: 'bool',
    str: 'str',
    unicode: 'str',
    int: 'int',
    float: 'float'
}

_fieldtypes = {
    'text': 'TextField(null=True, blank=True)',
    'bool': 'NullBooleanField()',
    'str': 'CharField(max_length=%(maxlength)d, null=True, blank=True)',
    'strc': 'CharField(max_length=%(maxlength)d, choices=%(choices)s, null=True, blank=True)',
    'int': 'IntegerField(null=True, blank=True)',
    'float': 'FloatField(null=True, blank=True)'
}
def _definition_for_name(charname, type, args={}):
    return "%s = models.%s" % (charname, _fieldtypes[type] % args)

def _choices_name_for_restrictionset(restrictionset):
    return '%s_CHOICES' % restrictionset.name.upper()

def _choices_str_for_restrictionset(restrictionset, type=str):
    choices = []
    for value in restrictionset.values:
        text = value.text if value.text else value.symbol
        choices.append((type(value.symbol), text))
    return '(\n%s\n)' % '\n'.join(('    %s,' % repr(c)) for c in choices)

def restrictions_dict_for_dictionary(mtsdict):
    restrictions_dict = {}
    for restrictionset in mtsdict.restrictions:
        if restrictionset.values:
            name = _choices_name_for_restrictionset(restrictionset)
            choices = _choices_str_for_restrictionset(restrictionset)
            restrictions_dict[name] = choices
    return restrictions_dict

def model_dict_for_dictionary(mtsdict):
    model_dict = {}
    classnamer = lambda n: '%s' % (n if n != '' else 'EmptySource')
    for source in mtsdict.sources:
        sourcename = source.name
        fields = []
        for characteristic in mtsdict.characteristics:
            if sourcename in characteristic.sources:
                if characteristic.is_derived:
                    pass
                elif characteristic.is_multivalued:
                    fieldnames = db_names_for_chardef(characteristic)
                    fields.extend([_definition_for_name(fieldname, 'bool')
                                   for fieldname in fieldnames])
                else:
                    restrictionset = characteristic.restrictionset
                    type = _pytype_to_type[characteristic.basetype.pytype]
                    maxlength = 0
                    minlength = 20
                    choicesname = ''
                    if restrictionset:
                        choicesname = _choices_name_for_restrictionset(
                            restrictionset)
                        if restrictionset.lengths:
                            for length in restrictionset.lengths:
                                maxlength = max(maxlength, length.max)
                        if restrictionset.values:
                            if type == 'str':
                                type = 'strc'
                            for value in restrictionset.values:
                                maxlength = max(maxlength, len(value.symbol))
                    if maxlength == 0:
                        maxlength = minlength
                    if maxlength > 100 and type == 'str':
                        type = 'text'
                    args = dict(maxlength=maxlength,
                        choices=choicesname)
                    fields.append(_definition_for_name(characteristic.name,
                        type, args))
        model_dict[classnamer(sourcename)] = fields
    return model_dict

