# -*- coding: utf-8 -*-

import tokenlib
import time
from rest_framework import authentication
from rest_framework import exceptions
from django.utils import timezone
from constants import constants
from constants import error_constants


token_manager = tokenlib.TokenManager(secret=constants.SECRET_KEY, timeout=constants.expire_time)


def create_token(user_name):
    data = {'user_name': user_name}
    token = token_manager.make_token(data)
    return token


class SystemAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            req_token = request.META['HTTP_AUTHORIZATION']
        except:
            raise exceptions.AuthenticationFailed(error_constants.ERR_TOKEN_ERROR)
        # 判断 get 还是 post
        if request.method == 'POST':
            user_name = request.POST.get('userName', '0')
        elif request.method == 'PUT':
            user_name = request.POST.get('userName', '0')
        elif request.method == 'DELETE':
            user_name = request.GET.get('userName', '0')
        elif request.method == 'GET':
            user_name = request.GET.get('userName', '0')
        else:
            user_name = request.query_params.get('userName', '0')
            req_token = request.query_params.get('token', '0')
        # 验证token
        try:
            # 当前时间
            token_now = time.mktime(timezone.now().timetuple())
            # 获取当前token
            current_parsed_token = token_manager.parse_token(str(req_token), now=token_now)
            if current_parsed_token['user_name'] != user_name:
                raise exceptions.AuthenticationFailed(error_constants.ERR_TOKEN_ERROR)
        except ValueError:
            raise exceptions.AuthenticationFailed(error_constants.ERR_TOKEN_EXPIRED)
        return current_parsed_token, None