# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
"""
class NewSearch(models.Model):

    SINGLEVIEW = 'similarityindex'
    MULTIVIEW = 'updated_similarity_index'

    DATABASE_CHOICES = (
        (MULTIVIEW, 'Multiview Model'),
        (SINGLEVIEW, 'Single View Model'),
    )

    H1 = "\'H1\'"
    H1L1 = "\'H1\', \'L1\'"
    H1L1V1 = "\'H1\', \'L1\', \'V1\'"
    L1 = "\'L1\'"
    L1V1 = "\'L1\', \'V1\'"
    V1 = "\'V1\'"

    IFO_CHOICES = (
        (H1L1, 'H1 L1'),
        (H1, 'H1'),
        (H1L1V1, 'H1 L1 V1'),
        (L1, 'L1'),
        (L1V1, 'L1 V1'),
        (V1, 'V1'),
    )

    database = models.ChoiceField(choices=DATABASE_CHOICES,)
    howmany = models.IntegerField(label='How many similar images would you like to return', max_value=500, min_value=1)
    zooid = models.CharField(label = 'This is the Zooniverse assigned random ID of the image (an integer value)', max_length=10, required=False)
    imageid = models.CharField(label='The GravitySpy uniqueid (this is the 10 character hash that uniquely identifies all gravity spy images)', max_length=10, required=False)
    ifo = models.ChoiceField(choices=IFO_CHOICES,)

    user = models.ForeignKey(User)
    new_subjects = ArrayField(models.CharField(max_length=10), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
"""
