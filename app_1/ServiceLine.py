# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from models import Road, District, ServiceLine
from constants import error_constants
from api_tools.api_tools import generate_error_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Serializers.serializers import StationSerializer, SingleStationSerializer, ServiceLineSerializer
from api_tools.token import SystemAuthentication


class ServiceLineView(APIView):
    authentication_classes = (SystemAuthentication,)

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            name = request.POST.get('name')
            start_place = request.POST.get('startPlace')
            end_place = request.POST.get('endPlace')
            time = request.POST.get('time')
            # 片区id组合起来德字符串，例如：'1-2-3-4-5'
            district_str = request.POST.get('districtStr', '')
            remark_1 = request.POST.get('remark1', '')
            remark_2 = request.POST.get('remark2', '')
            remark_3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_service_line = ServiceLine.objects.create(name=name, startPlace=start_place, endPlace=end_place,
                                                      time=time, remark1=remark_1, remark2=remark_2, remark3=remark_3)
        try:
            with transaction.atomic():
                cur_service_line.save()
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                           status.HTTP_500_INTERNAL_SERVER_ERROR)
        district_list = []
        if district_str:
            district_list = district_str.split('-')
        print(district_list)
        for item in district_list:
            cur_district = District.objects.get(id=int(item))
            cur_service_line.district.add(cur_district)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data': {}}
        try:
            district_id = int(request.GET.get('districtId', 0))
            service_line_id = int(request.GET.get('serviceLineId', 0))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        if service_line_id:
            cur_service_line = ServiceLine.objects.filter(id=service_line_id, enabled=True)
        elif district_id:
            cur_district = District.objects.get(id=district_id)
            cur_service_line = cur_district.District_Service.filter(enabled=True).order_by('-time')
        else:
            cur_service_line = ServiceLine.objects.filter(enabled=True).order_by('-time')
        response_data['data'] = ServiceLineSerializer(cur_service_line, many=True).data
        return Response(response_data, status.HTTP_200_OK)

    def put(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            select_districts_str = request.POST.get('selectDistrictsStr', '')
            service_line_id = int(request.POST.get('serviceLineId'))
            name = request.POST.get('name', '')
            start_place = request.POST.get('startPlace', '')
            end_place = request.POST.get('endPlace', '')
            time = request.POST.get('time', '')
            remark1 = request.POST.get('remark1', '')
            remark2 = request.POST.get('remark2', '')
            remark3 = request.POST.get('remark3', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_service_line = ServiceLine.objects.get(id=service_line_id)
        cur_service_line.name = name
        cur_service_line.startPlace = start_place
        cur_service_line.endPlace = end_place
        cur_service_line.time = time
        cur_service_line.remark1 = remark1
        cur_service_line.remark2 = remark2
        cur_service_line.remark3 = remark3
        cur_service_line.save()
        dis_list = []
        if select_districts_str:
            dis_list = select_districts_str.split('-')
        cur_service_line.district.clear()
        for item in dis_list:
            cur_dis = District.objects.get(id=int(item))
            cur_service_line.district.add(cur_dis)
        return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            service_line_id = int(request.data.get('serviceLineId'))
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_service_line = ServiceLine.objects.get(id=service_line_id)
        cur_service_line.enabled = False
        cur_service_line.save()
        return Response(response_data, status.HTTP_200_OK)

