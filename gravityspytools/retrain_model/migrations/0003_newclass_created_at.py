# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-28 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('retrain_model', '0002_remove_newclass_thumbnail_subects'),
    ]

    operations = [
        migrations.AddField(
            model_name='newclass',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]