# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
import tokenlib


def generate_error_response(error_message, error_type):
    return Response({'retCode': error_message[0],
                     'retMsg': error_message[1]}, error_type)