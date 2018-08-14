# -*- coding: utf-8 -*-

from app_1.models import Faculty, ServiceLine, Station, Section
from t.models import guard_admin, guard_line,guard_road, guard_section,guard_station
from django.db.models import signals
from django.dispatch import receiver
from constants.constants import increment
from api_tools.api_tools import is_already_in_use


@receiver(signals.post_save, sender=Faculty)
def create_update_faculty(sender, instance, created, **kwargs):
    if created:
        print('handlers1_created')
        id = instance.id
        name = instance.name
        mobile = instance.mobile
        duty = instance.duty
        channel = instance.channel
        call_sign = instance.call_sign
        cur_guard_admin = guard_admin.objects.create(uid=id+increment, duties=duty,
                                                     phone=mobile, radio_station=channel,
                                                     call=call_sign, username=name)
        cur_guard_admin.save()
    else:
        print('handlers1_update')
        id = instance.id
        name = instance.name
        mobile = instance.mobile
        duty = instance.duty
        channel = instance.channel
        call_sign = instance.call_sign
        enabled = str(int(instance.enabled))
        guard_admin.objects.filter(uid=id+increment).update(duties=duty, phone=mobile,
                                                             radio_station=channel, call=call_sign,
                                                             username=name, enabled=enabled)


@receiver(signals.post_save, sender=Station)
def create_update_station(sender, instance, created, **kwargs):
    if created:
        print('station_created')
        id = instance.id
        name = instance.name
        location = instance.location
        remark1 = instance.remark1
        remark2 = instance.remark2
        remark3 = instance.remark3
        section_id = instance.section_id
        if section_id:
            section_id = section_id + increment
        cur_guard_station = guard_station.objects.create(uid=id+increment, station_name=name,
                                                         xycoordinate=location, remark1=remark1,
                                                         remark2=remark2, remark3=remark3,
                                                         sectionid=section_id)
        cur_guard_station.save()
    else:
        print('station_update')
        id = instance.id
        name = instance.name
        location = instance.location
        remark1 = instance.remark1
        remark2 = instance.remark2
        remark3 = instance.remark3
        section_id = instance.section_id
        if section_id:
            section_id = section_id + increment
        enabled = str(int(instance.enabled))
        guard_station.objects.filter(uid=id+increment).update(station_name=name, xycoordinate=location,
                                                               remark1=remark1, remark2=remark2,
                                                               remark3=remark3, sectionid=section_id,
                                                               enabled=enabled)


def station_faculty_change(sender, instance, model, action, pk_set, **kwargs):
    faculty_type = str(sender).split('\'')[1].split('.')[-1].split('_')[-1]
    if action == 'post_add':
        print('post_add')
        for item in pk_set:
            if faculty_type == 'chief':
                print('chief')
                duty_name = u'岗长(分局)'
                order_list = 1
            else:
                print('execu_chief')
                duty_name = u'执行岗长(交管)'
                order_list = 2
            print('打印dutyname orderlist')
            print(duty_name, order_list)
            count = is_already_in_use(item)
            # 无其他职位
            if count < 2:
                print('no other')
                guard_admin.objects.filter(uid=item+increment).update(dutyname=duty_name, orderlist=order_list,
                                                                     category='3', mainid=instance.id+increment)
            # 有其他职位
            else:
                print('exists')
                cur_faculty = Faculty.objects.filter(id=item).first()
                username = cur_faculty.name
                duties = cur_faculty.duty
                phone = cur_faculty.mobile
                radio_station = cur_faculty.channel
                call = cur_faculty.call_sign
                cur_guard_admin = guard_admin.objects.create(uid=item+increment, username=username, duties=duties,
                                                             phone=phone, radio_station=radio_station, call=call,
                                                             dutyname=duty_name, orderlist=order_list,
                                                             category='3', mainid=instance.id + increment)
                cur_guard_admin.save()
    if action == 'post_remove':
        for item in pk_set:
            if faculty_type == 'chief':
                order_list = 1
            else:
                order_list = 2
            count = is_already_in_use(item)
            # 还有其他职位
            if count:
                print('other duty')
                guard_admin.objects.filter(uid=item+increment, orderlist=order_list,
                                           category='3', mainid=instance.id + increment).\
                    delete()
            else:
                print('no other duty')
                guard_admin.objects.filter(uid=item+increment).\
                    update(dutyname=None, orderlist=None, category=None, mainid=None)


signals.m2m_changed.connect(station_faculty_change, sender=Station.chief.through)
signals.m2m_changed.connect(station_faculty_change, sender=Station.exec_chief_trans.through)


@receiver(signals.post_save, sender=Section)
def create_update_section(sender, instance, created, **kwargs):
    if created:
        print('section_created')
        id = instance.id
        name = instance.name
        start_place = instance.start_place
        end_place = instance.end_place
        xy_coordinate = instance.xy_coordinate
        road_id = instance.road_id
        remark1 = instance.remark1
        remark2 = instance.remark2
        remark3 = instance.remark3
        if road_id:
            road_id = road_id + increment
        cur_guard_section = guard_section.objects.create(uid=id+increment, section_name=name,
                                                         section_begin=start_place, section_end=end_place,
                                                         xycoordinate=xy_coordinate,roadid=road_id, remark1=remark1,
                                                         remark2=remark2, remark3=remark3)
        cur_guard_section.save()
    else:
        print('section_update')
        id = instance.id
        name = instance.name
        start_place = instance.start_place
        end_place = instance.end_place
        xy_coordinate = instance.xy_coordinate
        road_id = instance.road_id
        remark1 = instance.remark1
        remark2 = instance.remark2
        remark3 = instance.remark3
        enabled = str(int(instance.enabled))
        if road_id:
            road_id = road_id + increment
        guard_section.objects.filter(uid=id + increment).update(section_name=name, section_begin=start_place,
                                                                section_end=end_place, xycoordinate=xy_coordinate,
                                                                roadid=road_id, remark1=remark1, remark2=remark2,
                                                                remark3=remark3, enabled=enabled)
