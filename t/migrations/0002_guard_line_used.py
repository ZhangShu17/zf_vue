# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-16 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guard_line',
            name='used',
            field=models.CharField(default='1', max_length=1),
        ),
    ]
