from tailoring2.common import json
from django.contrib.auth.models import User
from django.db import models

from djangotailoring import getproject

class SubjectData(models.Model):
    #user_id = models.CharField(max_length=40, db_column="user_id", verbose_name="Unique user id")
    user_id = models.ForeignKey(User, db_column="user_id", to_field='username', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Unique user id")  
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        clsname = self.__class__.__name__
        return "%s data for user '%s'" % (clsname, self.user_id) 
    
    def as_json(self):
        return json.dumps(self.as_dict())
    
    def as_dict(self):
        result = {}
        local_field_names = (field.name for field in self._meta.local_fields)
        local_field_names = (name for name in local_field_names
                             if name not in ('id', 'user_id', 'updated'))
        for name in local_field_names:
            val = getattr(self, name)
            if val is not None:
                result[name] = val
        return result
    

class SerializedSubjectData(models.Model):
    user_id = models.CharField(max_length=30, db_column="user_id",
        verbose_name="Unique user id")
    primary_data = models.TextField(db_column="primary_data",
        verbose_name="Serialized primary characteristics")
    updated = models.DateTimeField(auto_now=True)

