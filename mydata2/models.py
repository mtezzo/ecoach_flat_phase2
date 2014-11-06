from django.db import models
from django.contrib.auth.models import User

# table format source data
from djangotailoring.models import SubjectData

# Create your models here.

# python ../manage.py makemtsmodel > MODEL.OUT (results go below here)

_GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

_SLCENROLLED_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)


class Source1(SubjectData):
    # add meta property
    class Meta: 
        db_table = 'mydata_source1'
    SLCENROLLED = models.CharField(max_length=3, choices=_SLCENROLLED_CHOICES, null=True, blank=True)

class EmptySource(SubjectData):
    pass

class Common1(SubjectData):
    # add meta property
    class Meta: 
        db_table = 'mydata_common1'
    First_Name = models.CharField(max_length=20, null=True, blank=True)
    NetID = models.CharField(max_length=20, null=True, blank=True)
    Gender = models.CharField(max_length=1, choices=_GENDER_CHOICES, null=True, blank=True)
    Last_Name = models.CharField(max_length=20, null=True, blank=True)

