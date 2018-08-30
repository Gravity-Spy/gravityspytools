# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class NewClass(models.Model):

    collection_owner = models.CharField(max_length=30,)
    collection_name = models.CharField(max_length=100,)
    new_class_name = models.CharField(max_length=30,)

    user = models.ForeignKey(User)
    new_subjects = ArrayField(models.CharField(max_length=10), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
