import logging

from django.utils import simplejson as json
from django.core.exceptions import ObjectDoesNotExist

from djangotailoring.project import getproject
from djangotailoring.models import SerializedSubjectData

logger = logging.getLogger(__name__)

MULTIVAL_SEPARATOR = '__'

def values_for_chardef(cdef):
    return [valuerestriction.symbol
            for valuerestriction in cdef.restrictionset.values]

_db_name_template = "%%s%s%%s" % MULTIVAL_SEPARATOR
def db_names_for_chardef(cdef):
    charname = cdef.name
    return [_db_name_template % (charname, valname)
            for valname in values_for_chardef(cdef)]

def multi_val_characteristics(project=None):
    if project is None:
        project = getproject()
    return [cdef for cdef in project.mtsdict.characteristics
            if cdef.is_multivalued]

def _filter_multi_val_characteristics(source_data, multivalnames):
    newvaltable = {}
    namestoremove = set()
    for characteristicname in multivalnames:
        if characteristicname in source_data:
            logger.debug('Generating "%s".', characteristicname)
            basename, valname = characteristicname.split(MULTIVAL_SEPARATOR)
            lst = newvaltable.setdefault(basename, [])
            if source_data[characteristicname]:
                lst.append(valname)
            namestoremove.add(characteristicname)
    for name in namestoremove:
        del source_data[name]
    source_data.update(newvaltable)

def filter_multi_val_characteristics(subject_data):
    logger.info('Filtering data.')
    logger.debug('Flat subject data: %s', subject_data)
    multivalcdefs = multi_val_characteristics()
    multivalnames = []
    for cdef in multivalcdefs:
        multivalnames.extend(db_names_for_chardef(cdef))
    for source, data in subject_data.items():
        logger.info('Filtering data for "%s".', source)
        _filter_multi_val_characteristics(data, multivalnames)
    logger.info('Finished filtering data.')

def _flatten_list(lst, cdef):
    flatdict = {}
    if lst is not None:
        if not isinstance(lst, (list, tuple, set)):
            lst = list(lst)
        valnames = values_for_chardef(cdef)
        for valname in valnames:
            name = _db_name_template % (cdef.name, valname)
            flatdict[name] = valname in lst
    return flatdict

def _flatten_multi_val_characteristics(source_data, cdefindex):
    newvaltable = {}
    namestoremove = set()
    for characteristicname, value in source_data.items():
        if characteristicname in cdefindex:
            logger.debug('Flattening "%s"', characteristicname)
            newvaltable.update(_flatten_list(value, cdefindex[characteristicname]))
            namestoremove.add(characteristicname)
    for name in namestoremove:
        del source_data[name]
    source_data.update(newvaltable)

def flatten_multi_val_characteristics(subject_data):
    logger.info('Flattening data.')
    logger.debug('Subject data: %s', subject_data)
    multivalcdefs = multi_val_characteristics()
    cdefindex = dict((cdef.name, cdef) for cdef in multivalcdefs)
    logger.debug('Characteristics to flatten: %s', cdefindex.keys())
    for source, data in subject_data.items():
        logger.info('Flattening data for source "%s".', source)
        _flatten_multi_val_characteristics(data, cdefindex)
    logger.info('Finished flattening data.')

def encode_subject(subject):
    logger.info('encode_subject() called.')
    logger.debug('Subject data: %s', subject.primary_chars)
    es = json.dumps(subject.primary_chars)
    logger.debug('Encoded data: %s', es)
    return es

def decode_subject(subject_data, project):
    logger.info('decode_subject() called.')
    logger.debug('Encoded data: %s', subject_data)
    s, e = project.subject_for_primary_chars(json.loads(subject_data))
    logger.debug('Subject data: %s', s.selection_chars)
    logger.debug('Subject errors: %s', e)
    return s, e

class SubjectDoesNotExist(ObjectDoesNotExist):
    """Raised when a subject loader cannot find a subject with the given ID."""
    pass

class SubjectLoader(object):
    """A simple baseclass that defines the protocol by which subject loaders
    can handle subject loading and saving."""
    
    @classmethod
    def empty_subject(cls):
        raise NotImplementedError, 'empty_subject is not available for this loader'
    
    @classmethod
    def all_subject_ids(cls):
        raise NotImplementedError, 'all_subject_ids is not available for this loader'
    
    @classmethod
    def subject_exists(cls, userid):
        raise NotImplementedError, 'subject_exists is not available for this loader'
    
    @classmethod
    def get_subject(cls, userid):
        raise NotImplementedError, 'get_subject is not available for this loader'
    
    @classmethod
    def store_subject(cls, userid, subject):
        raise NotImplementedError, 'store_subject is not available for this loader'
    
    @classmethod
    def delete_subject(cls, userid):
        raise NotImplementedError, 'delete_subject is not available for this loader'

class SerializedSubjectLoader(SubjectLoader):
    project = getproject()
    
    @classmethod
    def empty_subject(cls):
        return cls.project.subject_for_primary_chars({})
    
    @classmethod
    def all_subject_ids(cls):
        return [subject['user_id'] for subject in
                SerializedSubjectData.objects.values('user_id')]
    
    @classmethod
    def subject_exists(cls, user_id):
        logger.info('Checking for subject existence "%s".', user_id)
        try:
            SerializedSubjectData.objects.get(user_id=user_id)
            logger.info('Subject found.')
            return True
        except SerializedSubjectData.DoesNotExist:
            logger.info('Subject not found.')
            return False
    
    @classmethod
    def get_subject(cls, user_id):
        logger.info('Fetching subject "%s".', user_id)
        try:
            dbobj = SerializedSubjectData.objects.get(user_id=user_id)
            logger.info('Subject "%s" found.', user_id)
            primary_data = dbobj.primary_data
        except SerializedSubjectData.DoesNotExist:
            logger.error('Subject "%s" not found.', user_id)
            raise SubjectDoesNotExist, 'Subject with id "%s" does not exist' % user_id
        return decode_subject(primary_data, cls.project)
    
    @classmethod
    def store_subject(cls, user_id, subject):
        dbobj,_ = SerializedSubjectData.objects.get_or_create(user_id=user_id)
        dbobj.primary_data = encode_subject(subject)
        logger.info('Storing subject "%s".', user_id)
        dbobj.save()
    
    @classmethod
    def delete_subject(cls, user_id):
        logger.info('Deleting subject "%s".', user_id)
        try:
            SerializedSubjectData.objects.get(user_id=user_id).delete()
        except SerializedSubjectData.DoesNotExist:
            logger.warning('Subject "%s" not found.', user_id)
            raise SubjectDoesNotExist, 'Subject with id "%s" does not exist' % user_id
    

class DjangoSubjectLoader(SubjectLoader):
    sources = {}
    project = getproject()
    
    @classmethod
    def empty_subject(cls):
        return cls.project.subject_for_primary_chars({})
    
    @classmethod
    def as_subject(cls, user_id):
        primary_chars = cls.subject_data(user_id)
        return cls.project.subject_for_primary_chars(primary_chars)
    
    @classmethod
    def subject_data(cls, user_id):
        logger.info('Building subject "%s".', user_id)
        if not cls.subject_exists(user_id):
            raise SubjectDoesNotExist, 'Subject with id "%s" does not exist' % user_id
        all_data = {}
        for source, modelcls in cls.sources.iteritems():
            logger.info('Fetching data for source "%s" from table "%s".',
                source, modelcls._meta.db_table)
            try:
                dbobj = modelcls.objects.get(user_id=user_id)
                logger.info('Data found.')
                data = dbobj.as_dict()
                logger.debug('Table data: %s', data)
            except modelcls.DoesNotExist:
                logger.warning('No data found.')
                data = {}
            all_data[source] = data
        logger.debug('Database data: %s', all_data)
        filter_multi_val_characteristics(all_data)
        logger.debug('Final user subject data: %s', all_data)
        # probably overide here to append subject characteristics
        return all_data
    
    @classmethod
    def save_user_data(cls, user_id, data):
        logger.info('Saving subject "%s".', user_id)
        logger.debug('Subject data: %s', data)
        flat_data = {}
        for source, sdata in data.items():
            flat_data[source] = dict(sdata)
        flatten_multi_val_characteristics(flat_data)
        logger.debug('Flattened data: %s', flat_data)
        for source, modelcls in cls.sources.iteritems():
            logger.info('Saving data for source "%s" in table "%s".', source,
                modelcls._meta.db_table)
            try:
                dbobj = modelcls.objects.get(user_id=user_id)
                logger.info('Found existing data row.')
            except modelcls.DoesNotExist:
                dbobj = modelcls(user_id=user_id)
                logger.info('Created new data row.')
            source_data = flat_data.get(source, {})
            logger.debug('Source data: %s', source, source_data)
            for attrname, value in source_data.items():
                setattr(dbobj, attrname, value)
            dbobj.save()
            logger.info('Source data saved.')
        logger.info('Finished saving subject "%s".', user_id)
    
    @classmethod
    def all_subject_ids(cls):
        ids = set()
        for modelcls in cls.sources.itervalues():
            ids.update(o['user_id'] for o in modelcls.objects.values('user_id'))
        return ids
    
    @classmethod
    def subject_exists(cls, user_id):
        logger.info('Checking for subject existence "%s".', user_id)
        for source, modelcls in cls.sources.iteritems():
            try:
                modelcls.objects.get(user_id=user_id)
                logger.info('Subject found.')
                return True
            except modelcls.DoesNotExist:
                pass
        logger.info('Subject not found')
        return False
    
    @classmethod
    def get_subject(cls, user_id):
        return cls.as_subject(user_id)
    
    @classmethod
    def store_subject(cls, user_id, subject):
        data = subject.primary_chars
        cls.save_user_data(user_id, data)
    
    @classmethod
    def delete_subject(cls, user_id):
        logger.info('Deleting subject "%s".', user_id)
        for source, modelcls in cls.sources.iteritems():
            logger.info('Deleting data for source "%s" in table "%s"', source,
                modelcls._meta.db_table)
            try:
                dbobj = modelcls.objects.get(user_id=user_id)
                dbobj.delete()
                logger.info('Source data deleted.')
            except modelcls.DoesNotExist:
                logger.warning('No source data found.')
                pass
    
    @classmethod
    def assert_conforms_to_dictionary(cls):
        dictionary = cls.project.mtsdict
        field_names_for_source = dict(
            (source, set(cls.sources[source]._meta.get_all_field_names()))
            for source in cls.sources)
        for characteristic in dictionary.characteristics:
            for source in characteristic.sources:
                assert source in cls.sources
                dbcls = cls.sources[source]
                if characteristic.is_multivalued:
                    for fieldname in db_names_for_chardef(characteristic):
                        assert fieldname in field_names_for_source[source]
                else:
                    assert characteristic.name in field_names_for_source[source]
    

def build_model_definitions_for_dictionary(mtsdict):
    raise Exception('This functionality has been moved. Run: python manage.py makemtsmodel')
