__author__ = "anyeV"

from django.shortcuts import HttpResponse
from new_operator.ChargeFunc import ChargeF
import requests
import json
import datetime
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 页面接口-更改运营商
def query_change_operator(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_change_operator ******".format(now_time))
    print("请求: {0}".format(request.body))
    req = json.loads(request.body)
    cf = ChargeF()
    rep = cf.change_operator(req)
    return HttpResponse(rep, content_type="application/json")


# 页面接口-更新配置
def query_change_config(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_change_config ******".format(now_time))
    cf = ChargeF()
    rep = cf.change_config(request.body)
    return HttpResponse(rep, content_type="application/json")


# 页面接口-获取当前运营商配置
def query_get_config(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_change_config ******".format(now_time))
    cf = ChargeF()
    rep = cf.get_config()
    return HttpResponse(json.dumps(rep), content_type="application/json")


# 充电站信息
def query_stations_info(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_stations_info ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_stations_info()
    return HttpResponse(rep, content_type="application/json")


# 查询设备状态
def query_station_status(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_station_status ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_station_status(request.body)
    return HttpResponse(json.dumps(rep), content_type="application/json")


# 获取token
def get_token(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** get_token ******".format(now_time))
    cf = ChargeF()
    rep = cf.get_token()
    print("rep: {0}".format(rep))
    req = requests.post("https://www.baidu.com", data=rep, timeout=60, verify=False)
    Rjson = req.json()
    print("调用结果：{0},{1}".format(req, Rjson))
    de_t_data = cf.get_de_data(Rjson["Data"])
    AccessToken = de_t_data["AccessToken"]
    print("AccessToken: {0}".format(AccessToken))
    res_save = cf.save_token(AccessToken, 2)
    if res_save:
        print("保存token成功")
    return HttpResponse(json.dumps(Rjson), content_type="application/json")


# 请求设备认证
def query_equip_auth(request):
    # 请求token
    requests.post('http://www.baidu.com', data=request.body)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_equip_auth ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_equip_auth(request.body)
    return HttpResponse(rep, content_type="application/json")


# 平台认证
def query_token(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_token ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_token(request.body)
    return HttpResponse(rep, content_type="application/json")


# 查询业务策略信息
def query_equip_business_policy(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_equip_business_policy ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_equip_business_policy(request.body)
    return HttpResponse(rep, content_type="application/json")


# 请求启动充电（带手机号）
def query_start_charge_with_phone_num(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_start_charge_with_phone_num ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_start_charge(request.body)
    return_data = json.dumps(rep["rep"])
    try:
        return HttpResponse(return_data, content_type="application/json")
    finally:
        if rep["succ_stat"] == 0:
            time.sleep(1)
            headers = {
                "Content-Type": "application/json",
                "charset": "utf-8"
            }
            requests.post("http://www.baidu.com",
                          data=json.loads(return_data)["Data"],
                          timeout=60, headers=headers)


# 请求启动充电
def query_start_charge(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_start_charge ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_start_charge(request.body)
    return_data = json.dumps(rep["rep"])
    try:
        return HttpResponse(return_data, content_type="application/json")
    finally:
        if rep["succ_stat"] == 0:
            time.sleep(1)
            headers = {
                "Content-Type": "application/json",
                "charset": "utf-8"
            }
            requests.post("http://www.baidu.com",
                          data=json.loads(return_data)["Data"], timeout=60, headers=headers)


# 推送启动充电结果
def notification_start_charge_result(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** notification_start_charge_result ******".format(now_time))
    cf = ChargeF()
    rep = cf.notification_start_charge_result(request.body)
    operator_token = cf.get_operator_token(2)
    print("运营商token: {0}".format(operator_token))
    headers = {"Content-Type": "application/json"}
    req = requests.post("https://www.baidu.com",
                        headers=headers, data=json.dumps(rep["rep"]), verify=False)
    Rjson = req.json()
    print("调用结果：{0},{1}".format(req, Rjson))
    rData = Rjson.get("Data")
    deData = cf.get_de_data(rData)
    print("解析返回结果: {0}".format(deData))
    if deData["SuccStat"] == 0:
        print("推送启动充电结果成功！")
        return_data = {"code": 200, "Msg": "notification_start_charge_result Successful", "data": deData}
        # 推送设备状态变化为3
        sattion_status_rep = {"ConnectorID": rep["ConnectorID"], "StartChargeSeqStat": "3"}
        requests.post('http://www.baidu.com',
                      headers=headers, data=json.dumps(sattion_status_rep), verify=False)
    else:
        print("ERROR! 推送启动充电结果失败！")
        return_data = {"code": 500, "Msg": "notification_start_charge_result Failed", "data": cf.get_de_data(rData)}
    return HttpResponse(json.dumps(return_data), content_type="application/json")


# 查询充电状态
def query_equip_charge_status(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_equip_charge_status ******".format(now_time))
    _body = request.body
    cf = ChargeF()
    rep = cf.query_equip_charge_status(_body)
    try:
        return HttpResponse(rep["rep"], content_type="application/json")
    finally:
        headers = {
            "Content-Type": "application/json",
            "charset": "utf-8"
        }
        notification_data = rep["notification_data"]
        print("notification_data:{0}".format(notification_data))
        requests.post('http://www.baidu.com',
                      data=json.dumps(notification_data), headers=headers)


# 推送充电状态
def notification_equip_charge_status(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** notification_equip_charge_status ******".format(now_time))
    cf = ChargeF()
    rep = cf.notification_equip_charge_status(request.body)
    headers = {"Content-Type": "application/json"}
    req = requests.post('https://www.baidu.com',
                        headers=headers, data=json.dumps(rep), verify=False)
    Rjson = req.json()
    print(Rjson)
    rData = Rjson.get("Data")
    deData = cf.get_de_data(rData)
    print("调用结果：{0},{1}".format(req, deData))
    if cf.get_de_data(rData)["SuccStat"] == 0:
        print("推送停止充电结果成功！")
        rep = {"code": 200, "Msg": "notification_equip_charge_status Successful", "data": deData}

    else:
        print("ERROR! 推送停止充电结果失败！")
        rep = {"code": 500, "Msg": "notification_equip_charge_status Failed", "data": deData}
    return HttpResponse(json.dumps(rep), content_type="application/json")


# 请求停止充电
def query_stop_charge(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** query_stop_charge ******".format(now_time))
    cf = ChargeF()
    rep = cf.query_stop_charge(request.body)
    return_data = json.dumps(rep["rep"])
    try:
        return HttpResponse(return_data, content_type="application/json")
    finally:
        if rep["succ_stat"] == 0:
            redata = rep["returndata"]
            order_status = rep["charging_order_status"]
            # print("停止充电redata: {0}".format(redata))
            headers = {
                "Content-Type": "application/json",
                "charset": "utf-8"
            }
            time.sleep(1)
            requests.post("http://www.baidu.com",
                          data=redata, timeout=60, headers=headers)
            time.sleep(1)
            requests.post("http://www.baidu.com",
                          data=redata, timeout=60, headers=headers)
            if order_status == 4:
                pass
            else:
                time.sleep(1)
                requests.post("http://www.baidu.com",
                              data=redata, timeout=60, headers=headers)


# 推送停止充电结果
def notification_stop_charge_result(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** notification_stop_charge_result ******".format(now_time))
    cf = ChargeF()
    rep = cf.notification_stop_charge_result(request.body)
    headers = {"Content-Type": "application/json"}
    req = requests.post('https://www.baidu.com',
                        headers=headers, data=json.dumps(rep), verify=False)
    Rjson = req.json()
    rData = Rjson.get("Data")
    deData = cf.get_de_data(rData)
    print("调用结果：{0},{1}".format(req, deData))
    if cf.get_de_data(rData)["SuccStat"] == 0:
        print("推送停止充电结果成功！")
        rep = {"code": 200, "Msg": "notification_stop_charge_result Successful", "data": deData}
    else:
        print("ERROR! 推送停止充电结果失败！")
        rep = {"code": 500, "Msg": "notification_stop_charge_result Failed", "data": deData}
    return HttpResponse(json.dumps(rep), content_type="application/json")


# 设备状态变化推送
def notification_stationStatus(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** notification_stationStatus ******".format(now_time))
    cf = ChargeF()
    rep = cf.notification_station_status(request.body)
    headers = {"Content-Type": "application/json"}
    req = requests.post('https://www.baidu.com', headers=headers,
                        data=json.dumps(rep), verify=False)
    Rjson = req.json()
    rData = Rjson.get("Data")
    deData = cf.get_de_data(rData)
    print("调用结果：{0},{1}".format(req, deData))
    if deData["status"] == 0:
        print("推送设备状态变化成功！")
        rep = {"code": 200, "Msg": "notification_stop_charge_result Successful", "data": deData}
    else:
        print("ERROR! 推送设备状态变化失败！")
        rep = {"code": 500, "Msg": "notification_stop_charge_result Failed", "data": deData}
    return HttpResponse(json.dumps(rep), content_type="application/json")


# 推送充电订单信息
def notification_charge_order_info(request):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n{0} ****** notification_charge_order_info ******".format(now_time))
    cf = ChargeF()
    rep = cf.notification_charge_order_info(request.body)
    headers = {"Content-Type": "application/json"}

    req = requests.post('https://www.baidu.com',
                        headers=headers, data=json.dumps(rep), verify=False)
    Rjson = req.json()
    rData = Rjson.get("Data")
    deData = cf.get_de_data(rData)
    print("调用结果：{0},{1}".format(req, deData))
    notification_status = 0
    if deData:
        if deData["ConfirmResult"] == 0:
            notification_status = 1
            print("推送充电订单信息成功！")
            rep = {"code": 200, "Msg": "notification_charge_order_info Successful", "data": deData}
        else:
            print("ERROR! 推送充电订单信息失败！")
            rep = {"code": 500, "Msg": "notification_charge_order_info Failed", "data": deData}
    else:
        print("推送订单异常")
    try:
        return HttpResponse(json.dumps(rep), content_type="application/json")
    finally:
        if notification_status:
            redata = {"ConnectorID": deData["ConnectorID"], "StartChargeSeqStat": 2}
            requests.post("http://www.baidu.com",
                          data=cf.get_en_data(redata), timeout=60, headers=headers)
        else:
            print("订单推送异常，不推送设备状态")
