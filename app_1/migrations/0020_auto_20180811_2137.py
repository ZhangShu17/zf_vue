# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-11 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0019_auto_20180807_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='road',
            name='end_place',
            field=models.CharField(max_length=50, null=True, verbose_name='\u7ec8\u70b9\u5730\u540d'),
        ),
        migrations.AlterField(
            model_name='road',
            name='end_point',
            field=models.CharField(max_length=50, null=True, verbose_name='\u7ec8\u70b9\u7ecf\u7eac\u5ea6'),
        ),
        migrations.AlterField(
            model_name='road',
            name='remark1',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='road',
            name='remark2',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='road',
            name='remark3',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='road',
            name='start_place',
            field=models.CharField(max_length=50, null=True, verbose_name='\u8d77\u70b9\u5730\u540d'),
        ),
        migrations.AlterField(
            model_name='road',
            name='start_point',
            field=models.CharField(max_length=50, null=True, verbose_name='\u8d77\u70b9\u7ecf\u7eac\u5ea6'),
        ),
        migrations.AlterField(
            model_name='section',
            name='end_place',
            field=models.CharField(max_length=50, null=True, verbose_name='\u7ec8\u70b9\u5730\u540d'),
        ),
        migrations.AlterField(
            model_name='section',
            name='end_point',
            field=models.CharField(max_length=50, null=True, verbose_name='\u7ec8\u70b9\u7ecf\u7eac\u5ea6'),
        ),
        migrations.AlterField(
            model_name='section',
            name='remark1',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='remark2',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='remark3',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='start_place',
            field=models.CharField(max_length=50, null=True, verbose_name='\u8d77\u70b9\u5730\u540d'),
        ),
        migrations.AlterField(
            model_name='section',
            name='start_point',
            field=models.CharField(max_length=50, null=True, verbose_name='\u8d77\u70b9\u7ecf\u7eac\u5ea6'),
        ),
        migrations.AlterField(
            model_name='station',
            name='location',
            field=models.CharField(max_length=50, null=True, verbose_name='\u5c97\u54e8\u7ecf\u7eac\u5ea6'),
        ),
        migrations.AlterField(
            model_name='station',
            name='remark1',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='remark2',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='remark3',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together=set([('name', 'mobile', 'duty')]),
        ),
        migrations.AlterUniqueTogether(
            name='station',
            unique_together=set([('name', 'location')]),
        ),
    ]
