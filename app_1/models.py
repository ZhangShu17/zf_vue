# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# 区
class District(models.Model):
    code = models.CharField(max_length=4, verbose_name=unicode('区代码'))
    name = models.CharField(max_length=10, verbose_name=unicode('区名称'))

    class Meta:
        unique_together = (('code', 'name'),)


# 系统用户名及密码表
class Account(models.Model):
    name = models.CharField(max_length=100, verbose_name=unicode('用户名'))
    password = models.CharField(max_length=100, verbose_name=unicode('密码'))
    district_id = models.IntegerField(default=0)

    class Meta:
        unique_together = (('name', 'password'),)


# 人员表
class Faculty(models.Model):
    district = models.ForeignKey(to=District, related_name='district_faculty', null=True)
    name = models.CharField(max_length=255, verbose_name=unicode('姓名'))
    mobile = models.CharField(max_length=11, verbose_name=unicode('电话'), null=True)
    duty = models.CharField(max_length=30, verbose_name=unicode('职务'), null=True)
    channel = models.CharField(max_length=10, verbose_name=unicode('电台信道'), null=True)
    call_sign = models.CharField(max_length=10, verbose_name=unicode('电台呼号'), null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (('name', 'mobile', 'duty'),)


# 勤务路线
class ServiceLine(models.Model):
    name = models.CharField(max_length=100)
    startPlace = models.CharField(max_length=100)
    endPlace = models.CharField(max_length=100)
    time = models.DateField(max_length=100)
    district = models.ManyToManyField(to=District, related_name='District_Service')
    road = models.ManyToManyField(to='Road', related_name='Road_Service')
    remark1 = models.CharField(max_length=100, default='')
    remark2 = models.CharField(max_length=100, default='')
    remark3 = models.CharField(max_length=100, default='')
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (('name', 'startPlace', 'endPlace'),)


# 路线表
class Road(models.Model):
    name = models.CharField(max_length=100, verbose_name=unicode('路线名称'), null=True)
    start_place = models.CharField(max_length=50, verbose_name=unicode('起点地名'), null=True)
    end_place =  models.CharField(max_length=50, verbose_name=unicode('终点地名'), null=True)
    start_point = models.CharField(max_length=50, verbose_name=unicode('起点经纬度'), null=True)
    end_point = models.CharField(max_length=50, verbose_name=unicode('终点经纬度'), null=True)
    length = models.CharField(max_length=10, verbose_name=unicode('路线长度'), default='')
    district = models.ForeignKey(to=District, related_name='Districr_Road', null=True, on_delete=models.SET_NULL)
    # 路长
    chief = models.ManyToManyField(to=Faculty, related_name='Faculty_Road_Chief')
    # 执行路长-分局
    exec_chief_sub_bureau =  models.ManyToManyField(to=Faculty,
                                               related_name='Faculty_Road_Exec_Chief_Sub_Bureau')
    # 执行路长-交通
    exec_chief_trans =  models.ManyToManyField(to=Faculty,
                                          related_name='Faculty_Road_Exec_Chief_Trans')
    # 执行路长-武警
    exec_chief_armed_poli = models.ManyToManyField(to=Faculty,
                                              related_name='Faculty_Road_Exec_Chief_Armed_Poli')
    # 备注1
    remark1 = models.CharField(max_length=100, default='', null=True)
    # 备注2
    remark2 = models.CharField(max_length=100, default='', null=True)
    # 备注3
    remark3 = models.CharField(max_length=100, default='', null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (('name', 'start_point', 'end_point'),)


# 路段表
class Section(models.Model):
    district = models.ForeignKey(to=District, related_name='district_section', null=True)
    name = models.CharField(max_length=100, verbose_name=unicode('路段名称'), null=True)
    start_place = models.CharField(max_length=50, verbose_name=unicode('起点地名'), null=True)
    end_place = models.CharField(max_length=50, verbose_name=unicode('终点地名'), null=True)
    start_point = models.CharField(max_length=50, verbose_name=unicode('起点经纬度'), null=True)
    end_point = models.CharField(max_length=50, verbose_name=unicode('终点经纬度'), null=True)
    road = models.ForeignKey(to=Road, related_name='Road_Section', null=True, on_delete=models.SET_NULL)
    # 段长
    chief = models.ManyToManyField(to=Faculty, related_name='Faculty_Section_Chief')
    # 执行段长-分局
    exec_chief_sub_bureau = models.ManyToManyField(to=Faculty,
                                              related_name='Faculty_Section_Exec_Chief_Sub_Bureau')
    # 执行段长-交通
    exec_chief_trans = models.ManyToManyField(to=Faculty,
                                         related_name='Faculty_Section_Exec_Chief_Trans')
    # 执行段长-武警
    exec_chief_armed_poli = models.ManyToManyField(to=Faculty,
                                              related_name='Faculty_Section_Exec_Chief_Armed_Poli')
    # 备注1
    remark1 = models.CharField(max_length=100, default='', null=True)
    # 备注2
    remark2 = models.CharField(max_length=100, default='', null=True)
    # 备注3
    remark3 = models.CharField(max_length=100, default='', null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (('name', 'start_point', 'end_point'),)


# 岗哨表
class Station(models.Model):
    district = models.ForeignKey(to=District, related_name='district_station', null=True)
    name = models.CharField(max_length=100, verbose_name=unicode('岗哨名称'))
    location = models.CharField(max_length=50, verbose_name=unicode('岗哨经纬度'), null=True)
    section = models.ForeignKey(to=Section, related_name='Section_Station', null=True, on_delete=models.SET_NULL)
    # 岗长-分局
    chief = models.ManyToManyField(to=Faculty, related_name='Faculty_Station_Chief')
    # 执行岗长-交通
    exec_chief_trans = models.ManyToManyField(to=Faculty,
                                         related_name='Faculty_Station_Exec_Chief_Trans')
    # 备注1
    remark1 = models.CharField(max_length=100, default='', null=True)
    # 备注2
    remark2 = models.CharField(max_length=100, default='', null=True)
    # 备注3
    remark3 = models.CharField(max_length=100, default='', null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (('name', 'location'),)
