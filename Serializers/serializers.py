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
    class Meta:
        model = Faculty
        fields = (
            'id',
            'name',
            'mobile',
            'duty',
            'channel',
            'call_sign'
        )


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
            'start_point',
            'end_point',
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
            'start_point',
            'end_point',
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
            'start_point',
            'end_point',
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
            'start_point',
            'end_point',
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

