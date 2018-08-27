# coding=utf-8

import re
# 有效期12小时
expire_time = 12*60*60
SECRET_KEY = 'hqvsokks@#1)JJs'

increment = 10000
pattern = re.compile(r'\d+\.\d+')



account = [
    {'user_name': 'tam', 'pass_word': 'zf_7905', 'district_id': 1},
    {'user_name': 'dc', 'pass_word': 'zf_5891', 'district_id': 2},
    {'user_name': 'xc', 'pass_word': 'zf_7752', 'district_id': 3},
    {'user_name': 'cy', 'pass_word': 'zf_8868', 'district_id': 4},
    {'user_name': 'hd', 'pass_word': 'zf_1169', 'district_id': 5},
    {'user_name': 'ft', 'pass_word': 'zf_1679', 'district_id': 6},
    {'user_name': 'sjs', 'pass_word': 'zf_0904', 'district_id': 7},
    {'user_name': 'xz', 'pass_word': 'zf_9210', 'district_id': 8},
    {'user_name': 'sy', 'pass_word': 'zf_4093', 'district_id': 9},
    {'user_name': 'jwj', 'pass_word': 'zf_9649', 'district_id': 0},
]

district = [
    {'code': '0001', 'name': '天安门'},
    {'code': '0002', 'name': '东城区'},
    {'code': '0003', 'name': '西城区'},
    {'code': '0004', 'name': '朝阳区'},
    {'code': '0005', 'name': '海淀区'},
    {'code': '0006', 'name': '丰台区'},
    {'code': '0007', 'name': '石景山'},
    {'code': '0008', 'name': '西站区'},
    {'code': '0009', 'name': '顺义区'},
]