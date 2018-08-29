# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from models import Account, District
from constants import error_constants
from api_tools.api_tools import generate_error_response
from api_tools.token import create_token
from constants.constants import account, district
import hashlib


# 创建用户名和密码
class CreateAccountView(APIView):
    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        for item in account:
            user_name = item.get('user_name')
            pass_word = item.get('pass_word')
            district_id = item.get('district_id')
            password_md5 = hashlib.md5(pass_word).hexdigest()
            if not Account.objects.filter(name=user_name).exists():
                cur_account = Account(name=user_name, password=password_md5, district_id=district_id)
                try:
                    with transaction.atomic():
                        cur_account.save()
                except Exception as ex:
                    print 'function name: ', __name__
                    print Exception, ":", ex
                    return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                                   status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response_data, status.HTTP_200_OK)


class CreateDistrictView(APIView):
    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        for item in district:
            code = item.get('code')
            name = item.get('name')
            if not District.objects.filter(name=name, code=code).exists():
                cur_district = District(name=name, code=code)
                try:
                    with transaction.atomic():
                        cur_district.save()
                except Exception as ex:
                    print 'function name: ', __name__
                    print Exception, ":", ex
                    return generate_error_response(error_constants.ERR_SAVE_INFO_FAIL,
                                                   status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response_data, status.HTTP_200_OK)


class LoginView(APIView):
    # 登陆
    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data': {
                             'userName': '',
                             'token': '',
                         }}
        try:
            user_name = request.POST.get('userName', '')
            password = request.POST.get('password', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        pass_word_hash = hashlib.md5(password).hexdigest()
        cur_account = Account.objects.filter(name=user_name, password=pass_word_hash).first()
        if not cur_account:
            return generate_error_response(error_constants.ERR_INVALID_ACCOUNT, status.HTTP_400_BAD_REQUEST)
        token = create_token(user_name)
        response_data['data']['userName'] = user_name
        response_data['data']['token'] = token
        response_data['data']['districtId'] = cur_account.district_id
        return Response(response_data, status.HTTP_200_OK)

    # 修改账户密码
    def put(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                        }
        try:
            user_name = request.POST.get('userName')
            old_password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        cur_account = Account.objects.filter(name=user_name)
        if cur_account.first().password != hashlib.md5(old_password).hexdigest():
            return generate_error_response(error_constants.ERR_INVALID_ACCOUNT, status.HTTP_400_BAD_REQUEST)
        if old_password == new_password:
            return generate_error_response(error_constants.ERR_INVALID_NEW_PASSWORD, status.HTTP_400_BAD_REQUEST)
        cur_account.update(password=hashlib.md5(new_password).hexdigest())
        return Response(response_data, status.HTTP_200_OK)