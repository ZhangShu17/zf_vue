# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from app_1.models import Road, Section, Station, Faculty, ServiceLine
from t.models import guard_line
from constants.constants import increment


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
    else:
        print('serviceline remove roadid')
        roadids = cur_service_line.roadids.split('-')
        roadids.remove(str(road_id))
        roadids_str = '-'.join(roadids)
        cur_service_line.roadids = roadids_str
    cur_service_line.save()


def generate_service_line_points(service_line_id):
    cur_service_line = ServiceLine.objects.get(id=service_line_id)
    road_ids = cur_service_line.roadids
    print('road_ids=', road_ids)
    if not road_ids:
        guard_line.objects.filter(uid=service_line_id + increment). \
            update(points='', begin_point='', end_point='')
        return
    road_id_list = road_ids.split('-')
    point_list = []
    for road_id in road_id_list:
        cur_road = Road.objects.get(id=int(road_id))
        section_ids = cur_road.sectionids
        if not section_ids:
            break
        section_id_list = section_ids.split('-')
        for section_id in section_id_list:
            cur_section = Section.objects.get(id=int(section_id))
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
        if not item:
            point_list1.remove(item)
    if len(point_list1):
        begin_point = point_list1[0] + ',' + point_list1[1]
        end_point = point_list1[-2] + ',' + point_list1[-1]
    return begin_point, end_point, points_str