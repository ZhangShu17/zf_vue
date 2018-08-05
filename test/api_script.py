# -*- coding: utf-8 -*-

import requests
import json
# r = requests.post('http://127.0.0.1:8000/account/create')
# print(r.text)

# 登陆信息
url = 'http://127.0.0.1:8000/'
data = {
    'userName': 'user0010',
    'password': 'zf_9649'
}
r = requests.post('http://127.0.0.1:8000/faculty/login', data=data)
json_data = json.loads(r.text)
print(json_data)
print(type(json_data))
user_name = json_data['data']['userName']
token = json_data['data']['token']
print(user_name)
print(token)
print(r.text)

data = {
    'userName': user_name,
    # 'districtId': 1,
    'districtId': 2,
    'name': '勤务路线1',
    'startPlace': '正阳门',
    'endPlace': '中华门',
    'districtStr': '1-2-3-4-5',
    'remark1': '威严',
    'time': '2018-06-07'
}

headers = {
    'authorization': token
}
r = requests.get('http://127.0.0.1:8000/server_line/edit', params=data, headers=headers)
print(r.text)
