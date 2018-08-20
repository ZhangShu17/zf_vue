# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from models import Road, Faculty, Section, Station
from constants import error_constants
from api_tools.api_tools import generate_error_response, update_faculty_channel_call_sign
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Serializers.serializers import StationSerializer, SingleStationSerializer, FacultySerializer
from api_tools.token import SystemAuthentication
from t.models import guard_road
from constants.constants import increment
from django.db.models import F


class StationView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            district_id = int(request.POST.get('districtId'))
            section_id = int(request.POST.get('sectionId', 0))
            name = request.POST.get('name')
            location = request.POST.get('location')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        if section_id:
            cur_station = Station.objects.create(name=name, location=location, section_id=section_id,
                                                 district_id=district_id, channel=channel, call_sign=call_sign,
                                                 remark1=remark_1,remark2=remark_2, remark3=remark_3)

            try:
                with transaction.atomic():
                    cur_station.save()
            except Exception as ex:
                print 'function name: ', __name__
                print Exception, ":", ex
                return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                               status.HTTP_500_INTERNAL_SERVER_ERROR)
            # 路的段/岗数量更新
            road_id = Section.objects.get(id=section_id).road_id
            if road_id:
                cur_guard_road = guard_road.objects.filter(uid=road_id + increment)
                cur_guard_road.update(stationnum=F('stationnum')+1)
        else:
            cur_station = Station.objects.create(name=name, location=location, channel=channel,
                                                 remark1=remark_1, district_id=district_id, call_sign=call_sign,
                                                 remark2=remark_2, remark3=remark_3)
            try:
                with transaction.atomic():
                    cur_station.save()
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
            section_id = int(request.GET.get('sectionId', 0))
            district_id = int(request.GET.get('districtId', 0))
            station_id = int(request.GET.get('stationId', 0))
            cur_per_page = int(request.GET.get('perPage', 20))
            page = int(request.GET.get('page', 1))
            section_name = ''
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        if station_id:
            cur_station = Station.objects.filter(enabled=1, id=station_id).order_by('-id')
        elif section_id:
            section_name = Section.objects.get(id=section_id).name
            cur_station = Station.objects.filter(enabled=1, section_id=section_id).order_by('-id')
        else:
            cur_station = Station.objects.filter(enabled=1).order_by('-id')
        if district_id:
            cur_station = cur_station.filter(district_id=district_id).order_by('-id')
        paginator = Paginator(cur_station, cur_per_page)
        page_count = paginator.num_pages

        try:
            station_lists = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            station_lists = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            station_lists = paginator.page(page)
        serializer = StationSerializer(station_lists, many=True)
        response_data['data'] = {}
        response_data['data']['sectionName'] = section_name
        response_data['data']['curPage'] = page
        response_data['data']['listCount'] = paginator.count
        response_data['data']['list'] = serializer.data
        response_data['data']['pageCount'] = page_count
        return Response(response_data, status.HTTP_200_OK)

    def put(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.POST.get('stationId'))
            name = request.POST.get('name', '')
            location = request.POST.get('location', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        if name:
            cur_station.name = name
        if location:
            cur_station.location=location
        if channel:
            cur_station.channel = channel
        if call_sign:
            cur_station.call_sign = call_sign
        if remark_1:
            cur_station.remark1 = remark_1
        if remark_2:
            cur_station.remark2 = remark_2
        if remark_3:
            cur_station.remark3 = remark_3
        cur_station.save()
        update_faculty_channel_call_sign(3, station_id)
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.data.get('stationId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        cur_station.enabled = False
        cur_station.save()

        # 路的段/岗数量更新
        section_id = cur_station.section_id
        if section_id:
            road_id = Section.objects.get(id=section_id).road_id
            if road_id:
                guard_road.objects.filter(uid=road_id+increment).update(stationnum=F('stationnum')-1)

        return Response(response_data, status.HTTP_200_OK)


# 岗哨人员信息
class StationFacultyView(APIView):
    authentication_classes = (SystemAuthentication,)

    # 添加人员信息
    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.POST.get('stationId'))
            # faculty_id = int(request.POST.get('facultyId'))
            name = request.POST.get('name', '')
            mobile = request.POST.get('mobile', '')
            duty = request.POST.get('duty', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            district_id = int(request.POST.get('districtId', 0))
            # faculty_type 1 岗长；3 执行岗长 交通
            faculty_type = int(request.POST.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        cur_faculty = Faculty.objects.filter(name=name, mobile=mobile)
        if cur_faculty.exists():
            cur_faculty.update(enabled=True)
            cur_faculty = cur_faculty.first()
        else:
            if faculty_type == 3:
                faculty_type = 2
            cur_faculty = Faculty.objects.create(name=name, mobile=mobile, duty=duty,
                                                 level=3, role=faculty_type, main_id=station_id,
                                                 district_id=district_id, channel=cur_station.channel,
                                                 call_sign=cur_station.call_sign)
            try:
                with transaction.atomic():
                    cur_faculty.save()
            except Exception as ex:
                print 'function name: ', __name__
                print Exception, ":", ex
                return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                               status.HTTP_500_INTERNAL_SERVER_ERROR)
        if faculty_type == 1:
            cur_station.chief.add(cur_faculty)
        if faculty_type == 3:
            cur_station.exec_chief_trans.add(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.GET.get('stationId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        serializer = SingleStationSerializer(cur_station)
        response_data['data'] = serializer.data
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.GET.get('stationId'))
            faculty_id = int(request.GET.get('facultyId'))
            # faculty_type 1 路长；2 执行路长 交通
            faculty_type = int(request.GET.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        if faculty_type == 1:
            cur_station.chief.remove(cur_faculty)
        if faculty_type == 2:
            cur_station.exec_chief_trans.remove(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)


# 删除岗哨人员
class DeleteStationFacultyView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self,request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.GET.get('stationId'))
            faculty_id = int(request.GET.get('facultyId'))
            # faculty_type 1 路长；2 执行路长 分局；3： 执行路长 交通；4：执行路长 武警
            faculty_type = int(request.GET.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        if faculty_type == 1:
            cur_station.chief.remove(cur_faculty)
        if faculty_type == 3:
            cur_station.exec_chief_trans.remove(cur_faculty)
        cur_faculty.channel = ''
        cur_faculty.call_sign = ''
        cur_faculty.save()
        return Response(response_data, status.HTTP_200_OK)


class StationNotInToSectionView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'dataList': []}
        try:
            section_id = int(request.GET.get('sectionId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_section = Section.objects.get(id=section_id)
        # 当前路段district_id
        cur_section_district_id = cur_section.district_id
        # 当前路段岗位id
        cur_section_station_id_lists = cur_section.Section_Station.all().values_list('id', flat=True)

        cur_station_list = Station.objects.filter(enabled=True, district_id=cur_section_district_id,
                                                  section_id__isnull=True).exclude(id__in=cur_section_station_id_lists)
        response_data['dataList'] = StationSerializer(cur_station_list, many=True).data
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.POST.get('sectionId'))
            station_id = int(request.POST.get('stationId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        print(section_id)
        print(station_id)
        cur_station = Station.objects.get(id=station_id)
        cur_station.section_id = section_id
        cur_station.save()

        # 路的段/岗数量更新
        road_id = Section.objects.get(id=section_id).road_id
        if road_id:
            guard_road.objects.filter(uid=road_id + increment).update(stationnum=F('stationnum') + 1)

        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            section_id = int(request.POST.get('sectionId'))
            station_id = int(request.POST.get('stationId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        cur_station.section_id = None
        try:
            with transaction.atomic():
                cur_station.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                           status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 路的段/岗数量更新
        road_id = Section.objects.get(id=section_id).road_id
        if road_id:
            guard_road.objects.filter(uid=road_id + increment).update(stationnum=F('stationnum') - 1)

        return Response(response_data, status.HTTP_200_OK)


class FacultyNotInStation(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data':{
                             'chiefList': [],
                             'execChiefTransList': []}
                         }
        try:
            station_id = int(request.GET.get('stationId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        district_id = cur_station.district_id
        chief_list = cur_station.chief.all().values_list('id', flat=True)
        trans_list = cur_station.exec_chief_trans.all().values_list('id', flat=True)
        cur_chief_list = Faculty.objects.filter(enabled=True, district_id=district_id,
                                                level=3, role=1, main_id=station_id).\
            exclude(id__in=chief_list).order_by('id')
        cur_trans_list = Faculty.objects.filter(enabled=True, district_id=district_id,
                                                level=3, role=2, main_id=station_id).\
            exclude(id__in=trans_list).order_by('id')
        response_data['data']['chiefList'] = FacultySerializer(cur_chief_list, many=True).data
        response_data['data']['execChiefTransList'] = FacultySerializer(cur_trans_list, many=True).data
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.POST.get('stationId'))
            faculty_id = int(request.POST.get('facultyId'))
            faculty_type = int(request.POST.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        if faculty_type == 1:
            cur_station.chief.add(cur_faculty)
        if faculty_type == 3:
            cur_station.exec_chief_trans.add(cur_faculty)
        channel = cur_station.channel
        call_sign = cur_station.call_sign
        cur_faculty.channel = channel
        cur_faculty.call_sign = call_sign
        cur_faculty.save()
        return Response(response_data, status.HTTP_200_OK)


class CopyStationView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            station_id = int(request.POST.get('stationId'))
            name = request.POST.get('name')
            location = request.POST.get('location')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_station = Station.objects.get(id=station_id)
        district_id = cur_station.district_id
        section_id = cur_station.section_id
        new_station = Station.objects.create(name=name, location=location, channel=channel,
                                             remark1=remark_1, call_sign=call_sign, remark2=remark_2,
                                             remark3=remark_3, district_id=district_id)
        try:
            with transaction.atomic():
                new_station.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                           status.HTTP_500_INTERNAL_SERVER_ERROR)
        chief = cur_station.chief.all()
        trans = cur_station.exec_chief_trans.all()
        for item in chief:
            new_station.chief.add(item)
        for item in trans:
            new_station.exec_chief_trans.add(item)

        # 路的段/岗数量更新
        if section_id:
            road_id = Section.objects.get(id=section_id).road_id
            if road_id:
                cur_guard_road = guard_road.objects.filter(uid=road_id + increment)
                cur_guard_road.update(sectionnum=F('stationnum') + 1)
        return Response(response_data, status.HTTP_200_OK)