# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-07 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0017_auto_20180805_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='road',
            name='chief',
            field=models.ManyToManyField(related_name='Faculty_Road_Chief', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='road',
            name='exec_chief_armed_poli',
            field=models.ManyToManyField(related_name='Faculty_Road_Exec_Chief_Armed_Poli', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='road',
            name='exec_chief_sub_bureau',
            field=models.ManyToManyField(related_name='Faculty_Road_Exec_Chief_Sub_Bureau', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='road',
            name='exec_chief_trans',
            field=models.ManyToManyField(related_name='Faculty_Road_Exec_Chief_Trans', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='section',
            name='chief',
            field=models.ManyToManyField(related_name='Faculty_Section_Chief', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='section',
            name='exec_chief_armed_poli',
            field=models.ManyToManyField(related_name='Faculty_Section_Exec_Chief_Armed_Poli', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='section',
            name='exec_chief_sub_bureau',
            field=models.ManyToManyField(related_name='Faculty_Section_Exec_Chief_Sub_Bureau', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='section',
            name='exec_chief_trans',
            field=models.ManyToManyField(related_name='Faculty_Section_Exec_Chief_Trans', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='serviceline',
            name='district',
            field=models.ManyToManyField(related_name='District_Service', to='app_1.District'),
        ),
        migrations.AlterField(
            model_name='serviceline',
            name='road',
            field=models.ManyToManyField(related_name='Road_Service', to='app_1.Road'),
        ),
        migrations.AlterField(
            model_name='station',
            name='chief',
            field=models.ManyToManyField(related_name='Faculty_Station_Chief', to='app_1.Faculty'),
        ),
        migrations.AlterField(
            model_name='station',
            name='exec_chief_trans',
            field=models.ManyToManyField(related_name='Faculty_Station_Exec_Chief_Trans', to='app_1.Faculty'),
        ),
    ]
