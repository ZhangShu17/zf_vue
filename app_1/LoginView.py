# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from models import Account
from constants import error_constants
from api_tools.api_tools import generate_error_response
from api_tools.token import create_token
import hashlib


class LoginView(APIView):
    # 登陆
    def post(self, request):
        print(request.POST)
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data': {
                             'userName': '',
                             'token': ''
                         }}
        try:
            user_name = request.POST.get('userName', '')
            password = request.POST.get('password', '')
        except Exception as ex:
            print 'function name: ', __name__
            print Exception, ":", ex
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        print(user_name)
        print(password)
        cur_account = Account.objects.filter(name=user_name).first()
        if not cur_account:
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)
        if hashlib.md5(password).hexdigest() != cur_account.password:
            return generate_error_response(error_constants.ERR_INVALID_ACCOUNT, status.HTTP_400_BAD_REQUEST)
        token = create_token(user_name)
        response_data['data']['userName'] = user_name
        response_data['data']['token'] = token
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