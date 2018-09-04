# -*- coding: utf-8 -*-
from __future__ import division
from rest_framework import serializers
from app_1.models import Faculty, Road, District, Section, Station, ServiceLine
from t.models import guard_line
from constants.constants import increment, pattern


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = (
            'id',
            'code',
            'name'
        )


class FacultySerializer(serializers.ModelSerializer):
    level_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()
    main_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = (
            'id',
            'name',
            'mobile',
            'duty',
            'channel',
            'call_sign',
            'level',
            'level_name',
            'role',
            'role_name',
            'main_id',
            'main_name',
            'district_id',
            'district_name',
            'enabled'
        )

    def get_level_name(self, obj):
        if obj.level == 1:
            return u'路'
        elif obj.level == 2:
            return u'段'
        elif obj.level == 3:
            return u'岗'
        else:
            return ''

    def get_role_name(self, obj):
        if obj.level == 1:
            if obj.role == 1:
                return u'路长'
            elif obj.role == 2:
                return u'执行路长(分局)'
            elif obj.role == 3:
                return u'执行路长(交管)'
            elif obj.role == 4:
                return u'执行路长(武警)'
            else:
                return ''
        elif obj.level == 2:
            if obj.role == 1:
                return u'段长'
            elif obj.role == 2:
                return u'执行段长(分局)'
            elif obj.role == 3:
                return u'执行段长(交通)'
            elif obj.role == 4:
                return u'执行段长(武警)'
            else:
                return ''
        elif obj.level == 3:
            if obj.role == 1:
                return u'岗长(分局)'
            elif obj.role == 2:
                return u'执行岗长(交通)'
            else:
                return ''
        else:
            return ''

    def get_main_name(self, obj):
        if obj.level == 1:
            if obj.main_id:
                return Road.objects.get(id=obj.main_id).name
            else:
                return ''
        elif obj.level == 2:
            if obj.main_id:
                return Section.objects.get(id=obj.main_id).name
            else:
                return ''
        elif obj.level == 3:
            if obj.main_id:
                return Station.objects.get(id=obj.main_id).name
            else:
                return ''
        else:
            return ''

    def get_district_name(self, obj):
        if obj.district:
            return obj.district.name
        else:
            return ''


class RoadSerializer(serializers.ModelSerializer):
    section_number = serializers.SerializerMethodField()
    station_number = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    related_service_line = serializers.SerializerMethodField()
    related_service_line_ids = serializers.SerializerMethodField()

    class Meta:
        model = Road
        fields = (
            'id',
            'name',
            'length',
            'start_place',
            'end_place',
            'section_number',
            'station_number',
            'channel',
            'call_sign',
            'remark1',
            'remark2',
            'remark3',
            'district_name',
            'related_service_line',
            'related_service_line_ids',
        )

    def get_section_number(self, obj):
        cur_section = obj.Road_Section.filter(enabled=True).all()
        return cur_section.count()

    def get_station_number(self, obj):
        cur_section = obj.Road_Section.filter(enabled=True).all()
        count = 0
        for item in cur_section:
            cur_station = item.Section_Station.filter(enabled=True).all()
            count = count + cur_station.count()
        return count

    def get_district_name(self, obj):
        if obj.district:
            return obj.district.name
        else:
            return ''

    def get_related_service_line(self, obj):
        service_list = obj.Road_Service.values_list('name', flat=True)
        return '-'.join(service_list)

    def get_related_service_line_ids(self, obj):
        service_list = obj.Road_Service.values_list('id', flat=True)
        if service_list:
            return list(service_list)
        else:
            return []


class SingleRoadSerializer(serializers.ModelSerializer):
    chief = FacultySerializer(many=True)
    exec_chief_sub_bureau = FacultySerializer(many=True)
    exec_chief_trans = FacultySerializer(many=True)
    exec_chief_armed_poli = FacultySerializer(many=True)

    class Meta:
        model = Road
        fields = (
            'id',
            'name',
            'start_place',
            'end_place',
            'channel',
            'call_sign',
            'chief',
            'exec_chief_sub_bureau',
            'exec_chief_trans',
            'exec_chief_armed_poli'
        )


class SectionSerializer(serializers.ModelSerializer):
    station_number = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    related_service_line = serializers.SerializerMethodField()
    related_service_line_ids = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id',
            'name',
            'start_place',
            'end_place',
            'xy_coordinate',
            'channel',
            'call_sign',
            'station_number',
            'remark1',
            'remark2',
            'remark3',
            'district_name',
            'related_service_line',
            'related_service_line_ids',
        )

    def get_station_number(self, obj):
        cur_station = obj.Section_Station.filter(enabled=True).all()
        return cur_station.count()

    def get_district_name(self, obj):
        if obj.district:
            return obj.district.name
        else:
            return ''

    def get_related_service_line(self, obj):
        if obj.road:
            service_list = obj.road.Road_Service.values_list('name', flat=True)
            return '-'.join(service_list)
        else:
            return ''

    def get_related_service_line_ids(self, obj):
        if obj.road:
            service_list = obj.road.Road_Service.values_list('id', flat=True)
            return list(service_list)
        else:
            return []


class SingleSectionSerializer(serializers.ModelSerializer):
    chief = FacultySerializer(many=True)
    exec_chief_sub_bureau = FacultySerializer(many=True)
    exec_chief_trans = FacultySerializer(many=True)
    exec_chief_armed_poli = FacultySerializer(many=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'name',
            'start_place',
            'end_place',
            'xy_coordinate',
            'channel',
            'call_sign',
            'chief',
            'exec_chief_sub_bureau',
            'exec_chief_trans',
            'exec_chief_armed_poli'
        )


class StationSerializer(serializers.ModelSerializer):
    district_name = serializers.SerializerMethodField()
    related_service_line = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = (
            'id',
            'name',
            'location',
            'channel',
            'call_sign',
            'remark1',
            'remark2',
            'remark3',
            'district_name',
            'related_service_line',
        )

    def get_district_name(self, obj):
        if obj.district:
            return obj.district.name
        else:
            return ''

    def get_related_service_line(self, obj):
        if obj.section:
            if obj.section.road:
                service_list = obj.section.road.Road_Service.values_list('name', flat=True)
                return '-'.join(service_list)
            else:
                return ''
        else:
            return ''


class SingleStationSerializer(serializers.ModelSerializer):
    chief = FacultySerializer(many=True)
    exec_chief_trans = FacultySerializer(many=True)

    class Meta:
        model = Station
        fields = (
            'id',
            'name',
            'location',
            'channel',
            'call_sign',
            'enabled',
            'chief',
            'exec_chief_trans'
        )


class SectionExcelSerializer(serializers.ModelSerializer):
    chief = FacultySerializer(many=True)
    exec_chief_sub_bureau = FacultySerializer(many=True)
    exec_chief_trans = FacultySerializer(many=True)
    exec_chief_armed_poli = FacultySerializer(many=True)
    Section_Station = SingleStationSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'name',
            'channel',
            'call_sign',
            'chief',
            'exec_chief_sub_bureau',
            'exec_chief_trans',
            'exec_chief_armed_poli',
            'Section_Station',
            'enabled'
        )


class RoadExcelSerializer(serializers.ModelSerializer):
    chief = FacultySerializer(many=True)
    exec_chief_sub_bureau = FacultySerializer(many=True)
    exec_chief_trans = FacultySerializer(many=True)
    exec_chief_armed_poli = FacultySerializer(many=True)
    section_station_num = serializers.SerializerMethodField()
    Road_Section = SectionExcelSerializer(many=True)

    class Meta:
        model = Road
        fields = (
            'id',
            'name',
            'length',
            'section_station_num',
            'channel',
            'call_sign',
            'chief',
            'exec_chief_sub_bureau',
            'exec_chief_trans',
            'exec_chief_armed_poli',
            'Road_Section',
        )

    def get_section_station_num(self,obj):
        cur_section = obj.Road_Section.filter(enabled=True).all()
        section_count = cur_section.count()
        station_count = 0
        for item in cur_section:
            cur_station = item.Section_Station.filter(enabled=True).all()
            station_count = station_count + cur_station.count()
        return str(section_count) + '-' + str(station_count)


class ServiceLineSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(many=True)
    road = RoadSerializer(many=True)
    roadCount = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = ServiceLine
        fields = (
            'id',
            'name',
            'startPlace',
            'endPlace',
            'time',
            'remark1',
            'remark2',
            'remark3',
            'district',
            'road',
            'roadCount',
            'submit_district',
            'points',
        )

    def get_roadCount(self, obj):
        district_id = int(self.context.get('district_id'))
        if district_id:
            return obj.road.filter(enabled=True, district_id=district_id).count()
        else:
            return obj.road.filter(enabled=True).count()

    def get_points(self, obj):
        points_list = []
        road_ids = obj.roadids
        if road_ids:
            road_id_list = road_ids.split('-')
            for road_id in road_id_list:
                cur_road = Road.objects.get(id=int(road_id))
                section_ids = cur_road.sectionids
                if not section_ids:
                    break
                section_id_list = section_ids.split('-')
                for section_id in section_id_list:
                    cur_section = Section.objects.get(id=int(section_id))
                    if pattern.search(cur_section.xy_coordinate):
                        points_list.append(cur_section.xy_coordinate)
        return points_list
