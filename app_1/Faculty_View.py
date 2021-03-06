# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from models import Faculty, Road, Section, Station
from constants import error_constants
from api_tools.api_tools import generate_error_response, \
    check_faculty_count_particular_role, is_already_in_use
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Serializers.serializers import FacultySerializer
from api_tools.token import SystemAuthentication


class FacultyView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            name = request.POST.get('name', '')
            mobile = request.POST.get('mobile', '')
            duty = request.POST.get('duty', '')
            district_id = int(request.POST.get('districtId', 0))
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            level = int(request.POST.get('level', 0))
            role = int(request.POST.get('role', 0))
            road_section_station = int(request.POST.get('road_section_station', 0))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        if not name or not mobile:
            return generate_error_response(error_constants.ERR_NO_NAME_MOBILE, status.HTTP_400_BAD_REQUEST)
        # cur_faculty = Faculty.objects.filter(name=name, mobile=mobile)
        # if cur_faculty.exists():
        #     cur_faculty.update(enabled=True)
        else:
            main_name = ''
            if level and road_section_station:
                if level == 1:
                    main_name = Road.objects.get(id=road_section_station).name
                if level == 2:
                    main_name = Section.objects.get(id=road_section_station).name
                if level == 3:
                    main_name = Station.objects.get(id=road_section_station).name
            cur_faculty = Faculty(district_id=district_id, name=name, mobile=mobile, duty=duty,
                                                 channel=channel, call_sign=call_sign, level=level, role=role,
                                                 main_id=road_section_station, main_name=main_name)
            # 岗位人数限制
            count = check_faculty_count_particular_role(cur_faculty)
            if count >= 4:
                return generate_error_response(error_constants.ERR_FACULTY_EXCEED_COUNT, status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    with transaction.atomic():
                        cur_faculty.save()
                except Exception as ex:
                    print 'function name: ', __name__
                    print Exception, ":", ex
                    return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                                   status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            faculty_id = request.POST.get('facultyId')
            name = request.POST.get('name', '')
            mobile = request.POST.get('mobile', '')
            duty = request.POST.get('duty', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            level = int(request.POST.get('level', 0))
            role = int(request.POST.get('role', 0))
            road_section_station = int(request.POST.get('road_section_station', 0))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        cur_faculty = Faculty.objects.get(id=faculty_id)
        cur_faculty.mobile = mobile
        cur_faculty.name = name
        cur_faculty.duty = duty
        cur_faculty.channel = channel
        cur_faculty.call_sign = call_sign
        if not is_already_in_use(faculty_id):
            cur_faculty.level = level
            cur_faculty.role = role
            cur_faculty.main_id = road_section_station

        # 岗位人数限制
        count = check_faculty_count_particular_role(cur_faculty)
        if count >= 4:
            return generate_error_response(error_constants.ERR_FACULTY_EXCEED_COUNT, status.HTTP_400_BAD_REQUEST)
        else:
            with transaction.atomic():
                cur_faculty.save()
        return Response(response_data, status=status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            faculty_id = int(request.GET.get('facultyId', 0))
            district_id = int(request.GET.get('districtId', 0))
            cur_per_page = int(request.GET.get('perPage', 20))
            page = int(request.GET.get('page', 1))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        if faculty_id:
            cur_faculty = Faculty.objects.get(id=faculty_id)
            serializer = FacultySerializer(cur_faculty)
            response_data['data'] = serializer.data
        else:
            cur_faculty = Faculty.objects.filter(enabled=True).order_by('-id')
            if district_id:
                cur_faculty = cur_faculty.filter(district_id=district_id).order_by('-id')
            paginator = Paginator(cur_faculty, cur_per_page)
            page_count = paginator.num_pages

            try:
                faculty_lists = paginator.page(page)
            except PageNotAnInteger:
                page = 1
                faculty_lists = paginator.page(page)
            except EmptyPage:
                page = paginator.num_pages
                faculty_lists = paginator.page(page)
            serializer = FacultySerializer(faculty_lists, many=True)
            response_data['data'] = {}
            response_data['data']['curPage'] = page
            response_data['data']['listCount'] = paginator.count
            response_data['data']['list'] = serializer.data
            response_data['data']['pageCount'] = page_count
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            faculty_id = int(request.GET.get('facultyId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        try:
            Faculty.objects.filter(id=faculty_id).update(enabled=False)
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)


class DeleteFacultyView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self,request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            faculty_id = int(request.GET.get('facultyId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        cur_faculty.enabled = False
        try:
            with transaction.atomic():
                cur_faculty.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)