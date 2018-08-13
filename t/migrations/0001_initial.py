# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-13 06:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='guard_admin',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999L)])),
                ('dutyname', models.CharField(max_length=20, null=True)),
                ('username', models.CharField(max_length=20, null=True)),
                ('duties', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('radio_station', models.CharField(max_length=20, null=True)),
                ('call', models.CharField(max_length=20, null=True)),
                ('category', models.CharField(max_length=1, null=True)),
                ('orderlist', models.IntegerField(null=True)),
                ('mainid', models.IntegerField(null=True)),
                ('enabled', models.CharField(max_length=1, null=True)),
            ],
        ),
    ]
