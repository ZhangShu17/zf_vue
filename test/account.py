# -*- coding: utf-8 -*-

import hashlib
# 初始账号和密码
account = [
    {'user_name': 'tam', 'pass_word': 'zf_7905'},
    {'user_name': 'dc', 'pass_word': 'zf_5891'},
    {'user_name': 'xc', 'pass_word': 'zf_7752'},
    {'user_name': 'cy', 'pass_word': 'zf_8868'},
    {'user_name': 'hd', 'pass_word': 'zf_1169'},
    {'user_name': 'ft', 'pass_word': 'zf_1679'},
    {'user_name': 'sjs', 'pass_word': 'zf_0904'},
    {'user_name': 'xz', 'pass_word': 'zf_9210'},
    {'user_name': 'sy', 'pass_word': 'zf_4093'},
    {'user_name': 'jwj', 'pass_word': 'zf_9649'},
]

a = None
if a:
    print'yes'
if not a:
    print 'no'

b = ' '
if not b:
    print('space')

newPoints = []
tempPoint = []
originPoints = [1,2,3,4,5,6,7,8,9,10,11,12]
for i in range(0,len(originPoints),2):
    newPoints.append(originPoints[i:i+2])
print newPoints
# change order
for i in range(0,len(newPoints)/2,1):
    tempPoint = newPoints[i]
    newPoints[i] = newPoints[len(newPoints)-1-i]
    newPoints[len(newPoints) - 1 - i] = tempPoint
print newPoints
