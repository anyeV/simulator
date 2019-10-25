__author__ = "anyeV"


def get_operator_station_list(operator_id, station_count):
    station_info_list = []
    if isinstance(station_count, int):
        station_count += 1
    else:
        station_count = 2
    for i_station in range(1, station_count):
        station_info = {
            "OperatorID": operator_id,
            "StationID": "{1}1100000{0}".format(str(i_station), str(operator_id)),
            "StationName": "测试模拟站{0}".format(str(i_station)),
            "EquipmentOwnerID": operator_id,
            "CountryCode": "CN",
            "AreaCode": "44178{0}".format(str(i_station)),
            "Address": "北京",
            "ServiceTel": "123456789",
            "StationType": 1,
            "StationStatus": 50,
            "ParkNums": 3,
            "StationLng": 119.97049 + i_station / 100000,
            "StationLat": 31.717877 + i_station / 100000,
            "Construction": 1,
            "Pictures": [],
            "EquipmentInfos": []
        }
        equipment_info_type_3 = {
            "EquipmentID": "1100000{0}01".format(str(i_station)),
            "ManufacturerID": "123456789",
            "EquipmentModel": "p3",
            "ProductionDate": "2016-04-26",
            "EquipmentType": 3,
            "Power": "3.3",
            "EquipmentName": "交流{0}号桩".format(str(i_station)),
            "ConnectorInfos": []
        }
        connector_info_type_3 = {
            "ConnectorID": "1100000{0}0101".format(str(i_station)),
            "ConnectorType": 3,
            "VoltageUpperLimits": 220,
            "VoltageLowerLimits": 220,
            "Current": 15,
            "NationalStandard": 1,
            "Power": 30.3
        }
        equipment_info_type_3["ConnectorInfos"].append(connector_info_type_3)
        station_info["EquipmentInfos"].append(equipment_info_type_3)
        equipment_info_type_4 = {
            "EquipmentID": "1100000{0}02".format(str(i_station)),
            "ManufacturerID": "123456789",
            "EquipmentModel": "p3",
            "ProductionDate": "2016-04-26",
            "EquipmentType": 4,
            "Power": "3.3",
            "EquipmentName": "直流{0}号桩".format(str(i_station)),
            "ConnectorInfos": []
        }
        connector_info_type_4 = {
            "ConnectorID": "1100000{0}0201".format(str(i_station)),
            "ConnectorType": 4,
            "VoltageUpperLimits": 1220,
            "VoltageLowerLimits": 1220,
            "Current": 15,
            "NationalStandard": 1,
            "Power": 30.3
        }
        equipment_info_type_4["ConnectorInfos"].append(connector_info_type_4)
        station_info["EquipmentInfos"].append(equipment_info_type_4)
        station_info_list.append(station_info)
    return station_info_list
