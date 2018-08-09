# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from models import Road, Faculty, Section
from constants import error_constants
from django.db.models import Q
from api_tools.api_tools import generate_error_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Serializers.serializers import SectionSerializer, SingleSectionSerializer, FacultySerializer
from api_tools.token import SystemAuthentication


class SectionView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.POST.get('roadId', 0))
            name = request.POST.get('name')
            start_place = request.POST.get('startPlace')
            end_place = request.POST.get('endPlace')
            start_point = request.POST.get('startPoint')
            end_point = request.POST.get('endPoint')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        if road_id:
            cur_section = Section.objects.create(name=name, start_place=start_place, end_place=end_place,
                                                 start_point=start_point, end_point=end_point, road_id=road_id,
                                                 remark1=remark_1, remark2=remark_2, remark3=remark_3)
            try:
                with transaction.atomic():
                    cur_section.save()
            except Exception as ex:
                print 'function name: ', __name__
                print Exception, ":", ex
                return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                               status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            cur_section = Section.objects.create(name=name, start_place=start_place, end_place=end_place,
                                                 start_point=start_point, end_point=end_point, remark1=remark_1,
                                                 remark2=remark_2, remark3=remark_3)
            try:
                with transaction.atomic():
                    cur_section.save()
            except Exception as ex:
                print 'function name: ', __name__
                print Exception, ":", ex
                return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                               status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response_data, status=status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.GET.get('roadId', 0))
            district_id = int(request.GET.get('districtId', 0))
            cur_per_page = int(request.GET.get('perPage', 20))
            page = int(request.GET.get('page', 1))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        if road_id:
            cur_section = Section.objects.filter(enabled=1, road_id=road_id).order_by('id')
        else:
            cur_section = Section.objects.filter(enabled=1).order_by('id')
        if district_id:
            cur_section = cur_section.filter(district_id=district_id).order_by('id')
        paginator = Paginator(cur_section, cur_per_page)
        page_count = paginator.num_pages

        try:
            section_lists = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            section_lists = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            section_lists = paginator.page(page)
        serializer = SectionSerializer(section_lists, many=True)
        response_data['data'] = {}
        response_data['data']['curPage'] = page
        response_data['data']['listCount'] = paginator.count
        response_data['data']['list'] = serializer.data
        response_data['data']['pageCount'] = page_count
        return Response(response_data, status.HTTP_200_OK)

    def put(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.POST.get('sectionId'))
            name = request.POST.get('name', '')
            start_place = request.POST.get('startPlace', '')
            end_place = request.POST.get('endPlace', '')
            start_point = request.POST.get('startPoint', '')
            end_point = request.POST.get('endPoint', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.filter(id=section_id)
        if name:
            cur_section.update(name=name)
        if start_place:
            cur_section.update(start_place=start_place)
        if end_place:
            cur_section.update(end_place=end_place)
        if start_point and end_point:
            if cur_section.first().start_point != start_point or cur_section.first().end_point != end_point:
                cur_section.update(start_point=start_point, end_point=end_point)
        if remark_1:
            cur_section.update(remark1=remark_1)
        if remark_2:
            cur_section.update(remark1=remark_2)
        if remark_3:
            cur_section.update(remark1=remark_3)
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.GET.get('sectionId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        Section.objects.filter(id=section_id).update(enabled=False)
        return Response(response_data, status.HTTP_200_OK)


class DeleteSectionView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self,request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.GET.get('sectionId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        Section.objects.filter(id=section_id).update(enabled=False)
        return Response(response_data, status.HTTP_200_OK)


# 获取该条道路人员信息
class SectionFacultyView(APIView):
    authentication_classes = (SystemAuthentication,)

    # 添加人员信息
    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.POST.get('sectionId'))
            # faculty_id = int(request.POST.get('facultyId'))
            name = request.POST.get('name', '')
            mobile = request.POST.get('mobile', '')
            duty = request.POST.get('duty', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            # faculty_type 1 段长；2 执行段长 分局；3： 执行段长 交通；4：执行段长 武警
            faculty_type = int(request.POST.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        cur_faculty = Faculty.objects.filter(name=name, mobile=mobile)
        if cur_faculty.exists():
            cur_faculty.update(enabled=True)
            cur_faculty = cur_faculty.first()
        else:
            cur_faculty = Faculty.objects.create(name=name, mobile=mobile, duty=duty,
                                                 channel=channel, call_sign=call_sign)
            try:
                with transaction.atomic():
                    cur_faculty.save()
            except Exception as ex:
                print 'function name: ', __name__
                print Exception, ":", ex
                return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                               status.HTTP_500_INTERNAL_SERVER_ERROR)
        if faculty_type == 1:
            cur_section.chief.add(cur_faculty)
        if faculty_type == 2:
            cur_section.exec_chief_sub_bureau.add(cur_faculty)
        if faculty_type == 3:
            cur_section.exec_chief_trans.add(cur_faculty)
        if faculty_type == 4:
            cur_section.exec_chief_armed_poli.add(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.GET.get('sectionId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        serializer = SingleSectionSerializer(cur_section)
        response_data['data'] = serializer.data
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.GET.get('sectionId'))
            faculty_id = int(request.GET.get('facultyId'))
            # faculty_type 1 路长；2 执行路长 分局；3： 执行路长 交通；4：执行路长 武警
            faculty_type = int(request.GET.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        if faculty_type == 1:
            cur_section.chief.remove(cur_faculty)
        if faculty_type == 2:
            cur_section.exec_chief_sub_bureau.remove(cur_faculty)
        if faculty_type == 3:
            cur_section.exec_chief_trans.remove(cur_faculty)
        if faculty_type == 4:
            cur_section.exec_chief_armed_poli.remove(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)


class SingleSectionView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.GET.get('sectionId', 0))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(enabled=1, id=section_id)
        serializer = SectionSerializer(cur_section)
        response_data['data'] = serializer.data
        return Response(response_data, status.HTTP_200_OK)


# 删除路段人员
class DeleteSectionFacultyView(APIView):
    authentication_classes = (SystemAuthentication,)
    def get(self,request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.GET.get('sectionId'))
            faculty_id = int(request.GET.get('facultyId'))
            # faculty_type 1 路长；2 执行路长 分局；3： 执行路长 交通；4：执行路长 武警
            faculty_type = int(request.GET.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        if faculty_type == 1:
            cur_section.chief.remove(cur_faculty)
        if faculty_type == 2:
            cur_section.exec_chief_sub_bureau.remove(cur_faculty)
        if faculty_type == 3:
            cur_section.exec_chief_trans.remove(cur_faculty)
        if faculty_type == 4:
            cur_section.exec_chief_armed_poli.remove(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)


class SectionNotInToRoadView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'dataList': []}
        try:
            road_id = int(request.GET.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_road = Road.objects.get(id=road_id)
        # 当前道路district_id
        cur_road_district_id = cur_road.district_id
        # 当前道路路段id
        cur_road_section_id_lists = cur_road.Road_Section.all().values_list('id', flat=True)

        cur_section_list = Section.objects.filter(enabled=True, district_id=cur_road_district_id,
                                                  road_id__isnull=True).exclude(id__in=cur_road_section_id_lists)
        response_data['dataList'] = SectionSerializer(cur_section_list, many=True).data
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.POST.get('roadId'))
            section_id = int(request.POST.get('sectionId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        Section.objects.filter(id=section_id).update(road_id=road_id)
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.data.get('roadId'))
            section_id = int(request.data.get('sectionId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        Section.objects.filter(id=section_id).update(road_id=None)
        return Response(response_data, status.HTTP_200_OK)


class FacultyNotInSection(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data':{
                             'chiefList': [],
                             'execChiefSubBureauList': [],
                             'execChiefTransList': [],
                             'execChiefArmedPoliList': []}
                         }
        try:
            section_id = int(request.GET.get('sectionId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        district_id = cur_section.district_id
        chief_list = cur_section.chief.all().values_list('id', flat=True)
        bureau_list = cur_section.exec_chief_sub_bureau.all().values_list('id', flat=True)
        trans_list = cur_section.exec_chief_trans.all().values_list('id', flat=True)
        poli_list = cur_section.exec_chief_armed_poli.all().values_list('id', flat=True)
        cur_chief_list = Faculty.objects.filter(enabled=True, district_id=district_id).\
            exclude(id__in=chief_list).order_by('id')
        cur_bureau_list = Faculty.objects.filter(enabled=True, district_id=district_id).\
            exclude(id__in=bureau_list).order_by('id')
        cur_trans_list = Faculty.objects.filter(enabled=True, district_id=district_id).\
            exclude(id__in=trans_list).order_by('id')
        cur_poli_list = Faculty.objects.filter(enabled=True, district_id=district_id).\
            exclude(id__in=poli_list).order_by('id')
        response_data['data']['chiefList'] = FacultySerializer(cur_chief_list, many=True).data
        response_data['data']['execChiefSubBureauList'] = FacultySerializer(cur_bureau_list, many=True).data
        response_data['data']['execChiefTransList'] = FacultySerializer(cur_trans_list, many=True).data
        response_data['data']['execChiefArmedPoliList'] = FacultySerializer(cur_poli_list, many=True).data
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.POST.get('sectionId'))
            faculty_id = int(request.POST.get('facultyId'))
            faculty_type = int(request.POST.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        if faculty_type == 1:
            cur_section.chief.add(cur_faculty)
        if faculty_type == 2:
            cur_section.exec_chief_sub_bureau.add(cur_faculty)
        if faculty_type == 3:
            cur_section.exec_chief_trans.add(cur_faculty)
        if faculty_type == 4:
            cur_section.exec_chief_armed_poli.add(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)

