# -*- coding: utf-8 -*-
from django.conf.urls import url
import Faculty_View, LoginView, RoadView, District_View, SectionView, StationView, ServiceLine

urlpatterns = [
    #  get请求创建区
    url(r'^district/create/?$', LoginView.CreateDistrictView.as_view(), name='create_district'),

    #  get请求创建账号
    url(r'^account/create/?$', LoginView.CreateAccountView.as_view(), name='create_account'),

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

    # 路线所有信息页面展示
    url(r'^road/excel/info?$', RoadView.RoadExcelView.as_view(), name='road_excel_info'),

    # 勤务路线
    url(r'^server_line/edit?$',ServiceLine.ServiceLineView.as_view(), name='server_line'),

    # 分局提交勤務路綫
    url(r'^server_line/submit?$',ServiceLine.SubmitServiceLineView.as_view(), name='server_line_submit'),

    # 未添加到勤务路线的道路,
    url(r'^road/tobe_service_line?$', RoadView.RoadNotInToServiceLineView.as_view(), name='tobe_service_line'),

    # 未添加到给定道路的路段列表
    url(r'^section/tobe_road?$', SectionView.SectionNotInToRoadView.as_view(), name='tobe_road'),

    # 未添加到给定路段的岗位列表
    url(r'^station/tobe_section?$', StationView.StationNotInToSectionView.as_view(), name='tobe_section'),

    # 未添加到road的人员表
    url(r'^faculty/tobe_road?$', RoadView.FacultyNotInRoad.as_view(), name='faculty_tobe_road'),

    # 未添加到section的人员表
    url(r'^faculty/tobe_section?$', SectionView.FacultyNotInSection.as_view(), name='faculty_tobe_section'),

    # 未添加到station的人员表
    url(r'^faculty/tobe_station?$', StationView.FacultyNotInStation.as_view(), name='faculty_tobe_station'),

    # 复制station
    url(r'^copy/station?$', StationView.CopyStationView.as_view(), name='copy_station'),

    # 复制section
    url(r'^copy/section?$', SectionView.CopySectionView.as_view(), name='copy_section'),

    # 复制road
    url(r'^copy/road?$', RoadView.CopyRoadView.as_view(), name='copy_road'),

]
