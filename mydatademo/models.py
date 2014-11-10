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

YES_NO_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
)


class Source1(SubjectData):
    First_Name = models.CharField(max_length=20, null=True, blank=True)
    Last_Name = models.CharField(max_length=20, null=True, blank=True)
    NetID = models.CharField(max_length=20, null=True, blank=True)
    Gender = models.CharField(max_length=1, choices=_GENDER_CHOICES, null=True, blank=True)
    Cum_GPA = models.FloatField(null=True, blank=True)
    Cum_High_School_GPA = models.FloatField(null=True, blank=True)
    Declared = models.CharField(max_length=1, choices=YES_NO_CHOICES, null=True, blank=True)
    MLC_Enrolled = models.CharField(max_length=1, choices=YES_NO_CHOICES, null=True, blank=True)
    HeightTotal = models.IntegerField(null=True, blank=True)
    Weight = models.IntegerField(null=True, blank=True)

class EmptySource(SubjectData):
    pass

