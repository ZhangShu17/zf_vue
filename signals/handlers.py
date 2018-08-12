# -*- coding: utf-8 -*-

from app_1.models import Faculty, ServiceLine
from django.db.models import signals
from django.dispatch import receiver
import cx_Oracle

cursor = cx_Oracle.connect('icp_zf', 'icp_zf', '192.168.8.111:1521/orcl').cursor()


@receiver(signals.post_save, sender=Faculty)
def create_faculty(sender, instance, created, **kwargs):
    if created:
        param = {
            'ID': instance.id,
            'USERNAME': instance.name,
            'PHONE': instance.mobile,
            'RADIO_STATION ': instance.channel,
            'CALL': instance.call_sign,
            'DUTIES': instance.duty
        }
        cursor.execute('insert into T_GUARD_ADMIN values(:ID, :USERNAME, :PHONE, :RADIO_STATION, :CALL, :DUTIES)', param)
    else:
        print('update')
        print(instance.name)
        print(instance.id)


def road_changed(sender, instance, model, action, pk_set, **kwargs):
    print(instance.name)
    print(action)
    if action == 'pre_add':
        print('yes')
    print(pk_set)
    for item in pk_set:
        print(item)
    print('899e9e')


signals.m2m_changed.connect(road_changed, sender=ServiceLine.road.through)


