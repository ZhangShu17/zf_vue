# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from models import Road, Faculty, Section
from t.models import guard_road
from constants import error_constants
from django.db.models import Q
from api_tools.api_tools import generate_error_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Serializers.serializers import SectionSerializer, SingleSectionSerializer, FacultySerializer
from api_tools.token import SystemAuthentication
from constants.constants import increment
from api_tools.api_tools import update_road_section_ids


class SectionView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.POST.get('roadId', 0))
            district_id = int(request.POST.get('districtId'))
            name = request.POST.get('name')
            start_place = request.POST.get('startPlace')
            end_place = request.POST.get('endPlace')
            xy_coordinate = request.POST.get('XYCOORDINATE', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        if road_id:
            cur_section = Section.objects.create(name=name, start_place=start_place, end_place=end_place,
                                                 xy_coordinate=xy_coordinate, road_id=road_id, channel=channel,
                                                 call_sign=call_sign, remark1=remark_1, remark2=remark_2,
                                                 remark3=remark_3, district_id=district_id)

            try:
                with transaction.atomic():
                    cur_section.save()
            except Exception as ex:
                print 'function name: ', __name__
                print Exception, ":", ex
                return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                               status.HTTP_500_INTERNAL_SERVER_ERROR)
            update_road_section_ids(road_id, cur_section.id, True)
        else:
            cur_section = Section.objects.create(name=name, start_place=start_place,
                                                 end_place=end_place, xy_coordinate=xy_coordinate,
                                                 remark1=remark_1, channel=channel, call_sign=call_sign,
                                                 remark2=remark_2, remark3=remark_3, district_id=district_id)
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
            road_name = ''
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        if road_id:
            road_name = Road.objects.get(id = road_id).name
            cur_section = Section.objects.filter(enabled=1, road_id=road_id).order_by('-id')
        else:
            cur_section = Section.objects.filter(enabled=1).order_by('-id')
        if district_id:
            cur_section = cur_section.filter(district_id=district_id).order_by('-id')
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
        response_data['data']['roadName'] = road_name
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
            xy_coordinate = request.POST.get('XYCOORDINATE', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        if name:
            cur_section.name = name
        if start_place:
            cur_section.start_place = start_place
        if end_place:
            cur_section.end_place = end_place
        if xy_coordinate:
            cur_section.xy_coordinate = xy_coordinate
        if channel:
            cur_section.channel = channel
        if call_sign:
            cur_section.call_sign = call_sign
        if remark_1:
            cur_section.remark1 = remark_1
        if remark_2:
            cur_section.remark2 = remark_2
        if remark_3:
            cur_section.remark3 = remark_3
        cur_section.save()
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
        cur_section = Section.objects.get(id=section_id)
        cur_section.enabled = False
        cur_section.save()

        # 更新road的sectionids字段
        if cur_section.road_id:
            update_road_section_ids(cur_section.road_id, section_id, False)

        # 路的段/岗书数量更新
        road_id = cur_section.road_id
        if road_id:
            station_num = cur_section.Section_Station.filter(enabled=True).count()
            cur_guard_road = guard_road.objects.get(uid=road_id+increment)
            cur_guard_road.sectionnum = cur_guard_road.sectionnum - 1
            cur_guard_road.stationnum = cur_guard_road.stationnum - station_num
            cur_guard_road.save()
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
            district_id = int(request.POST.get('districtId', 0))
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
                                                 district_id=district_id, channel=channel, call_sign=call_sign)
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
        cur_faculty.channel = ''
        cur_faculty.call_sign = ''
        cur_faculty.save()
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
        cur_section = Section.objects.get(id=section_id)
        cur_section.road_id = road_id
        cur_section.save()

        # 修改road的sectionids字段
        update_road_section_ids(road_id, section_id, True)
        print('road add section')
        print(road_id)
        # 路的段/岗数据更新
        station_num = cur_section.Section_Station.filter(enabled=True).count()
        cur_guard_road = guard_road.objects.get(uid=road_id + increment)
        cur_guard_road.sectionnum = cur_guard_road.sectionnum + 1
        cur_guard_road.stationnum = cur_guard_road.stationnum + station_num
        cur_guard_road.save()
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
        cur_section = Section.objects.get(id=section_id)
        cur_section.road_id = None
        cur_section.save()

        # 更新road 的sectionids
        update_road_section_ids(road_id, section_id, False)

        # 路的段/岗数据更新
        station_num = cur_section.Section_Station.filter(enabled=True).count()
        cur_guard_road = guard_road.objects.get(uid=road_id + increment)
        cur_guard_road.sectionnum = cur_guard_road.sectionnum - 1
        cur_guard_road.stationnum = cur_guard_road.stationnum - station_num
        cur_guard_road.save()
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
        cur_chief_list = Faculty.objects.filter(enabled=True, district_id=district_id,
                                                level=2, role=1, main_id=section_id).\
            exclude(id__in=chief_list).order_by('id')
        cur_bureau_list = Faculty.objects.filter(enabled=True, district_id=district_id,
                                                 level=2, role=2, main_id=section_id).\
            exclude(id__in=bureau_list).order_by('id')
        cur_trans_list = Faculty.objects.filter(enabled=True, district_id=district_id,
                                                level=2, role=3, main_id=section_id).\
            exclude(id__in=trans_list).order_by('id')
        cur_poli_list = Faculty.objects.filter(enabled=True, district_id=district_id,
                                               level=2, role=4, main_id=section_id).\
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
        cur_faculty.channel = cur_section.channel
        cur_faculty.call_sign = cur_section.call_sign
        cur_faculty.save()
        return Response(response_data, status.HTTP_200_OK)


class CopySectionView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.POST.get('sectionId'))
            name = request.POST.get('name')
            start_place = request.POST.get('startPlace')
            end_place = request.POST.get('endPlace')
            xy_coordinate = request.POST.get('XYCOORDINATE', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        district_id = cur_section.district_id
        road_id = cur_section.road_id
        new_section = Section.objects.create(name=name, start_place=start_place, channel=channel, call_sign=call_sign,
                                             end_place=end_place, xy_coordinate=xy_coordinate,
                                             remark1=remark_1, remark2=remark_2, remark3=remark_3,
                                             district_id=district_id)
        try:
            with transaction.atomic():
                new_section.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                           status.HTTP_500_INTERNAL_SERVER_ERROR)
        chief = cur_section.chief.all()
        bureau = cur_section.exec_chief_sub_bureau.all()
        trans = cur_section.exec_chief_trans.all()
        arm_poli = cur_section.exec_chief_armed_poli.all()
        for item in chief:
            new_section.chief.add(item)
        for item in bureau:
            new_section.exec_chief_sub_bureau.add(item)
        for item in trans:
            new_section.exec_chief_trans.add(item)
        for item in arm_poli:
            new_section.exec_chief_armed_poli.add(item)
        return Response(response_data, status.HTTP_200_OK)
