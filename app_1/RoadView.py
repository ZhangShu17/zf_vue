# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from models import Road, Faculty, ServiceLine
from constants import error_constants
from api_tools.api_tools import generate_error_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Serializers.serializers import RoadSerializer, SingleRoadSerializer, RoadExcelSerializer
from django.db.models import Q
from api_tools.token import SystemAuthentication


class RoadView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            service_line_id = int(request.POST.get('serviceLineId', 0))
            district_id = int(request.POST.get('districtId'))
            name = request.POST.get('name')
            length = request.POST.get('length', '')
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
        cur_road = Road.objects.create(name=name, length=length, start_place=start_place,
                                       end_place=end_place, start_point=start_point,
                                       end_point=end_point, remark1=remark_1, remark2=remark_2,
                                       remark3=remark_3, district_id=district_id)
        try:
            with transaction.atomic():
                cur_road.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                           status.HTTP_500_INTERNAL_SERVER_ERROR)
        print('service_line_id', service_line_id)
        if service_line_id:
            cur_service_line = ServiceLine.objects.get(id=service_line_id)
            cur_service_line.road.add(cur_road)
        return Response(response_data, status=status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            service_line_id = int(request.GET.get('serviceLineId', 0))
            district_id = int(request.GET.get('districtId', 0))
            cur_per_page = int(request.GET.get('perPage', 20))
            page = int(request.GET.get('page', 1))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        if service_line_id:
            cur_service_line = ServiceLine.objects.get(id=service_line_id)
            cur_road = cur_service_line.road.filter(enabled=True).order_by('id')
        else:
            cur_road = Road.objects.filter(enabled=True).order_by('id')
        if district_id:
            cur_road = cur_road.filter(district_id=district_id)
        paginator = Paginator(cur_road, cur_per_page)
        page_count = paginator.num_pages

        try:
            road_lists = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            road_lists = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            road_lists = paginator.page(page)
        serializer = RoadSerializer(road_lists, many=True)
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
            road_id = int(request.POST.get('roadId'))
            name = request.POST.get('name', '')
            length = request.POST.get('length', '')
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
        cur_road = Road.objects.filter(id=road_id)
        if name:
            cur_road.update(name=name)
        if length:
            cur_road.update(length=length)
        if start_place:
            cur_road.update(start_place=start_place)
        if end_place:
            cur_road.update(end_place=end_place)
        if start_point and end_point:
            if cur_road.first().start_point != start_point or cur_road.first().end_point != end_point:
                cur_road.update(start_point=start_point, end_point=end_point)
        if remark_1:
            cur_road.update(remark1=remark_1)
        if remark_2:
            cur_road.update(remark1=remark_2)
        if remark_3:
            cur_road.update(remark1=remark_3)
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.GET.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        Road.objects.filter(id=road_id).update(enabled=False)
        return Response(response_data, status.HTTP_200_OK)


# 获取单条道路信息
class SingleRoadInfoView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.GET.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_road = Road.objects.get(id=road_id)
        serializer = RoadSerializer(cur_road)
        response_data['data'] = serializer.data
        return Response(response_data, status.HTTP_200_OK)


# 获取该条道路人员信息
class RoadFacultyView(APIView):
    authentication_classes = (SystemAuthentication,)

    # 添加人员信息
    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        print(request.POST)
        try:
            road_id = int(request.POST.get('roadId'))
            # faculty_id = int(request.POST.get('facultyId'))
            name = request.POST.get('name', '')
            mobile = request.POST.get('mobile', '')
            duty = request.POST.get('duty', '')
            channel = request.POST.get('channel', '')
            call_sign = request.POST.get('callSign', '')
            # faculty_type 1 路长；2 执行路长 分局；3： 执行路长 交通；4：执行路长 武警
            faculty_type = int(request.POST.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_road = Road.objects.get(id=road_id)
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
            cur_road.chief.add(cur_faculty)
        if faculty_type == 2:
            cur_road.exec_chief_sub_bureau.add(cur_faculty)
        if faculty_type == 3:
            cur_road.exec_chief_trans.add(cur_faculty)
        if faculty_type == 4:
            cur_road.exec_chief_armed_poli.add(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.GET.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        print(road_id)
        cur_road = Road.objects.get(id=road_id)
        serializer = SingleRoadSerializer(cur_road)
        response_data['data'] = serializer.data
        return Response(response_data, status.HTTP_200_OK)

    # def delete(self, request):
    #     response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
    #                      'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
    #     try:
    #         road_id = int(request.GET.get('roadId'))
    #         faculty_id = int(request.GET.get('facultyId'))
    #         # faculty_type 1 路长；2 执行路长 分局；3： 执行路长 交通；4：执行路长 武警
    #         faculty_type = int(request.GET.get('facultyType'))
    #     except Exception as ex:
    #         print 'function name: ', __name__
    #         print Exception, ":", ex
    #         return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
    #     cur_road = Road.objects.get(id=road_id)
    #     cur_faculty = Faculty.objects.get(id=faculty_id)
    #     if faculty_type == 1:
    #         cur_road.chief.remove(cur_faculty)
    #     if faculty_type == 2:
    #         cur_road.exec_chief_sub_bureau.remove(cur_faculty)
    #     if faculty_type == 3:
    #         cur_road.exec_chief_trans.remove(cur_faculty)
    #     if faculty_type == 4:
    #         cur_road.exec_chief_armed_poli.remove(cur_faculty)
    #     return Response(response_data, status.HTTP_200_OK)


class DeleteRoadFaculty(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.GET.get('roadId'))
            faculty_id = int(request.GET.get('facultyId'))
            # faculty_type 1 路长；2 执行路长 分局；3： 执行路长 交通；4：执行路长 武警
            faculty_type = int(request.GET.get('facultyType'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_road = Road.objects.get(id=road_id)
        cur_faculty = Faculty.objects.get(id=faculty_id)
        if faculty_type == 1:
            cur_road.chief.remove(cur_faculty)
        if faculty_type == 2:
            cur_road.exec_chief_sub_bureau.remove(cur_faculty)
        if faculty_type == 3:
            cur_road.exec_chief_trans.remove(cur_faculty)
        if faculty_type == 4:
            cur_road.exec_chief_armed_poli.remove(cur_faculty)
        return Response(response_data, status.HTTP_200_OK)


class DeleteRoadView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self,request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            road_id = int(request.GET.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        Road.objects.filter(id=road_id).update(enabled=False)
        return Response(response_data, status.HTTP_200_OK)


class RoadExcelView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data': {}}
        try:
            road_id = int(request.GET.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_road = Road.objects.get(id=road_id)
        response_data['data'] = RoadExcelSerializer(cur_road).data
        return Response(response_data, status.HTTP_200_OK)


class RoadNotInToServiceLineView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'dataList': []}
        try:
            service_line_id = int(request.GET.get('serviceLineId'))
            district_id = int(request.GET.get('districtId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        # 当前勤务路线的地区id
        service_line_district_list = ServiceLine.objects.get(id=service_line_id).\
            district.all().values_list('id', flat=True)
        # 当前勤务路线的路线road
        service_line_road_list = ServiceLine.objects.get(id=service_line_id).\
            road.all().values_list('id', flat=True)

        query1 = Q()

        temp1 = Q()
        temp1.connector = 'AND'
        temp1.children.append(('enabled', True))
        if district_id:
            temp1.children.append(('district_id', district_id))
        query1.add(temp1, 'AND')

        temp2 = Q()
        temp2.connector = 'AND'
        temp2.children.append(('district_id__in', service_line_district_list))
        query1.add(temp2, 'AND')

        query2 = Q()
        query2.connector = 'AND'
        query2.children.append(('id__in', service_line_road_list))

        road_list = Road.objects.filter(query1).exclude(query2).order_by('id')
        serializer = RoadSerializer(road_list, many=True)
        response_data['dataList'] = serializer.data
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            service_line_id = int(request.POST.get('serviceLineId'))
            road_id = int(request.POST.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_service_line = ServiceLine.objects.get(id=service_line_id)
        cur_road = Road.objects.get(id=road_id)
        cur_service_line.road.add(cur_road)
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        print('here')
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            service_line_id = int(request.data.get('serviceLineId'))
            road_id = int(request.data.get('roadId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_service_line = ServiceLine.objects.get(id=service_line_id)
        cur_road = Road.objects.get(id=road_id)
        cur_service_line.road.remove(cur_road)
        return Response(response_data, status.HTTP_200_OK)