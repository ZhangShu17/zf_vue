# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator


# 这张表切莫在连接oracle时迁移
class guard_admin(models.Model):
    uid = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
    dutyname = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20, null=True)
    duties = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    radio_station = models.CharField(max_length=20, null=True)
    call = models.CharField(max_length=20, null=True)
    category = models.CharField(max_length=1, null=True)
    orderlist = models.IntegerField(null=True)
    mainid = models.IntegerField(null=True)
    enabled = models.CharField(max_length=1, default='1')


class guard_station(models.Model):
    uid = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
    station_name = models.CharField(max_length=100, null=True)
    xycoordinate = models.CharField(max_length=4000, null=True)
    remark1 = models.CharField(max_length=100, null=True)
    remark2 = models.CharField(max_length=100, null=True)
    remark3 = models.CharField(max_length=100, null=True)
    sectionid = models.IntegerField(null=True)
    enabled = models.CharField(max_length=1, default='1')


class guard_section(models.Model):
    uid = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
    section_name = models.CharField(max_length=100, null=True)
    section_begin = models.CharField(max_length=100, null=True)
    section_end = models.CharField(max_length=100, null=True)
    xycoordinate = models.CharField(max_length=4000, null=True)
    station_ids = models.CharField(max_length=4000, null=True)
    remark1 = models.CharField(max_length=100, null=True)
    remark2 = models.CharField(max_length=100, null=True)
    remark3 = models.CharField(max_length=100, null=True)
    roadid = models.IntegerField(null=True)
    color = models.CharField(max_length=100, null=True)
    enabled = models.CharField(max_length=1, default='1')


class guard_road(models.Model):
    uid = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
    road_name = models.CharField(max_length=100, null=True)
    road_begin = models.CharField(max_length=100, null=True)
    road_end = models.CharField(max_length=100, null=True)
    section_ids = models.CharField(max_length=4000, null=True)
    remark1 = models.CharField(max_length=100, null=True)
    remark2 = models.CharField(max_length=100, null=True)
    remark3 = models.CharField(max_length=100, null=True)
    lineid = models.IntegerField(null=True)
    roadlength = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sectionnum = models.PositiveIntegerField(default=0)
    stationnum = models.PositiveIntegerField(default=0)
    areaid = models.IntegerField(null=True)
    enabled = models.CharField(max_length=1, default='1')


class guard_line(models.Model):
    uid = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], null=True)
    type = models.CharField(max_length=1, null=True)
    name = models.CharField(max_length=20, null=True)
    code = models.CharField(max_length=20, null=True)
    team_group = models.CharField(max_length=20, null=True)
    begins = models.CharField(max_length=64, null=True)
    ends = models.CharField(max_length=64, null=True)
    qwid = models.CharField(max_length=30, null=True)
    begin_point = models.CharField(max_length=100, null=True)
    end_point = models.CharField(max_length=100, null=True)
    vedio_id = models.CharField(max_length=100, null=True)
    direction = models.CharField(max_length=10, null=True)
    points = models.FileField(null=True)
    tz = models.CharField(max_length=20, null=True)
    line_id = models.CharField(max_length=10, null=True)
    used = models.CharField(max_length=1, default='1')
    enabled = models.CharField(max_length=1, default='1')

