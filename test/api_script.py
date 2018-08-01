# -*- coding: utf-8 -*-

import requests
import json

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
    'roadId': 2,
}

headers = {
    'authorization': token
}
r = requests.delete('http://127.0.0.1:8000/road/edit', params=data, headers=headers)
print(r.text)
