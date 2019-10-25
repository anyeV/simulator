__author__ = "anyeV"

import pymysql
import contextlib
import datetime
import json


class SqlTools(object):

    # 初始化数据
    def __init__(self):
        self.__host = ''
        self.__port = 0
        self.__user = ''
        self.__passwd = ''

    # 建立mysql链接上下文
    @contextlib.contextmanager
    def __connect_db(self, db_name):
        connect = pymysql.Connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            passwd=self.__passwd,
            db=db_name,
            charset='utf8'
        )
        cursor = connect.cursor()
        try:
            yield cursor
        finally:
            connect.commit()
            cursor.close()
            connect.close()

    # 查询
    def get_data(self, sql, db_name):
        res = []
        with self.__connect_db(db_name) as cursor:
            cursor.execute(sql)
            collection = cursor.fetchall()
            len_collection = len(collection)
            if len_collection > 0:
                for row in collection:
                    res.append(row)
            else:
                pass
        return res

    # 更新
    def update_data(self, sql, db_name):
        with self.__connect_db(db_name) as cursor:
            effect_no = cursor.execute(sql)
            return effect_no

    # 插入
    def insert_data(self, sql, db_name):
        with self.__connect_db(db_name) as cursor:
            effect_no = cursor.execute(sql)
            return effect_no

    def to_strings(self, strings):
        return '"' + str(strings) + '"'

    # 获取当前时间
    def get_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 查询设备状态
    def select_equip(self, connector_id):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0][0]
        return result

    # 插入订单
    def insert_order(self, order_data, operator_id):
        sql = ''
        re_data = self.insert_data(sql, "")
        print("re_data: {0}".format(re_data))
        return re_data

    # 获取订单信息
    def get_order_info(self, order_id):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0]
        return result

    # 获取枪类型
    def get_connector_type(self, connector_id):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0][0]
        return result

    # 获取计费策略
    def get_policy(self, charge_type):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data
        return result

    # 保存运营商token
    def save_token(self, _token, token_type):
        sql = ''
        re_data = self.get_data(sql, "")
        return re_data

    # 获取运营商token
    def get_token(self, token_type):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0][0]
        return result

    # 获取当前时段计费策略
    def get_now_policy(self, charge_type):
        now_time = datetime.datetime.now().strftime('%H%M%S')
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0]
        return result

    # 更新订单状态
    def update_order_data(self, order_data):
        sql = ''
        re_data = self.update_data(sql, "")
        return re_data

    # 更新订单状态
    def update_order_status(self, order_id, order_status, end_charge_time):
        sql = ''
        re_data = self.update_data(sql, "")
        return re_data

    # 根据运营商id获取配置信息
    def get_imitator_config(self, operator_id):
        sql = ''
        print("sql:{0}".format(sql))
        re_data = self.get_data(sql, "")
        return re_data[0]

    # 查询充电站下枪
    def get_connector_by_station(self, station_id):
        sql = ''
        re_data = self.get_data(sql, "")
        result = []
        if re_data:
            [result.append(connector_id[0]) for connector_id in re_data]
        return result

    # 更新运营商配置-更新运营商
    def update_imitator_operator(self, operator_dict):
        sql = ''
        re_data = self.update_data(sql, "")
        return re_data

    # 更新运营商配置-更新设置
    def update_imitator_config(self, kwarges):
        sql = ''
        re_data = self.update_data(sql, "")
        return re_data

    # 根据qr_code查询枪id
    def get_connector_id_by_qr_code(self, qr_code):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0][0]
        return result

    # 获取设备运营商id
    def get_operator_id_by_connector(self, czb_connector_id):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0][0]
        return result

    # 根据订单id获取运营商id
    def get_operator_id_by_order(self, order_id):
        sql = ''
        re_data = self.get_data(sql, "")
        result = 0
        if re_data:
            result = re_data[0][0]
        return result
