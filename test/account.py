# -*- coding: utf-8 -*-

import hashlib
# 初始账号和密码
account = [
    {'user_name': 'user0001', 'pass_word': 'zf_7905'},
    {'user_name': 'user0002', 'pass_word': 'zf_5891'},
    {'user_name': 'user0003', 'pass_word': 'zf_7752'},
    {'user_name': 'user0004', 'pass_word': 'zf_8868'},
    {'user_name': 'user0005', 'pass_word': 'zf_1169'},
    {'user_name': 'user0006', 'pass_word': 'zf_1679'},
    {'user_name': 'user0007', 'pass_word': 'zf_0904'},
    {'user_name': 'user0008', 'pass_word': 'zf_9210'},
    {'user_name': 'user0009', 'pass_word': 'zf_4093'},
    {'user_name': 'user0010', 'pass_word': 'zf_9649'},
]

for item in account:
    user_name = item.get('user_name')
    pass_word = item.get('pass_word')
    password_md5 = hashlib.md5(pass_word).hexdigest()
    print(password_md5)
# {
#     'retcode': '',
#     'retmsg': '',
#     'data':{
#         'id':'',
#         'name':'',
#         'length': '',
#         'section_station_num': '',
#         'chief': [
#             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#         ],
#         'exec_chief_sub_bureau': [
#                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                 ],
#         'exec_chief_trans': [
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                         ],
#         'exec_chief_armed_poli': [
#                                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                 ],
#         'sectionList':[
#             {
#                 'id': '',
#                 'name': '',
#                 'chief': [
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                         ],
#                 'exec_chief_sub_bureau': [
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                         ],
#                 'exec_chief_trans': [
#                                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                 ],
#                 'exec_chief_armed_poli': [
#                                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                         ],
#                 'stationList': [
#                     {'id': '',
#                      'name': '',
#                      'chief': [
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                             {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                      ],
#                     'exec_chief_trans': [
#                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                     ],
#                      }
#                 ]
#             },
#             {
#                             'id': '',
#                             'name': '',
#                             'chief': [
#                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                     ],
#                             'exec_chief_sub_bureau': [
#                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                     ],
#                             'exec_chief_trans': [
#                                                 {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                                 {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                             ],
#                             'exec_chief_armed_poli': [
#                                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                                     ],
#                             'stationList': [
#                                 {'id': '',
#                                  'name': '',
#                                  'chief': [
#                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                         {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                  ],
#                                 'exec_chief_trans': [
#                                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                     {'id':'', 'name': '', 'mobile': '', 'duty':'', 'channel': '', 'callSign': ''},
#                                 ],
#                                  }
#                             ]
#                         },
#         ]
#     }
# }