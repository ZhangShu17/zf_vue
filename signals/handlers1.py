# -*- coding: utf-8 -*-

from app_1.models import Faculty, ServiceLine, Station, Section, Road
from t.models import guard_admin, guard_line,guard_road, guard_section,guard_station
from django.db.models import signals
from django.dispatch import receiver
from constants.constants import increment
from api_tools.api_tools import is_already_in_use
from api_tools.api_tools import generate_service_line_points
from django.db import transaction


@receiver(signals.post_save, sender=Faculty)
def create_update_faculty(sender, instance, created, **kwargs):
    if created:
        id = instance.id
        name = instance.name
        mobile = instance.mobile
        duty = instance.duty
        channel = instance.channel
        call_sign = instance.call_sign
        count = guard_admin.objects.count()
        cur_guard_admin = guard_admin(uid=id+increment, duties=duty,id=count+1,
                                                     phone=mobile, radio_station=channel,
                                                     call=call_sign, username=name)
        with transaction.atomic():
            cur_guard_admin.save()
    else:
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
        id = instance.id
        name = instance.name
        location = instance.location
        remark1 = instance.remark1
        remark2 = instance.remark2
        remark3 = instance.remark3
        section_id = instance.section_id
        if section_id:
            section_id = section_id + increment
        cur_guard_station = guard_station(id=id+increment, uid=id+increment, station_name=name,
                                                         xycoordinate=location, remark1=remark1,
                                                         remark2=remark2, remark3=remark3,
                                                         sectionid=section_id)
        with transaction.atomic():
            cur_guard_station.save()
    else:
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
        for item in pk_set:
            if faculty_type == 'chief':
                duty_name = u'岗长(分局)'
                order_list = 1
            else:
                duty_name = u'执行岗长(交管)'
                order_list = 2
            count = is_already_in_use(item)
            # 无其他职位
            if count < 2:
                guard_admin.objects.filter(uid=item+increment).update(dutyname=duty_name, orderlist=order_list,
                                                                      category='3', mainid=instance.id+increment,
                                                                      radio_station=instance.channel,
                                                                      call=instance.call_sign)
            # 有其他职位
            else:
                cur_faculty = Faculty.objects.filter(id=item).first()
                username = cur_faculty.name
                duties = cur_faculty.duty
                phone = cur_faculty.mobile
                radio_station = instance.channel
                call = instance.call_sign
                count = guard_admin.objects.count()
                cur_guard_admin = guard_admin(uid=item+increment,id=count+1,
                                              username=username, duties=duties, phone=phone, radio_station=radio_station,
                                              call=call, dutyname=duty_name, orderlist=order_list,
                                              category='3', mainid=instance.id + increment)
                with transaction.atomic():
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
                guard_admin.objects.filter(uid=item+increment, orderlist=order_list,
                                           category='3', mainid=instance.id + increment).\
                    delete()
            else:
                guard_admin.objects.filter(uid=item+increment).\
                    update(dutyname=None, orderlist=None, category=None, mainid=None)


signals.m2m_changed.connect(station_faculty_change, sender=Station.chief.through)
signals.m2m_changed.connect(station_faculty_change, sender=Station.exec_chief_trans.through)


@receiver(signals.post_save, sender=Section)
def create_update_section(sender, instance, created, **kwargs):
    if created:
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
            cur_guard_road = guard_road.objects.get(uid=road_id)
            cur_guard_road.sectionnum = cur_guard_road.sectionnum + 1
            with transaction.atomic():
                cur_guard_road.save()
        cur_guard_section = guard_section(id=id+increment, uid=id+increment, section_name=name,
                                                         section_begin=start_place, section_end=end_place,
                                                         xycoordinate=xy_coordinate,roadid=road_id, remark1=remark1,
                                                         remark2=remark2, remark3=remark3)
        with transaction.atomic():
            cur_guard_section.save()
    else:
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

    road_id = instance.road_id
    if road_id:
        cur_road = Road.objects.get(id=road_id)
        related_service_line_list = cur_road.Road_Service.filter(enabled=True).distinct()
        for item in related_service_line_list:
            generate_service_line_points(item.id)


def section_faculty_change(sender, instance, model, action, pk_set, **kwargs):
    faculty_type = str(sender).split('\'')[1].split('.')[-1].split('_')[-1]
    if action == 'post_add':
        for item in pk_set:
            if faculty_type == 'chief':
                duty_name = u'段长'
                order_list = 1
            if faculty_type == 'bureau':
                duty_name = u'执行段长(分局)'
                order_list = 2
            if faculty_type == 'trans':
                duty_name = u'执行段长(交通)'
                order_list = 3
            if faculty_type == 'poli':
                duty_name = u'执行段长(武警)'
                order_list = 4
            count = is_already_in_use(item)
            # 无其他职位
            if count < 2:
                guard_admin.objects.filter(uid=item+increment).update(dutyname=duty_name, orderlist=order_list,
                                                                     category='2', mainid=instance.id+increment,
                                                                      radio_station=instance.channel,
                                                                      call=instance.call_sign)
            # 有其他职位
            else:
                cur_faculty = Faculty.objects.filter(id=item).first()
                username = cur_faculty.name
                duties = cur_faculty.duty
                phone = cur_faculty.mobile
                radio_station = instance.channel
                call = instance.call_sign
                count = guard_admin.objects.count()
                cur_guard_admin = guard_admin(uid=item+increment, username=username, duties=duties,id=count+1,
                                                             phone=phone, radio_station=radio_station, call=call,
                                                             dutyname=duty_name, orderlist=order_list,
                                                             category='2', mainid=instance.id + increment)
                with transaction.atomic():
                    cur_guard_admin.save()

    if action == 'post_remove':
        for item in pk_set:
            if faculty_type == 'chief':
                order_list = 1
            if faculty_type == 'bureau':
                order_list = 2
            if faculty_type == 'trans':
                order_list = 3
            if faculty_type == 'poli':
                order_list = 4
            count = is_already_in_use(item)
            # 还有其他职位
            if count:
                guard_admin.objects.filter(uid=item+increment, orderlist=order_list,
                                           category='2', mainid=instance.id + increment).\
                    delete()
            else:
                guard_admin.objects.filter(uid=item+increment).\
                    update(dutyname=None, orderlist=None, category=None, mainid=None)


signals.m2m_changed.connect(section_faculty_change, sender=Section.chief.through)
signals.m2m_changed.connect(section_faculty_change, sender=Section.exec_chief_sub_bureau.through)
signals.m2m_changed.connect(section_faculty_change, sender=Section.exec_chief_trans.through)
signals.m2m_changed.connect(section_faculty_change, sender=Section.exec_chief_armed_poli.through)


@receiver(signals.post_save, sender=Road)
def create_update_road(sender, instance, created, **kwargs):

    if created:
        id = instance.id
        name = instance.name
        start_place = instance.start_place
        end_place = instance.end_place
        length = instance.length
        district_id = instance.district_id
        remark1 = instance.remark1
        remark2 = instance.remark2
        remark3 = instance.remark3
        cur_guard_road = guard_road(id=id+increment, uid=id+increment, road_name=name,road_begin=start_place,
                                                   road_end=end_place, areaid=district_id, roadlength=length,
                                                   remark1=remark1, remark2=remark2, remark3=remark3)
        with transaction.atomic():
            cur_guard_road.save()
    else:
        id = instance.id
        name = instance.name
        start_place = instance.start_place
        end_place = instance.end_place
        length = instance.length
        district_id = instance.district_id
        remark1 = instance.remark1
        remark2 = instance.remark2
        remark3 = instance.remark3
        enabled = str(int(instance.enabled))
        guard_road.objects.filter(uid=id+increment).update(uid=id+increment, road_name=name,road_begin=start_place,
                                                   road_end=end_place, areaid=district_id, roadlength=length,
                                                   remark1=remark1, remark2=remark2, remark3=remark3, enabled=enabled)
    related_service_line_list = instance.Road_Service.filter(enabled=True).distinct()
    for item in related_service_line_list:
        generate_service_line_points(item.id)


def road_faculty_change(sender, instance, model, action, pk_set, **kwargs):
    faculty_type = str(sender).split('\'')[1].split('.')[-1].split('_')[-1]
    if action == 'post_add':
        for item in pk_set:
            if faculty_type == 'chief':
                duty_name = u'路长'
                order_list = 1
            if faculty_type == 'bureau':
                duty_name = u'执行路长(分局)'
                order_list = 2
            if faculty_type == 'trans':
                duty_name = u'执行路长(交管)'
                order_list = 3
            if faculty_type == 'poli':
                duty_name = u'执行路长(武警)'
                order_list = 4
            count = is_already_in_use(item)
            # 无其他职位
            if count < 2:
                guard_admin.objects.filter(uid=item+increment).update(dutyname=duty_name, orderlist=order_list,
                                                                     category='1', mainid=instance.id+increment,
                                                                      radio_station=instance.channel,
                                                                      call=instance.call_sign)
            # 有其他职位
            else:
                cur_faculty = Faculty.objects.filter(id=item).first()
                username = cur_faculty.name
                duties = cur_faculty.duty
                phone = cur_faculty.mobile
                radio_station = instance.channel
                call = instance.call_sign
                count = guard_admin.objects.count()
                cur_guard_admin = guard_admin(uid=item+increment, username=username, duties=duties,id=count+1,
                                                             phone=phone, radio_station=radio_station, call=call,
                                                             dutyname=duty_name, orderlist=order_list,
                                                             category='1', mainid=instance.id + increment)
                with transaction.atomic():
                    cur_guard_admin.save()
    if action == 'post_remove':
        for item in pk_set:
            if faculty_type == 'chief':
                order_list = 1
            if faculty_type == 'bureau':
                order_list = 2
            if faculty_type == 'trans':
                order_list = 3
            if faculty_type == 'poli':
                order_list = 4
            count = is_already_in_use(item)
            # 还有其他职位
            if count:
                guard_admin.objects.filter(uid=item+increment, orderlist=order_list,
                                           category='1', mainid=instance.id + increment).\
                    delete()
            else:
                guard_admin.objects.filter(uid=item+increment).\
                    update(dutyname=None, orderlist=None, category=None, mainid=None)


signals.m2m_changed.connect(road_faculty_change, sender=Road.chief.through)
signals.m2m_changed.connect(road_faculty_change, sender=Road.exec_chief_sub_bureau.through)
signals.m2m_changed.connect(road_faculty_change, sender=Road.exec_chief_trans.through)
signals.m2m_changed.connect(road_faculty_change, sender=Road.exec_chief_armed_poli.through)


@receiver(signals.post_save, sender=ServiceLine)
def create_update_service_line(sender, instance, created, **kwargs):
    if created:
        id = instance.id
        name = instance.name
        startPlace = instance.startPlace
        endPlace = instance.endPlace
        count = ServiceLine.objects.filter(name=name, enabled=True).count()
        if count > 1:
            direction = '2'
            used = '0'
            line_id = str(ServiceLine.objects.filter(name=name, enabled=True).order_by('id').first().id+increment)
            # reverse start and end
            tmp = startPlace
            startPlace = endPlace
            endPlace = tmp

        else:
            direction = '1'
            used = '1'
            line_id = str(id+increment)
        cur_guard_line = guard_line(id=id+increment, uid=id+increment, name=name, begins=startPlace, used=used,
                                                   ends=endPlace, qwid=id+increment, direction=direction, line_id=line_id)
        with transaction.atomic():
            cur_guard_line.save()
    else:
        id = instance.id
        name = instance.name
        startPlace = instance.startPlace
        endPlace = instance.endPlace
        enabled = str(int(instance.enabled))
        cur_guard_line = guard_line.objects.filter(uid=id+increment)
        cur_guard_line.update(name=name, begins=startPlace, ends=endPlace, enabled=enabled)
    generate_service_line_points(instance.id)
