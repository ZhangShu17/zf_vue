# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-07-31 17:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0011_auto_20180730_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='road',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Road_Section', to='app_1.Road'),
        ),
        migrations.AlterField(
            model_name='station',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Section_Station', to='app_1.Section'),
        ),
    ]