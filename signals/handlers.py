# -*- coding: utf-8 -*-

from app_1.models import Faculty, ServiceLine, Station, Section
from django.db.models import signals
from django.dispatch import receiver
from constants.constants import increment
from api_tools.api_tools import is_already_in_use
import cx_Oracle

# db = cx_Oracle.connect('icp_zf', 'icp_zf', '192.168.8.111:1521/orcl')
# cursor = db.cursor()
#
#
# @receiver(signals.post_save, sender=Faculty)
# def create_update_faculty(sender, instance, created, **kwargs):
#     if created:
#         param = {
#             'ID': instance.id,
#             'USERNAME': instance.name,
#             'PHONE': instance.mobile,
#             'RADIO_STATION ': instance.channel,
#             'CALL': instance.call_sign,
#             'DUTIES': instance.duty
#         }
#         sql_exe = 'insert into T_GUARD_ADMIN (ID, USERNAME, PHONE, RADIO_STATION, CALL, DUTIES) ' \
#                   'values(%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' \
#                   % (param['ID']+increment, param['USERNAME'], param['PHONE'],
#                      param['RADIO_STATION '], param['CALL'], param['DUTIES'])
#         cursor.execute(sql_exe)
#         db.commit()
#     else:
#         param = {
#             'ID': instance.id,
#             'USERNAME': instance.name,
#             'PHONE': instance.mobile,
#             'RADIO_STATION ': instance.channel,
#             'CALL': instance.call_sign,
#             'DUTIES': instance.duty,
#             'ENABLED': str(int(instance.enabled))
#         }
#         sql_exe = 'update T_GUARD_ADMIN set USERNAME=\'%s\', PHONE=\'%s\', RADIO_STATION=\'%s\', CALL=\'%s\', ' \
#                   'DUTIES=\'%s\', ENABLED=\'%s\' WHERE ID=\'%d\'' % (param['USERNAME'], param['PHONE'],
#                                                                      param['RADIO_STATION '], param['CALL'], param['DUTIES'],
#                                                                      param['ENABLED'], param['ID']+increment)
#         cursor.execute(sql_exe)
#         db.commit()
#
#
# @receiver(signals.post_save, sender=Station)
# def create_update_station(sender, instance, created, **kwargs):
#     if created:
#         param = {
#             'id': instance.id,
#             'name': instance.name,
#             'location': instance.location,
#             'section_id': instance.section_id,
#             'remark1': instance.remark1,
#             'remark2': instance.remark1,
#             'remark3': instance.remark1,
#         }
#         print(param)
#         if param['section_id']:
#             sql_exe = 'insert into T_GUARD_STATION (ID, STATION_NAME, XYCOORDINATE, SECTIONID, REMARK1, REMARK2, REMARK3) ' \
#                       'values(%d, \'%s\', \'%s\', \'%d\', \'%s\', \'%s\', \'%s\')' \
#                       % (param['id'] + increment, param['name'], param['location'],
#                          param['section_id'] + increment, param['remark1'], param['remark2'], param['remark3'])
#         else:
#             sql_exe = 'insert into T_GUARD_STATION (ID, STATION_NAME, XYCOORDINATE, REMARK1, REMARK2, REMARK3) ' \
#                       'values(%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' \
#                       % (param['id'] + increment, param['name'], param['location'], param['remark1'],
#                          param['remark2'], param['remark3'])
#         print(sql_exe)
#         cursor.execute(sql_exe)
#         db.commit()
#     else:
#         print('update')
#         param = {
#             'id': instance.id,
#             'name': instance.name,
#             'location': instance.location,
#             'section_id': instance.section_id,
#             'enabled': str(int(instance.enabled)),
#             'remark1': instance.remark1,
#             'remark2': instance.remark1,
#             'remark3': instance.remark1,
#         }
#         print(param)
#         if param['section_id']:
#             sql_exe = 'update T_GUARD_STATION set STATION_NAME=\'%s\', XYCOORDINATE=\'%s\', SECTIONID=\'%d\', ENABLED=\'%s\', ' \
#                       'REMARK1=\'%s\', REMARK2=\'%s\', REMARK3=\'%s\' WHERE ID=\'%d\'' \
#                       % (param['name'], param['location'], param['section_id'] + increment,
#                          param['enabled'], param['remark1'], param['remark2'],
#                          param['remark3'], param['id']+increment)
#         else:
#             sql_exe = 'update T_GUARD_STATION set STATION_NAME=\'%s\', XYCOORDINATE=\'%s\', ENABLED=\'%s\', ' \
#                       'REMARK1=\'%s\', REMARK2=\'%s\', REMARK3=\'%s\' WHERE ID=\'%d\'' \
#                       % (param['name'], param['location'], param['enabled'], param['remark1'],
#                          param['remark2'], param['remark3'], param['id'] + increment)
#         cursor.execute(sql_exe)
#         db.commit()
#
#
# def station_chief_change(sender, instance, model, action, pk_set, **kwargs):
#     faculty_type = str(sender).split('\'')[1].split('.')[-1].split('_')[-1]
#     if action == 'post_add':
#         print('post_add')
#         for item in pk_set:
#             if faculty_type == 'chief':
#                 print('chief')
#                 duty_name = u'岗长(分局)'
#                 order_list = 1
#             else:
#                 print('execu_chief')
#                 duty_name = u'执行岗长(交管)'
#                 order_list = 2
#             count = is_already_in_use(item)
#             # 无其他职位
#             if not count:
#                 print('no other')
#                 param = {
#                     'ID': item,
#                     'DUTYNAME': duty_name,
#                     'CATEGORY': str(3),
#                     'ORDERLIST': order_list,
#                     'MAINID': instance.id + increment
#                 }
#                 sql_exe = 'update T_GUARD_ADMIN set DUTYNAME=\'%s\', CATEGORY=\'%s\', ORDERLIST=\'%s\', ' \
#                           'MAINID=\'%s\' WHERE ID=\'%d\'' \
#                           % (param['DUTYNAME'], param['CATEGORY'], param['ORDERLIST'], param['MAINID'],
#                              param['ID'] + increment)
#             # 有其他职位
#             else:
#                 print('exists')
#                 cur_faculty = Faculty.objects.get(id=item)
#                 param = {
#                     'ID': item,
#                     'DUTYNAME': duty_name,
#                     'CATEGORY': str(3),
#                     'ORDERLIST': order_list,
#                     'MAINID': instance.id + increment,
#                     'USERNAME': cur_faculty.name,
#                     'PHONE': cur_faculty.mobile,
#                     'RADIO_STATION ': cur_faculty.channel,
#                     'CALL': cur_faculty.call_sign,
#                     'DUTIES': cur_faculty.duty
#                 }
#                 sql_exe = 'insert into T_GUARD_ADMIN (DUTYNAME, CATEGORY, ORDERLIST, MAINID, ID, USERNAME, PHONE, ' \
#                           'RADIO_STATION, CALL, DUTIES) ' \
#                           'values(\'%s\', \'%s\', \'%s\', %d, %d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' \
#                           % (param['DUTYNAME'], param['CATEGORY'], param['ORDERLIST'], param['MAINID'],
#                              param['ID'] + increment, param['USERNAME'], param['PHONE'],
#                              param['RADIO_STATION '], param['CALL'], param['DUTIES'])
#             cursor.execute(sql_exe)
#             db.commit()
#     if action == 'post_remove':
#         print('post_remove')
#         for item in pk_set:
#             count = is_already_in_use(item)
#             # 只有本职位
#             if count < 2:
#                 param = {
#                     'ID': item,
#                 }
#                 sql_exe = 'update T_GUARD_ADMIN set DUTYNAME=null, CATEGORY=null, ' \
#                           'ORDERLIST=null, MAINID=null WHERE ID=\'%d\'' % (param['ID'] + increment,)
#             else:
#                 if faculty_type == 'chief':
#                     print('chief')
#                     duty_name = u'岗长(分局)'
#                     order_list = 1
#                 else:
#                     print('execu_chief')
#                     duty_name = u'执行岗长(交管)'
#                     order_list = 2
#                 param = {
#                     'ID': item,
#                     'DUTYNAME': duty_name,
#                     'CATEGORY': str(3),
#                     'ORDERLIST': order_list,
#                     'MAINID': instance.id + increment
#                 }
#                 sql_exe = 'update T_GUARD_ADMIN set DUTYNAME=null, CATEGORY=null, ' \
#                           'ORDERLIST=null, MAINID=null WHERE ID=\'%d\', DUTYNAME=\'%s\', MAINID=\'%d\'' \
#                           % (param['ID'] + increment, param['DUTYNAME'], param['MAINID'])
#             cursor.execute(sql_exe)
#             db.commit()
#
#
# signals.m2m_changed.connect(station_chief_change, sender=Station.chief.through)
# signals.m2m_changed.connect(station_chief_change, sender=Station.exec_chief_trans.through)


@receiver(signals.post_save, sender=Section)
def create_update_section(sender, instance, created, **kwargs):
    if created:
        param = {
            'id': instance.id,
            'name': instance.name,
            'start_place': instance.mobile,
            'end_place': instance.channel,
            'xy_coordinate': instance.call_sign,
            'DUTIES': instance.duty
        }


