__author__ = "anyeV"

from django.conf.urls import url
from new_operator import new_operator_views

urlpatterns = [
    url(r'query_stations_info', new_operator_views.query_stations_info),
    url(r'query_equip_auth', new_operator_views.query_equip_auth),
    url(r'query_token', new_operator_views.query_token),
    url(r'query_equip_business_policy', new_operator_views.query_equip_business_policy),
    url(r'query_start_charge_with_phone_num', new_operator_views.query_start_charge_with_phone_num),
    url(r'notification_start_charge_result', new_operator_views.notification_start_charge_result,
        name='tld_start_charge_result'),
    url(r'query_equip_charge_status', new_operator_views.query_equip_charge_status),
    url(r'query_stop_charge', new_operator_views.query_stop_charge),
    url(r'notification_stop_charge_result', new_operator_views.notification_stop_charge_result),
    url(r'notification_charge_order_info', new_operator_views.notification_charge_order_info),
    url(r'notification_equip_charge_status', new_operator_views.notification_equip_charge_status),
    url(r'notification_stationStatus', new_operator_views.notification_stationStatus),
    url(r'get_token', new_operator_views.get_token),
    url(r'query_start_charge', new_operator_views.query_start_charge),
    url(r'query_station_status', new_operator_views.query_station_status),
    url(r'query_change_operator', new_operator_views.query_change_operator),
    url(r'query_change_config', new_operator_views.query_change_config),
    url(r'query_get_config', new_operator_views.query_get_config),
]
