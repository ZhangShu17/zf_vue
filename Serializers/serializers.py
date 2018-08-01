# -*- coding: utf-8 -*-
from __future__ import division
from rest_framework import serializers
from app_1.models import Faculty, Road, District, Section, Station


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
