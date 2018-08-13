# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from app_1.models import Road, Section, Station, Faculty
from django.db.models import Q
import tokenlib


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
   count = count + cur_faculty.Faculty_Road_Exec_Chief_Trans.distinct().count()
   count = count + cur_faculty.Faculty_Section_Exec_Chief_Armed_Poli.distinct().count()
   count = count + cur_faculty.Faculty_Station_Chief.distinct().count()
   count = count + cur_faculty.Faculty_Station_Exec_Chief_Trans.distinct().count()
   print('打印用户岗位数量')
   print(count)
   return count