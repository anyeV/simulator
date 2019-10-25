__author__ = "anyeV"

import json
from new_operator.AESMD5 import encrypt, decrypt, HMACMD5
from new_operator.SqlTools import SqlTools
import time
import datetime
from new_operator.OperatorStationList import get_operator_station_list


class ChargeF(object):

    def __init__(self):
        self.IV = ""
        self.KEY = ""
        # 实例化数据库类
        self.st = SqlTools()

    # 获取服务器设置
    def get_config(self, connector_id=None, order_id=None):
        if connector_id:
            operator_id = self.st.get_operator_id_by_connector(connector_id)
        elif order_id:
            operator_id = self.st.get_operator_id_by_order(order_id)
        else:
            operator_id = None

        # 获取服务器设置信息
        conf = self.st.get_imitator_config(operator_id)

        # 解压
        _id, yn, czb_operator_id, operator_id, operator_name, charge_status_details, pro_charging_status, charging_order_status, notification_charge_info_details, query_token_succ_stat, \
        query_token_fail_reason, policy_succ_stat, policy_fail_reason, start_charge_succ_stat, start_charge_fail_reason, \
        stop_charge_succ_stat, stop_charge_fail_reason, notification_charge_status_details, notification_stop_charge_succ_stat, \
        notification_stop_charge_fail_reason, charging_data_null, notification_charge_info, set_connector_status = conf

        # 封装备用
        re_data = {
            "czb_operator_id": czb_operator_id,
            "operator_id": operator_id,
            "operator_name": operator_name,
            "charge_status_details": charge_status_details,
            "pro_charging_status": pro_charging_status,
            "charging_order_status": charging_order_status,
            "notification_charge_info_details": notification_charge_info_details,
            "query_token_succ_stat": query_token_succ_stat,
            "query_token_fail_reason": query_token_fail_reason,
            "policy_succ_stat": policy_succ_stat,
            "policy_fail_reason": policy_fail_reason,
            "start_charge_succ_stat": start_charge_succ_stat,
            "start_charge_fail_reason": start_charge_fail_reason,
            "stop_charge_succ_stat": stop_charge_succ_stat,
            "stop_charge_fail_reason": stop_charge_fail_reason,
            "notification_charge_status_details": notification_charge_status_details,
            "notification_stop_charge_succ_stat": notification_stop_charge_succ_stat,
            "notification_stop_charge_fail_reason": notification_stop_charge_fail_reason,
            "charging_data_null": charging_data_null,
            "notification_charge_info": notification_charge_info,
            "set_connector_status": set_connector_status
        }
        return re_data

    # 页面方法-更新运营商
    def change_operator(self, operator_dict):
        change_res = self.st.update_imitator_operator(operator_dict)
        if change_res:
            print("更新运营商成功！")
            rep = {"status": 200, "Msg": "update successful"}
        else:
            print("无更新！运营商id: {0}".format(operator_dict))
            rep = {"status": 500,
                   "Msg": "update failed.with no need for updated.post 'czb_operator_id ' or 'operator_id' as json"}
        return json.dumps(rep)

    # 页面方法-更新设置
    def change_config(self, json_arges):
        change_res = self.st.update_imitator_config(json_arges)
        if change_res:
            print("更新设置成功！")
            rep = {"status": 200, "Msg": "update successful"}
        else:
            print("更新失败! 更新内容: {0}".format(json_arges))
            rep = {"status": 500, "Msg": "update failed"}
        return json.dumps(rep)

    # 获取当前时间
    def now_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 加密
    def get_en_data(self, data):
        de_data = encrypt(self.KEY, data, self.IV)
        return de_data

    # 解析data
    def get_de_data(self, data):
        json_de_data = {}
        try:
            de_data = decrypt(self.KEY, data, self.IV)
            json_de_data = json.loads(de_data)
            # print("解析data: {0}".format(de_data))
        except:
            print("data解析失败: {0}".format(data))
        return json_de_data

    # 构造返回
    def get_rep(self, data, notification=None, operator_id=None):
        re_data = {"Ret": 0, "Msg": "", "Data": {}}
        if notification and operator_id:
            timestamp = str(round(time.time() * 1000))
            re_data = {"OperatorID": operator_id, "Data": {}, "TimeStamp": timestamp[:-3], "Seq": '0' + timestamp[-3:]}
        if isinstance(data, dict):
            # data加密
            en_data = encrypt(self.KEY, data, self.IV)
            re_data.update({"Data": en_data})
            # 拼接加签字符串
            sig_strs = ""
            for value in re_data.values():
                sig_strs += str(value)
            # print("sig_strs: " + sig_strs)
            # 加签
            sig = HMACMD5(sig_strs, self.KEY)
            # 拼返回
            re_data.update({"Sig": sig})
            # print("return_data: {0}".format(re_data))
            return re_data
        else:
            print("data参数错误: {0}, type: {1}".format(data, type(data)))
            return {}

    # 根据类型获取token
    def get_operator_token(self, token_type):
        return self.st.get_token(token_type)

    # 充电站信息
    def query_stations_info(self):
        cf = self.get_config()
        operator_id = cf["operator_id"]
        operator_name = cf["operator_name"]
        print("当前运营商id: {0},运营商名称: {1}".format(operator_id, operator_name))
        stations_data = {
            "ItemSize": 1,
            "PageCount": 1,
            "PageNo": 1,
            "StationInfos": []
        }
        # 定制充电站list
        station_info_list = get_operator_station_list(operator_id, 2)
        stations_data.update({"ItemSize": len(station_info_list), "StationInfos": station_info_list})
        print("stations_data: {0}".format(stations_data))
        # 拼返回数据包
        rep = self.get_rep(stations_data)
        return json.dumps(rep)

    # 请求设备认证
    def query_equip_auth(self, body):
        req = json.loads(body)
        # 解密Data
        de_data = self.get_de_data(req["Data"])
        print("解析请求data: {0}".format(de_data))
        if de_data:
            EquipAuthSeq = de_data["EquipAuthSeq"]
            ConnectorID = de_data["ConnectorID"]
            succ_stat = 1
            fail_reason = 2
            # 检查设备状态
            if int(self.st.select_equip(ConnectorID)):
                succ_stat = 0
                fail_reason = 0
            # 拼返回data
            rep_data = {
                "EquipAuthSeq": EquipAuthSeq,
                "ConnectorID": ConnectorID,
                "SuccStat": succ_stat,
                "FailReason": fail_reason
            }
            print("返回data: {0}".format(rep_data))
            # 拼返回数据包
            rep = self.get_rep(rep_data)
            return json.dumps(rep)
        else:
            return

    # 平台认证
    def query_token(self, body):
        cf = self.get_config()
        succ_stat = cf["query_token_succ_stat"]
        fail_reason = cf["query_token_fail_reason"]
        print("成功状态设置:{0},失败原因:{1}".format(succ_stat, fail_reason))
        req = json.loads(body)
        # 解密Data
        de_data = self.get_de_data(req["Data"])
        print("解析请求data: {0}".format(de_data))
        # 获取token
        AccessToken = self.st.get_token(1)
        if de_data:
            operator_id = de_data["OperatorID"]
            # 拼返回data
            rep_data = {
                "OperatorID": operator_id,
                "SuccStat": succ_stat,
                "AccessToken": AccessToken,
                "TokenAvailableTime": 7200,
                "FailReason": fail_reason
            }
            print("返回data: {0}".format(rep_data))
            # 拼返回数据包
            rep = self.get_rep(rep_data)
            return json.dumps(rep)
        else:
            return

    # 获取token
    def get_token(self, operator_secret=""):
        cf = self.get_config()
        operator_id = cf["operator_id"]
        operator_name = cf["operator_name"]
        # print("当前运营商id: {0},运营商名称: {1}".format(operator_id, operator_name))
        _data = {
            "OperatorID": operator_id,
            "OperatorSecret": operator_secret
        }
        print("rData:{0}".format(_data))
        # data加密
        en_data = encrypt(self.KEY, _data, self.IV)
        re_data = {
            "OperatorID": operator_id,
            "Data": en_data,
            "TimeStamp": "20180808095855",
            "Seq": "0001"
        }
        # 拼接加签字符串
        sig_strs = ""
        for value in re_data.values():
            sig_strs += str(value)
        # print("sig_strs: " + sig_strs)
        # 加签
        sig = HMACMD5(sig_strs, self.KEY)
        # 拼返回
        re_data.update({"Sig": sig})
        return json.dumps(re_data)

    # 保存token
    def save_token(self, _token, token_type):
        re_data = self.st.save_token(_token, token_type)
        return re_data

    # 查询业务策略信息
    def query_equip_business_policy(self, body, not_policy_infos=1):
        cf = self.get_config()
        succ_stat = cf["policy_succ_stat"]
        fail_reason = cf["policy_fail_reason"]
        print("成功状态设置:{0},失败原因:{1}".format(succ_stat, fail_reason))
        print(body)
        _data = json.loads(body)["Data"]
        # 解密Data
        de_data = self.get_de_data(_data)
        if de_data:
            EquipBizSeq = de_data["EquipBizSeq"]
            ConnectorID = de_data["ConnectorID"]
            # 获取设备类型
            connector_type = self.st.get_connector_type(ConnectorID)
            # 获取计费策略
            policy_list = self.st.get_policy(connector_type)
            PolicyInfos = []
            if not_policy_infos and policy_list:
                [PolicyInfos.append({
                    "StartTime": elm[2],
                    "ElecPrice": elm[3],
                    "SevicePrice": elm[4]
                }) for elm in policy_list]
            # 拼返回data
            rep_data = {
                "EquipBizSeq": EquipBizSeq,
                "ConnectorID": ConnectorID,
                "SuccStat": succ_stat,
                "FailReason": fail_reason,
                "SumPeriod": len(PolicyInfos),
                "PolicyInfos": PolicyInfos
            }
            print("返回data：{0}".format(rep_data))
            # 拼返回数据包
            rep = self.get_rep(rep_data)
            return json.dumps(rep)
        else:
            return

    # 请求启动充电
    def query_start_charge(self, body):
        print("接收到的请求: {0}".format(body))
        req = json.loads(body)
        # 解密Data
        de_data = self.get_de_data(req["Data"])
        print("解析请求data: {0}".format(de_data))
        if de_data:
            StartChargeSeq = de_data["StartChargeSeq"]
            ConnectorID = de_data["ConnectorID"]
            cf = self.get_config(connector_id=ConnectorID)
            succ_stat = cf["start_charge_succ_stat"]
            fail_reason = cf["start_charge_fail_reason"]
            con_operator_id = cf["operator_id"]
            print("订单id:{0},运营商id:{1}".format(StartChargeSeq, con_operator_id))
            print("成功状态设置:{0},失败原因:{1}".format(succ_stat, fail_reason))
            operator_id = self.st.get_operator_id_by_connector(ConnectorID)
            StartChargeSeqStat = 2
            # 拼返回data
            rep_data = {
                "StartChargeSeqStat": StartChargeSeqStat,
                "StartChargeSeq": StartChargeSeq,
                "ConnectorID": ConnectorID,
                "SuccStat": succ_stat,
                "FailReason": fail_reason
            }
            print("返回data：{0}".format(rep_data))

            # 如果启动成功，创建订单
            if succ_stat == 0:
                self.st.insert_order(rep_data, operator_id)
            # 拼返回数据包
            rep = self.get_rep(rep_data)
            print("rep:{0}".format(rep))
            return {"rep": rep, "succ_stat": succ_stat}
        else:
            return

    # 自定义返回数据
    def query_equip_charge_status_error(self):
        rep = {"Ret": 4004, "Msg": "ERROR", "Data": "", "Sig": ""}
        return json.dumps(rep)

    # 自定义返回数据
    def charge_status_pro(self):
        update_rep_data = {
            "ConnectorStatus": 0,
            "Soc": 0.0,
            "SeviceMoney": 0.0,
            "TotalMoney": 0.0,
            "SumPeriod": 0
        }
        return update_rep_data

    # 查询充电状态
    def query_equip_charge_status(self, body):
        req = json.loads(body)

        # 解密Data
        de_data = self.get_de_data(req["Data"])
        print("解析请求data: {0}".format(de_data))
        if de_data:
            StartChargeSeq = de_data["StartChargeSeq"]
            order_info = self.st.get_order_info(StartChargeSeq)
            if order_info:
                # 解压 order_info
                order_id, order_status, connector_id, operator_id, start_charge_time, end_charge_time, \
                total_service_money, total_elec_money, total_money, total_power, ident_code = order_info
                cf = self.get_config(order_id=StartChargeSeq)
                charging_data_null = cf["charging_data_null"]
                pro_charging_status = cf["pro_charging_status"]
                charging_order_status = cf["charging_order_status"]
                con_operator_id = cf["operator_id"]
                print("订单id:{0},运营商id:{1}".format(order_id, con_operator_id))
                # 是否启用自定义数据
                if charging_data_null:
                    rep = self.query_equip_charge_status_error()
                    print("当前charging_data_null: {0}, 返回: {1}".format(charging_data_null, rep))
                    return rep
                else:
                    pass
                details = cf["charge_status_details"]
                print("当前充电中明细设置:{0}".format(details))
                if charging_order_status:
                    order_status = charging_order_status
                else:
                    pass
                # 获取设备类型
                connector_type = self.st.get_connector_type(connector_id)
                # 查询当前时间策略
                now_policy = self.st.get_now_policy(connector_type)
                if now_policy:
                    _, add_power, time_phase, operator_elec_price, operator_sevice_price, operator_park_fee, charge_type, *ts = now_policy
                    print("当前时间策略｛电增量:{0},时段:{1},电费单价:{2},服务费单价:{3},占桩费:{4},类型:{5}｝".format(
                        add_power, time_phase, operator_elec_price, operator_sevice_price, operator_park_fee,
                        charge_type))
                    # 计算充电数据
                    sum_total_power = total_power + add_power
                    sum_elec_money = total_elec_money + operator_elec_price * add_power
                    sum_sevice_money = total_service_money + operator_sevice_price * add_power
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sum_total_money = sum_elec_money + sum_sevice_money
                    SumPeriod = 1

                    # 组装明细数据
                    ChargeDetails = [{
                        "DetailStartTime": start_charge_time,
                        "DetailEndTime": now_time,
                        "ElecPrice": operator_elec_price,
                        "SevicePrice": operator_sevice_price,
                        "DetailPower": round(sum_total_power, 2),
                        "DetailElecMoney": round(sum_elec_money, 2),
                        "DetailSeviceMoney": round(sum_sevice_money, 2)
                    }]
                    if not details:
                        ChargeDetails = []
                        SumPeriod = 0

                    # 拼返回
                    rep_data = {
                        "StartChargeSeqStat": order_status,
                        "StartChargeSeq": StartChargeSeq,
                        "ConnectorID": connector_id,
                        "ConnectorStatus": 3,
                        "CurrentA": 56.11121,
                        "CurrentB": 0.0,
                        "CurrentC": 0.0,
                        "VoltageA": 975.11233,
                        "VoltageB": 0.0,
                        "VoltageC": 0.0,
                        "Soc": 90.0,
                        "StartTime": start_charge_time,
                        "EndTime": now_time,
                        "TotalPower": round(sum_total_power, 2),
                        "ElecMoney": round(sum_elec_money, 2),
                        "SeviceMoney": round(sum_sevice_money, 2),
                        "TotalMoney": round(sum_total_money, 2),
                        "SumPeriod": SumPeriod,
                        "ChargeDetails": ChargeDetails
                    }
                    # 更新充电状态
                    if self.st.update_order_data(rep_data):
                        print("订单状态更新成功！")
                    else:
                        print("ERROR! 订单更新失败！")

                    # 交流设备不返回Soc
                    if connector_type == 3:
                        rep_data.update({"Soc": 1.0})

                    # 是否启用自定义数据
                    if pro_charging_status:
                        update_rep_data = self.charge_status_pro()
                        rep_data.update(update_rep_data)
                    print("返回data：{0}".format(rep_data))
                    # 拼接返回
                    rep = self.get_rep(rep_data)
                    notification_data = {"StartChargeSeq": StartChargeSeq}
                    return {"rep": json.dumps(rep), "notification_data": notification_data}
                else:
                    print("ERROR! 未找到当前时段计费策略！")
            else:
                print("ERROR! 未找到订单：{0}".format(StartChargeSeq))
        else:
            return

    # 停止充电
    def query_stop_charge(self, body):
        req = json.loads(body)
        # 解密Data
        de_data = self.get_de_data(req["Data"])
        print("解析请求data: {0}".format(de_data))
        StartChargeSeq = de_data["StartChargeSeq"]
        cf = self.get_config(order_id=StartChargeSeq)
        succ_stat = cf["stop_charge_succ_stat"]
        fail_reason = cf["stop_charge_fail_reason"]
        con_operator_id = cf["operator_id"]
        charging_order_status = cf["charging_order_status"]
        print("订单id:{0},运营商id:{1}".format(StartChargeSeq, con_operator_id))
        print("成功状态设置:{0},失败原因:{1}".format(succ_stat, fail_reason))
        StartChargeSeqStat = 3
        if de_data:
            rep_data = {
                "StartChargeSeqStat": StartChargeSeqStat,
                "SuccStat": succ_stat,
                "FailReason": fail_reason
            }
            print("返回data：{0}".format(rep_data))

            # 拼接返回
            rep = self.get_rep(rep_data)

            # 获取订单信息
            order_info = self.st.get_order_info(StartChargeSeq)

            # 解压 order_info
            order_id, order_status, connector_id, operator_id, start_charge_time, end_charge_time, \
            total_service_money, total_elec_money, total_money, total_power, ident_code = order_info
            returndata = {"StartChargeSeq": StartChargeSeq, "ConnectorID": connector_id, "StartTime": start_charge_time,
                          "StartChargeSeqStat": StartChargeSeqStat}
            print("拼装推送data: {0}".format(returndata))
            # returndata加密
            en_returndata = encrypt(self.KEY, returndata, self.IV)
            return {"rep": rep, "succ_stat": succ_stat, "returndata": en_returndata,
                    "charging_order_status": charging_order_status}
        else:
            return

    # 推送启动充电结果
    def notification_start_charge_result(self, data, ident_code="7890"):

        de_data = self.get_de_data(data)
        print("解析请求data: {0}".format(de_data))
        if de_data:
            req = de_data
        else:
            req = json.loads(data)
        StartChargeSeq = req["StartChargeSeq"]
        StartChargeSeqStat = req["StartChargeSeqStat"]
        ConnectorID = req["ConnectorID"]
        StartTime = self.now_time()
        IdentCode = ident_code

        cf = self.get_config(order_id=StartChargeSeq)
        operator_id = cf["operator_id"]
        operator_name = cf["operator_name"]
        print("当前运营商id: {0},运营商名称: {1}".format(operator_id, operator_name))

        rep_data = {
            "StartChargeSeq": StartChargeSeq,
            "StartChargeSeqStat": StartChargeSeqStat,
            "ConnectorID": ConnectorID,
            "StartTime": StartTime,
            "IdentCode": IdentCode
        }
        print("返回data: {0}".format(rep_data))
        rep = self.get_rep(rep_data, notification=1, operator_id=operator_id)
        print("rep: {0}".format(rep))
        return {"rep": rep, "ConnectorID": ConnectorID}

    # 推送充电状态
    def notification_equip_charge_status(self, body):
        order_id = ""
        print("data:{0}".format(body))
        req = json.loads(body)
        order_id = req["StartChargeSeq"]
        print("推送的订单id: {0}".format(order_id))
        cf = self.get_config(order_id=order_id)
        details = cf["notification_charge_status_details"]
        print("当前推送充电中明细设置:{0}".format(details))
        print("请求推送的订单: {0}".format(order_id))
        order_info = self.st.get_order_info(order_id)
        order_id, order_status, connector_id, operator_id, start_charge_time, end_charge_time, \
        total_service_money, total_elec_money, total_money, total_power, ident_code = order_info
        if int(order_status) == 2:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 获取设备类型
            connector_type = self.st.get_connector_type(connector_id)
            # 查询当前时间策略
            now_policy = self.st.get_now_policy(connector_type)
            print("当前时间策略: {0}".format(now_policy))
            if now_policy:
                _, add_power, _, operator_elec_price, operator_sevice_price, operator_park_fee, *ts = now_policy
                SumPeriod = 1
                ChargeDetails = [{
                    "DetailStartTime": start_charge_time,
                    "DetailEndTime": now_time,
                    "ElecPrice": operator_elec_price,
                    "SevicePrice": operator_sevice_price,
                    "DetailPower": round(total_power, 2),
                    "DetailElecMoney": round(total_elec_money, 2),
                    "DetailSeviceMoney": round(total_service_money, 2)
                }]
                if not details:
                    ChargeDetails = []
                    SumPeriod = 0
                rep_data = {
                    "StartChargeSeqStat": order_status,
                    "StartChargeSeq": 4,
                    "ConnectorID": connector_id,
                    "ConnectorStatus": 3,
                    "CurrentA": 78.1,
                    "CurrentB": 0.0,
                    "CurrentC": 0.0,
                    "VoltageA": 575.3,
                    "VoltageB": 0.0,
                    "VoltageC": 0.0,
                    "Soc": 90.0,
                    "StartTime": start_charge_time,
                    "EndTime": now_time,
                    "TotalPower": round(total_power, 2),
                    "ElecMoney": round(total_elec_money, 2),
                    "SeviceMoney": round(total_service_money, 2),
                    "TotalMoney": round(total_money, 2),
                    "SumPeriod": SumPeriod,
                    "ChargeDetails": ChargeDetails
                }
                # 拼接返回
                print("返回data: {0}".format(rep_data))
                rep = self.get_rep(rep_data, notification=1, operator_id=cf["operator_id"])
                print("return_data: {0}".format(rep))
                return json.dumps(rep)
            else:
                print("ERROR! 当前时间没有计费策略")
        else:
            print("ERROR! 不是充电中的订单: {0}".format(order_id))

    # 推送停止充电结果
    def notification_stop_charge_result(self, data, operator_id=None):

        de_data = self.get_de_data(data)
        print("解析请求data: {0}".format(de_data))
        if de_data:
            req = de_data
        else:
            req = json.loads(data)
        StartChargeSeq = req["StartChargeSeq"]
        StartChargeSeqStat = req["StartChargeSeqStat"]
        ConnectorID = req["ConnectorID"]

        cf = self.get_config(order_id=StartChargeSeq)
        SuccStat = cf["notification_stop_charge_succ_stat"]
        FailReason = cf["notification_stop_charge_fail_reason"]
        print("成功状态设置:{0},失败原因:{1}".format(SuccStat, FailReason))
        if not operator_id:
            operator_id = cf["operator_id"]

        if int(StartChargeSeqStat) == 3:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if self.st.update_order_status(StartChargeSeq, 4, now_time):
                print("停止充电更新订单成功：{0}".format(StartChargeSeq))
            else:
                SuccStat = 1
                FailReason = 6
                print("ERROR! 停止充电更新订单失败！")
        else:
            SuccStat = 1
            FailReason = 7
            print("ERROR! 没有正在充电的订单！")
        rep_data = {
            "StartChargeSeqStat": 4,
            "StartChargeSeq": StartChargeSeq,
            "ConnectorID": ConnectorID,
            "SuccStat": SuccStat,
            "FailReason": FailReason
        }
        print("返回data: {0}".format(rep_data))
        rep = self.get_rep(rep_data, notification=1, operator_id=operator_id)
        return rep

    # 查询设备状态
    def query_station_status(self, data):
        cf = self.get_config()
        set_connector_status = cf["set_connector_status"]
        req = json.loads(data)
        de_data = self.get_de_data(req["Data"])
        print("解析请求data: {0}".format(de_data))
        if de_data:
            de_req = de_data
        else:
            de_req = req["Data"]
        print("de_req: {0}".format(de_req))
        station_info = {
            "StationID": "",
            "ConnectorStatusInfos": []
        }

        rep_data = {
            "Total": "1",
            "StationStatusInfos": []
        }
        total = 0
        for station_id in de_req["StationIDs"]:
            connector_id_list = self.st.get_connector_by_station(station_id)
            if connector_id_list:
                total += 1
                station_info.update({"StationID": station_id})
                for connector_id in connector_id_list:
                    station_info["ConnectorStatusInfos"].append(
                        {"ConnectorID": connector_id, "Status": set_connector_status, "ParkStatus": 0, "LockStatus": 0})
            rep_data["StationStatusInfos"].append(station_info)
        rep_data.update({"Total": total})

        print("返回data: {0}".format(rep_data))
        rep = self.get_rep(rep_data)
        print("rep: {0}".format(rep))
        return rep

    # 推送设备状态
    def notification_station_status(self, data):
        # 解密Data
        de_data = self.get_de_data(data)
        print("解析请求data: {0}".format(de_data))
        if de_data:
            req = de_data
        else:
            req = json.loads(data)
        ConnectorID = req["ConnectorID"]
        ConnectorStatus = req["StartChargeSeqStat"]

        cf = self.get_config(connector_id=ConnectorID)
        operator_id = cf["operator_id"]
        operator_name = cf["operator_name"]
        print("当前运营商id: {0},运营商名称: {1}".format(operator_id, operator_name))

        rep_data = {
            "ConnectorStatusInfo": {
                "ConnectorID": ConnectorID,
                "Status": ConnectorStatus,
                "ParkStatus": 0,
                "LockStatus": 0
            }
        }
        print("返回data: {0}".format(rep_data))
        # 拼返回
        rep = self.get_rep(rep_data, notification=1, operator_id=operator_id)
        return rep

    # 推送充电订单信息
    def notification_charge_order_info(self, data):
        # 解密Data
        de_data = self.get_de_data(data)
        print("解析请求data: {0}".format(de_data))
        if de_data:
            req = de_data
        else:
            print("接收非加密参数：{0}".format(data))
            req = json.loads(data)
        StartChargeSeq = req["StartChargeSeq"]
        ConnectorID = req["ConnectorID"]

        cf = self.get_config(order_id=StartChargeSeq)
        details = cf["notification_charge_info_details"]
        notification_charge_info = cf["notification_charge_info"]
        print("当前充电订单明细设置:{0}, 推送成功状态：{1}".format(details, notification_charge_info))

        # 获取订单信息
        order_info = self.st.get_order_info(StartChargeSeq)
        if order_info:
            # 解压 order_info
            order_id, order_status, connector_id, operator_id, start_charge_time, end_charge_time, \
            total_service_money, total_elec_money, total_money, total_power, ident_code = order_info
            # 获取当前计费策略
            now_policy = self.st.get_now_policy(self.st.get_connector_type(ConnectorID))
            _, add_power, _, elec_price, server_price, park_fee, charge_type, _ = now_policy

            # 设置明细
            if details:
                ChargeDetails = [{
                    "DetailStartTime": start_charge_time,
                    "DetailEndTime": end_charge_time,
                    "ElecPrice": elec_price,
                    "SevicePrice": server_price,
                    "DetailPower": total_power,
                    "DetailElecMoney": total_elec_money,
                    "DetailSeviceMoney": total_service_money
                }]
                SumPeriod = 1
            else:
                ChargeDetails = []
                SumPeriod = 0

            # 返回data
            rep_data = {
                "StartChargeSeq": order_id,
                "ConnectorID": connector_id,
                "StartTime": start_charge_time,
                "EndTime": end_charge_time,
                "TotalPower": total_power,
                "TotalElecMoney": total_elec_money,
                "TotalSeviceMoney": total_service_money,
                "TotalMoney": total_money,
                "StopReason": 2,
                "SumPeriod": SumPeriod,
                "StayCost": 0.0,
                "ChargeDetails": ChargeDetails
            }
            print("返回data: {0}".format(rep_data))
            if notification_charge_info:
                rep_data = {}
            # 拼返回
            rep = self.get_rep(rep_data, notification=1, operator_id=operator_id)
            return rep
        else:
            return
