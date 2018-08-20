import django

from app_1.models import Station, Section, Road, ServiceLine, Faculty
from t.models import guard_line, guard_road, guard_section, guard_admin, guard_station

for item in Station.objects.all():
    item.chief.clear()
    item.exec_chief_trans.clear()

for item in Section.objects.all():
    item.chief.clear()
    item.exec_chief_armed_poli.clear()
    item.exec_chief_trans.clear()
    item.exec_chief_sub_bureau.clear()

for item in Road.objects.all():
    item.chief.clear()
    item.exec_chief_armed_poli.clear()
    item.exec_chief_trans.clear()
    item.exec_chief_sub_bureau.clear()

for item in ServiceLine.objects.all():
    item.road.clear()

ServiceLine.objects.all().delete()
Road.objects.all().delete()
Section.objects.all().delete()
Station.objects.all().delete()
Faculty.objects.all().delete()


guard_line.objects.all().delete()
guard_road.objects.all().delete()
guard_section.objects.all().delete()
guard_admin.objects.all().delete()
guard_station.objects.all().delete()