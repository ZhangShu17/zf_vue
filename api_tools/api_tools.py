# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response

from app_1.models import Road, Section, Station, Faculty, ServiceLine
from constants.constants import increment
from constants.constants import pattern
from t.models import guard_line, guard_road


def generate_error_response(error_message, error_type):
    print('shshhshshshshsh')
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
        print('road add sectionid')
        if not cur_road.sectionids:
            cur_road.sectionids = str(section_id)
        else:
            cur_road.sectionids = cur_road.sectionids + '-' + str(section_id)
    else:
        print('remove roadid')
        sectionids = cur_road.sectionids.split('-')
        sectionids.remove(str(section_id))
        sectionids_str = '-'.join(sectionids)
        cur_road.sectionids = sectionids_str
    cur_road.save()


def update_service_line_road_ids(service_line_id, road_id, bollen):
    cur_service_line = ServiceLine.objects.get(id=service_line_id)
    if bollen:
        print('serviceline add road')
        if not cur_service_line.roadids:
            print('yes')
            cur_service_line.roadids = str(road_id)
        else:
            cur_service_line.roadids = cur_service_line.roadids + '-' + str(road_id)
        print(guard_road.objects.get(id=road_id+increment).road_name)
        guard_road.objects.filter(uid=road_id+increment).update(lineid=service_line_id+increment)
    else:
        print('serviceline remove roadid')
        roadids = cur_service_line.roadids.split('-')
        roadids.remove(str(road_id))
        roadids_str = '-'.join(roadids)
        cur_service_line.roadids = roadids_str
        guard_road.objects.filter(id=road_id+increment).update(lineid=None)
    cur_service_line.save()


def generate_service_line_points(service_line_id):
    print 'generate_service_line_points'
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
        begin_point, end_point, points_str = handle(point_list, direction)
        guard_line.objects.filter(uid=service_line_id+increment).\
            update(points=points_str, begin_point=begin_point, end_point=end_point)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!Done!!!!!!!!!!!!!!!!!!!!!!!!!!!')


def handle(point_list, direction):
    print point_list
    points_str = ','.join(point_list)
    point_list1 = points_str.split(',')
    print point_list1
    new_points = []
    if(direction == 2):
        for i in range(0, len(point_list1), 2):
            new_points.append(point_list1[i:i + 2])
        for i in range(0, len(new_points) / 2, 1):
            temp_points = new_points[i]
            new_points[i] = new_points[len(new_points) - 1 - i]
            new_points[len(new_points) - 1 - i] = temp_points
        point_list1 = new_points
        print 'reverse points:'
        print point_list1
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
    if district_id_road not in road_id_list:
        pass
    else:
        district_id_ser.remove(str(district_id_road))
        if len(district_id_ser):
            cur_service.submit_district = '-'.join(district_id_ser)
        else:
            cur_service.submit_district = ''
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
            item.save()
        for item in cur_road.exec_chief_sub_bureau.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            item.save()
        for item in cur_road.exec_chief_trans.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            item.save()
        for item in cur_road.exec_chief_armed_poli.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
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
            item.save()
        for item in cur_section.exec_chief_sub_bureau.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            item.save()
        for item in cur_section.exec_chief_trans.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            item.save()
        for item in cur_section.exec_chief_armed_poli.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
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
            item.save()
        for item in cur_station.exec_chief_trans.all():
            item.main_name = main_name
            item.channel = channel
            item.call_sign = call_sign
            item.save()


def check_faculty_count_particular_role(instance):
    # 表示新创建的人员
    level = instance.level
    role = instance.role
    main_id = instance.main_id
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
                count = Faculty.objects.filter(level=level, role=role, main_id=main_id, enabled=True).count()
            else:  # 表示更新
                faculty_id = instance.id
                count = Faculty.objects.filter(level=level, role=role, main_id=main_id, enabled=True).\
                    exclude(id=faculty_id).count()
        else:
            count = 0
    return count
