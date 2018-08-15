# -*- coding: utf-8 -*-

# import cx_Oracle
#
#
# conn = cx_Oracle.connect('icp_zf', 'icp_zf', '192.168.8.111:1521/orcl')
# curs = conn.cursor()
# print('连接成功')

def func1(x):
    if x<5:
        return
    print('yes')
func1(6)