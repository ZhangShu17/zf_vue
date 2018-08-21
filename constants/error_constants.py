# coding=utf-8

ERR_STATUS_SUCCESS = [0, u"成功 | Success"]
ERR_STATUS_FAIL = [-1, u"失败 | Fail"]

ERR_INVALID_PARAMETER = [10000, u"请求参数错误"]

ERR_SAVE_INFO_FAIL = [20000, u"保存数据错误"]

ERR_INVALID_ACCOUNT = [30000, u"用户名或密码错误"]
ERR_INVALID_NEW_PASSWORD = [30001, u"新密码和旧密码相同"]
ERR_TOKEN_EXPIRED = [30002, u"token已过期"]
ERR_TOKEN_ERROR = [30003, u"token错误"]

ERR_NO_SECTION_IN_ROAD = [40001, u"路中没有路段"]
ERR_ONE_SECTION_IN_ROAD = [40002, u"路中仅有一条路段，无需排序"]
ERR_SECTION_FIRST = [40003, u"该路段已在第一位，无需升序"]
ERR_SECTION_LAST = [40004, u"该路段已在最后一位，无需降序"]

RR_NO_ROAD_IN_SERVICELINE = [50001, u"勤务中没有路线"]
ERR_ONE_ROAD_IN_SERVICELINE = [50002, u"勤务中仅有一条路路，无需排序"]
ERR_ROAD_FIRST = [50003, u"该路先已在第一位，无需升序"]
ERR_ROAD_LAST = [50004, u"该路线已在最后一位，无需降序"]

