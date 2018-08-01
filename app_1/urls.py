# -*- coding: utf-8 -*-
from django.conf.urls import url
import Faculty_View, LoginView, RoadView, District_View, SectionView, StationView

urlpatterns = [

    # post 登陆，put修改密码
    url(r'^faculty/login/?$', LoginView.LoginView.as_view(), name='login_and_change_password'),
    # district列表
    url(r'^district/lists/?$', District_View.DistrictView.as_view(), name='district_lists'),
    # 人员增删改查
    url(r'^faculty/edit/?$', Faculty_View.FacultyView.as_view(), name='edit'),
    # 删除人员
    url(r'^faculty/delete/?$', Faculty_View.DeleteFacultyView.as_view(), name='delete_faculty'),
    # road
    url(r'^road/edit?$', RoadView.RoadView.as_view(), name='road'),
    # road 单条道路信息
    url(r'^road/single?$', RoadView.SingleRoadInfoView.as_view(), name='single_road_info'),
    # 删除道路
    url(r'^road/delete/?$', RoadView.DeleteRoadView.as_view(), name='delete_road'),
    # road 人员信息
    url(r'^road/faculty?$', RoadView.RoadFacultyView.as_view(), name='road_faculty'),
    # road 删除道路人员
    url(r'^road/faculty/delete?$', RoadView.DeleteRoadFaculty.as_view(), name='delete_road_faculty'),
    # section
    url(r'^section/edit?$', SectionView.SectionView.as_view(), name='section'),
    # 单条section信息
    url(r'^section/single?$', SectionView.SingleSectionView.as_view(), name='single_section_info'),
    # section 删除
    url(r'^section/delete/?$', SectionView.DeleteSectionView.as_view(), name='delete_section'),
    # section 人员信息
    url(r'^section/faculty?$', SectionView.SectionFacultyView.as_view(), name='section_faculty'),
    # 删除路段人员
    url(r'^section/faculty/delete?$', SectionView.DeleteSectionFacultyView.as_view(), name='delete_section_faculty'),
    # station
    url(r'^station/edit?$', StationView.StationView.as_view(), name='station'),
    # station 人员信息
    url(r'^station/faculty?$', StationView.StationFacultyView.as_view(), name='station_faculty'),
    # 删除岗位人员
    url(r'^station/faculty/delete?$', StationView.DeleteStationFacultyView.as_view(), name='delete_station_faculty'),
]
