# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator

# 这张表切莫在连接oracle时迁移
class guard_admin(models.Model):
    id = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)],primary_key=True)
    dutyname = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20, null=True)
    duties = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    radio_station = models.CharField(max_length=20, null=True)
    call = models.CharField(max_length=20, null=True)
    category = models.CharField(max_length=1, null=True)
    orderlist = models.IntegerField(null=True)
    mainid = models.IntegerField(null=True)
    enabled = models.CharField(max_length=1,null=True)


class guard_station(models.Model):
    id = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], primary_key=True)
    duties = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    radio_station = models.CharField(max_length=20, null=True)
    call = models.CharField(max_length=20, null=True)
    category = models.CharField(max_length=1, null=True)