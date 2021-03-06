# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from app_1.models import Road, Section, Station, Faculty, ServiceLine
from t.models import guard_line, guard_road
from constants import error_constants
from constants.constants import increment
from constants.constants import pattern
from django.db import transaction
from rest_framework import status


def generate_error_response(error_message, error_type):
    return Response({'retCode': error_message[0],
                     'retMsg': error_message[1]}, error_type)


# 判断人员是否有新的岗位
def is_already_in_use(faculty_id):
   cur_faculty = Faculty.objects.get(id=faculty_id)
   count = cur_faculty.Faculty_Road_Chief.distinct().count()
   count = count + cur_faculty.Faculty_Road_Exec_Chief_Sub_Bureau.distinct().count()
   count = count + cur_faculty.Faculty_Road_Exec_Chief_Trans.distinct().count()
   count = count + cur_faculty.Faculty_Road_Exec_Chief_Armed_Poli.distinct().count()
   count = count + cur_faculty.Faculty_Section_Chief.distinct().count()
   count = count + cur_faculty.Faculty_Section_Exec_Chief_Sub_Bureau.distinct().count()
   count = count + cur_faculty.Faculty_Section_Exec_Chief_Trans.distinct().count()
   count = count + cur_faculty.Faculty_Section_Exec_Chief_Armed_Poli.distinct().count()
   count = count + cur_faculty.Faculty_Station_Chief.distinct().count()
   count = count + cur_faculty.Faculty_Station_Exec_Chief_Trans.distinct().count()
   return count


def update_road_section_ids(road_id, section_id, bollen):
    cur_road = Road.objects.get(id=road_id)
    if bollen:
        if not cur_road.sectionids:
            cur_road.sectionids = str(section_id)
        else:
            cur_road.sectionids = cur_road.sectionids + '-' + str(section_id)
    else:
        sectionids = cur_road.sectionids.split('-')
        sectionids.remove(str(section_id))
        sectionids_str = '-'.join(sectionids)
        cur_road.sectionids = sectionids_str
    with transaction.atomic():
        cur_road.save()


def update_service_line_road_ids(service_line_id, road_id, bollen):
    cur_service_line = ServiceLine.objects.get(id=service_line_id)
    if bollen:
        if not cur_service_line.roadids:
            cur_service_line.roadids = str(road_id)
        else:
            cur_service_line.roadids = cur_service_line.roadids + '-' + str(road_id)
        guard_road.objects.filter(uid=road_id+increment).update(lineid=service_line_id+increment)
    else:
        roadids = cur_service_line.roadids.split('-')
        roadids.remove(str(road_id))
        roadids_str = '-'.join(roadids)
        cur_service_line.roadids = roadids_str
        guard_road.objects.filter(id=road_id+increment).update(lineid=None)
    with transaction.atomic():
        cur_service_line.save()


def generate_service_line_points(service_line_id):
    cur_service_line = ServiceLine.objects.get(id=service_line_id)
    road_ids = cur_service_line.roadids
    if not road_ids:
        guard_line.objects.filter(uid=service_line_id + increment). \
            update(points='', begin_point='', end_point='')
    else:
        # generate points by the direction
        direction = guard_line.objects.filter(uid=service_line_id+increment).first().direction
        print 'generate_service_line_points,direction:'+direction
        road_id_list = road_ids.split('-')
        point_list = []
        for road_id in road_id_list:
            cur_road = Road.objects.get(id=int(road_id))
            section_ids = cur_road.sectionids
            if not section_ids:
                continue
            section_id_list = section_ids.split('-')
            for section_id in section_id_list:
                cur_section = Section.objects.get(id=int(section_id))
                if pattern.search(cur_section.xy_coordinate):
                    point_list.append(cur_section.xy_coordinate)
        begin_point, end_point, points_str = handle(point_list)
        guard_line.objects.filter(uid=service_line_id+increment).\
            update(points=points_str, begin_point=begin_point, end_point=end_point)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!Done!!!!!!!!!!!!!!!!!!!!!!!!!!!')


def handle(point_list):
    points_str = ','.join(point_list)
    point_list1 = points_str.split(',')
    begin_point = ''
    end_point = ''
    for item in point_list1:
        if not pattern.search(item):
            point_list1.remove(item)
    if len(point_list1):
        begin_point = point_list1[0] + ',' + point_list1[1]
        end_point = point_list1[-2] + ',' + point_list1[-1]
    return begin_point, end_point, points_str


def update_service_submit(service_line_id, road_id):
    cur_service = ServiceLine.objects.get(id=service_line_id)
    cur_road = Road.objects.get(id=road_id)
    district_id_ser = cur_service.submit_district.split('-')
    district_id_road = cur_road.district_id
    road_id_list = cur_service.road.values_list('district_id', flat=True).distinct()
    # 如果该区没有提交，或者该区还有其他道路在勤务路线，则pass
    if str(district_id_road) not in district_id_ser or district_id_road in road_id_list:
        pass
    else:
        district_id_ser.remove(str(district_id_road))
        if len(district_id_ser):
            cur_service.submit_district = '-'.join(district_id_ser)
        else:
            cur_service.submit_district = ''
        with transaction.atomic():
            cur_service.save()


def update_faculty_channel_call_sign(level, element_id):
    if level == 1:
        cur_road = Road.objects.get(id=element_id)
        channel = cur_road.channel
        main_name = cur_road.name
        call_sign = cur_road.call_sign
        for item in cur_road.chief.all():
            item.channel = channel
            item.main_name = main_name
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
        for item in cur_road.exec_chief_sub_bureau.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
        for item in cur_road.exec_chief_trans.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
        for item in cur_road.exec_chief_armed_poli.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
    if level == 2:
        cur_section = Section.objects.get(id=element_id)
        main_name = cur_section.name
        channel = cur_section.channel
        call_sign = cur_section.call_sign
        for item in cur_section.chief.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
        for item in cur_section.exec_chief_sub_bureau.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
        for item in cur_section.exec_chief_trans.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
        for item in cur_section.exec_chief_armed_poli.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
    if level == 3:
        cur_station = Station.objects.get(id=element_id)
        main_name = cur_station.name
        channel = cur_station.channel
        call_sign = cur_station.call_sign
        for item in cur_station.chief.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()
        for item in cur_station.exec_chief_trans.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            with transaction.atomic():
                item.save()


def check_faculty_count_particular_role(instance):
    # 表示新创建的人员
    level = instance.level
    role = instance.role
    main_id = instance.main_id
    main_name = instance.main_name
    # if not instance.id:
    #     count = Faculty.objects.filter(level=level, role=role, main_id=main_id, enabled=True).count()
    # # 表示更新的
    # else:
    #     faculty_id = instance.id
    #     count = Faculty.objects.filter(level=level, role=role, main_id=main_id, enabled=True).\
    #         exclude(id=faculty_id).count()
    # return count
    district_id = instance.district_id
    # 天安门地区人员放开限制
    if int(district_id) == 1:
        count = 0
    else:
        # 表示角色是确定了的
        if level and role and main_id:
            # 表示创建
            if not instance.id:
                count = Faculty.objects.filter(level=level, role=role, main_name=main_name, enabled=True).count()
                print 'count:', count
            else:  # 表示更新
                faculty_id = instance.id
                count = Faculty.objects.filter(level=level, role=role, main_name=main_name, enabled=True).\
                    exclude(id=faculty_id).count()
        else:
            count = 0
    return count


# 将岗及岗的人员复制并关联给段
def copy_station_to_new_section(new_section, old_section):
    station_list = old_section.Section_Station.all()
    for station in station_list:
        chief = station.chief.all()
        exec_chief_trans = station.exec_chief_trans.all()
        new_station = Station(district_id=station.district_id, name=station.name, location=station.location,
                              section_id=new_section.id, remark1=station.remark1, remark2=station.remark2,
                              remark3=station.remark3, channel=station.channel, call_sign=station.call_sign,
                              enabled=station.enabled)
        try:
            with transaction.atomic():
                new_station.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                           status.HTTP_500_INTERNAL_SERVER_ERROR)
        for item in chief:
            new_station.chief.add(item)
        for item in exec_chief_trans:
            new_station.exec_chief_trans.add(item)


# 复制路时触发
def copy_section_to_new_road(new_road, old_road):
    section_list = old_road.Road_Section.all()
    str_list = []
    for section in section_list:
        chief = section.chief.all()
        exec_chief_sub_bureau = section.exec_chief_sub_bureau.all()
        exec_chief_trans = section.exec_chief_trans.all()
        exec_chief_armed_poli = section.exec_chief_armed_poli.all()
        new_section = Section(district_id=section.district_id, name=section.name,
                                             start_place=section.start_place, end_place=section.end_place,
                                             xy_coordinate=section.xy_coordinate, road_id=new_road.id,
                                             remark1=section.remark1, remark2=section.remark2, remark3=section.remark3,
                                             channel=section.channel, call_sign=section.call_sign,
                                             enabled=section.enabled)
        try:
            with transaction.atomic():
                new_section.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                           status.HTTP_500_INTERNAL_SERVER_ERROR)
        str_list.append(str(new_section.id))
        for item in chief:
            new_section.chief.add(item)
        for item in exec_chief_armed_poli:
            new_section.exec_chief_armed_poli.add(item)
        for item in exec_chief_trans:
            new_section.exec_chief_trans.add(item)
        for item in exec_chief_sub_bureau:
            new_section.exec_chief_sub_bureau.add(item)
        copy_station_to_new_section(new_section, section)
    new_road.sectionids = '-'.join(str_list)
    with transaction.atomic():
        new_road.save()
