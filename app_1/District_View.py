# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from models import District
from constants import error_constants
from Serializers.serializers import DistrictSerializer
from api_tools.token import SystemAuthentication


class DistrictView(APIView):
    authentication_classes = (SystemAuthentication,)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'districtList': []}
        district_list = District.objects.all()
        serializer = DistrictSerializer(district_list, many=True)
        response_data['districtList'] = serializer.data
        return Response(response_data, status.HTTP_200_OK)

