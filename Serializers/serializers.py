# -*- coding: utf-8 -*-
from __future__ import division
from rest_framework import serializers
from app_1.models import Faculty, Road, District, Section, Station, ServiceLine


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
            'district_id'
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



class RoadSerializer(serializers.ModelSerializer):
    section_number = serializers.SerializerMethodField()
    station_number = serializers.SerializerMethodField()
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
            'remark1',
            'remark2',
            'remark3'
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
            'chief',
            'exec_chief_sub_bureau',
            'exec_chief_trans',
            'exec_chief_armed_poli'
        )


class SectionSerializer(serializers.ModelSerializer):
    station_number = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id',
            'name',
            'start_place',
            'end_place',
            'xy_coordinate',
            'station_number',
            'remark1',
            'remark2',
            'remark3'
        )

    def get_station_number(self, obj):
        cur_station = obj.Section_Station.filter(enabled=True).all()
        return cur_station.count()


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
            'chief',
            'exec_chief_sub_bureau',
            'exec_chief_trans',
            'exec_chief_armed_poli'
        )


class StationSerializer(serializers.ModelSerializer):
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
            'remark3'
        )


class SingleStationSerializer(serializers.ModelSerializer):
    chief = FacultySerializer(many=True)
    exec_chief_trans = FacultySerializer(many=True)

    class Meta:
        model = Station
        fields = (
            'id',
            'name',
            'location',
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
            'chief',
            'exec_chief_sub_bureau',
            'exec_chief_trans',
            'exec_chief_armed_poli',
            'Section_Station',
        )


class RoadExcelSerializer(serializers.ModelSerializer):
    chief = FacultySerializer(many=True)
    exec_chief_sub_bureau = FacultySerializer(many=True)
    exec_chief_trans = FacultySerializer(many=True)
    exec_chief_armed_poli = FacultySerializer(many=True)
    section_station_num = serializers.SerializerMethodField()
    Road_Section = SectionExcelSerializer(many=True, )

    class Meta:
        model = Road
        fields = (
            'id',
            'name',
            'length',
            'section_station_num',
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
        )

    def get_roadCount(self, obj):
        return obj.road.filter(enabled=True).count()

