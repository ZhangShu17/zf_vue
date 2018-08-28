import django
from app_1.models import Faculty, Station, Section, Road
from t.models import guard_admin
from constants.constants import increment

for item in Faculty.objects.all():
    guard_admin.objects.create(uid=item.id+increment, duties=item.duty, username=item.name,
                               phone=item.mobile, enabled=str(int(item.enabled)))


for station in Station.objects.all():
    for chief in station.chief.all():
        if guard_admin.objects.filter(uid=chief.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=chief.id+increment).update(dutyname=u'岗长(分局)', radio_station=station.channel,
                                                                      call=station.call_sign, category=3, orderlist=1,
                                                                      mainid=station.id+increment)
        else:
            guard_admin.objects.create(uid=chief.id+increment, duties=chief.duty, username=chief.name,
                                       phone=chief.mobile, enabled=str(int(chief.enabled)), dutyname=u'岗长(分局)',
                                       radio_station=station.channel, call=station.call_sign, category=3,
                                       orderlist=1, mainid=station.id+increment)
    for chief in station.exec_chief_trans.all():
        if guard_admin.objects.filter(uid=chief.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=chief.id+increment).update(dutyname=u'执行岗长(交管)', radio_station=station.channel,
                                                                      call=station.call_sign, category=3, orderlist=2,
                                                                      mainid=station.id+increment)
        else:
            guard_admin.objects.create(uid=chief.id+increment, duties=chief.duty, username=chief.name,
                                       phone=chief.mobile, enabled=str(int(chief.enabled)), dutyname=u'执行岗长(交管)',
                                       radio_station=station.channel, call=station.call_sign, category=3,
                                       orderlist=2, mainid=station.id+increment)

for section in Section.objects.all():
    for faculty in section.chief.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'段长', radio_station=section.channel,
                                                                      call=section.call_sign, category=2, orderlist=1,
                                                                      mainid=section.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'段长',
                                       radio_station=section.channel, call=section.call_sign, category=2,
                                       orderlist=1, mainid=section.id+increment)
    for faculty in section.exec_chief_sub_bureau.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'执行段长(分局)', radio_station=section.channel,
                                                                      call=section.call_sign, category=2, orderlist=2,
                                                                      mainid=section.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'执行段长(分局)',
                                       radio_station=section.channel, call=section.call_sign, category=2,
                                       orderlist=2, mainid=section.id+increment)
    for faculty in section.exec_chief_trans.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'执行段长(交通)', radio_station=section.channel,
                                                                      call=section.call_sign, category=2, orderlist=3,
                                                                      mainid=section.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'执行段长(交通)',
                                       radio_station=section.channel, call=section.call_sign, category=2,
                                       orderlist=3, mainid=section.id+increment)
    for faculty in section.exec_chief_armed_poli.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'执行段长(武警)', radio_station=section.channel,
                                                                      call=section.call_sign, category=2, orderlist=4,
                                                                      mainid=section.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'执行段长(武警)',
                                       radio_station=section.channel, call=section.call_sign, category=2,
                                       orderlist=4, mainid=section.id+increment)

for road in Road.objects.all():
    for faculty in road.chief.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'路长', radio_station=road.channel,
                                                                      call=road.call_sign, category=1, orderlist=1,
                                                                      mainid=road.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'路长',
                                       radio_station=road.channel, call=road.call_sign, category=1,
                                       orderlist=1, mainid=road.id+increment)
    for faculty in road.exec_chief_sub_bureau.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'执行路长(分局)', radio_station=road.channel,
                                                                      call=road.call_sign, category=1, orderlist=2,
                                                                      mainid=road.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'执行路长(分局)',
                                       radio_station=road.channel, call=road.call_sign, category=1,
                                       orderlist=2, mainid=road.id+increment)
    for faculty in road.exec_chief_trans.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'执行路长(交管)', radio_station=road.channel,
                                                                      call=road.call_sign, category=1, orderlist=3,
                                                                      mainid=road.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'执行路长(交管)',
                                       radio_station=road.channel, call=road.call_sign, category=1,
                                       orderlist=3, mainid=road.id+increment)
    for faculty in road.exec_chief_armed_poli.all():
        if guard_admin.objects.filter(uid=faculty.id+increment, category__isnull=False).count() == 0:
            guard_admin.objects.filter(uid=faculty.id+increment).update(dutyname=u'执行路长(武警)', radio_station=road.channel,
                                                                      call=road.call_sign, category=1, orderlist=4,
                                                                      mainid=road.id+increment)
        else:
            guard_admin.objects.create(uid=faculty.id+increment, duties=faculty.duty, username=faculty.name,
                                       phone=faculty.mobile, enabled=str(int(faculty.enabled)), dutyname=u'执行路长(武警)',
                                       radio_station=road.channel, call=road.call_sign, category=1,
                                       orderlist=4, mainid=road.id+increment)
