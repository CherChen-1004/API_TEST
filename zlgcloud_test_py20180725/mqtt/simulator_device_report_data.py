#-*- coding: utf-8 -*-
#@Time  :2018/5/2411:15
#@Autor :CherChan
#@File  :simulator_device_report_data.py

#coding=utf_8
#Author=Cher Chan
#Date=2018-4-9
data = {
  "devices": [
    {
      "data": {
        "total_energy": {
          "max": 15000,
          "min": 10,
          "value": 3712.151855,
          "sign": 1
        },
        "power": {
          "max": 50,
          "min": 0,
          "value": 43.113449
        },
        "pv1_volt": {
          "max": 240,
          "min": 180,
          "value": 215.289337
        },
        "pv2_volt": {
          "max": 240,
          "min": 180,
          "value": 209.290283
        },
        "pv3_volt": {
          "max": 240,
          "min": 180,
          "value": 240
        },
        "pv1_curr": {
          "max": 10,
          "min": 0,
          "value": 8.308626
        },
        "pv2_curr": {
          "max": 10,
          "min": 0,
          "value": 7.544042
        },
        "pv3_curr": {
          "max": 10,
          "min": 0,
          "value": 4.571661
        },
        "l1_volt": {
          "max": 240,
          "min": 180,
          "value": 202.132202
        },
        "l1_curr": {
          "max": 10,
          "min": 0,
          "value": 4.033163
        },
        "l1_power": {
          "max": 50,
          "min": 0,
          "value": 22.893677
        },
        "l1_pf": {
          "max": 1,
          "min": 0,
          "value": 0.557055
        },
        "l1_dci": {
          "max": 10,
          "min": 0,
          "value": 5.91683
        },
        "l1_freq": {
          "max": 60,
          "min": 40,
          "value": 50.83102
        },
        "q_power": {
          "max": 50,
          "min": 0,
          "value": 15.364963
        },
        "pf": {
          "max": 1,
          "min": 0,
          "value": 0.929501
        },
        "temperature": {
          "max": 80,
          "min": 20,
          "value": 22.950752
        }
      },
      "id": "KIO022",
      "model": "XYZ",
      "type": "inverter"
    },
    {
      "data": {
        "total_energy": {
          "max": 15000,
          "min": 10,
          "value": 3715.875977,
          "sign": 1
        },
        "power": {
          "max": 50,
          "min": 0,
          "value": 4.040904
        },
        "pv1_volt": {
          "max": 240,
          "min": 180,
          "value": 237.396057
        },
        "pv2_volt": {
          "max": 240,
          "min": 180,
          "value": 223.690811
        },
        "pv3_volt": {
          "max": 240,
          "min": 180,
          "value": 187.547989
        },
        "pv1_curr": {
          "max": 10,
          "min": 0,
          "value": 7.15674
        },
        "pv2_curr": {
          "max": 10,
          "min": 0,
          "value": 3.269794
        },
        "pv3_curr": {
          "max": 10,
          "min": 0,
          "value": 8.997447
        },
        "l1_volt": {
          "max": 240,
          "min": 180,
          "value": 194.126541
        },
        "l1_curr": {
          "max": 10,
          "min": 0,
          "value": 2.198126
        },
        "l1_power": {
          "max": 50,
          "min": 0,
          "value": 14.620568
        },
        "l1_pf": {
          "max": 1,
          "min": 0,
          "value": 0.382423
        },
        "l1_dci": {
          "max": 10,
          "min": 0,
          "value": 5.430965
        },
        "l1_freq": {
          "max": 60,
          "min": 40,
          "value": 44.522514
        },
        "q_power": {
          "max": 50,
          "min": 0,
          "value": 47.993553
        },
        "pf": {
          "max": 1,
          "min": 0,
          "value": 0.645407
        },
        "temperature": {
          "max": 80,
          "min": 20,
          "value": 41.982113
        }
      },
      "id": "KIO023",
      "model": "XYZ",
      "type": "inverter"
    }
  ]
}
data_1 = {'data': {'total_energy': 3712.151855, 'l1_curr': 4.033163, 'q_power': 15.364963, 'power': 43.113449, 'pv2_volt': 209.290283, 'pv3_volt': 240, 'pv2_curr': 7.544042, 'temperature': 22.950752, 'pv1_volt': 215.289337, 'l1_power': 22.893677, 'pf': 0.929501, 'l1_dci': 5.91683, 'l1_volt': 202.132202, 'l1_pf': 0.557055, 'l1_freq': 50.83102, 'pv3_curr': 4.571661, 'pv1_curr': 8.308626}}
data_2 = {'data': {'total_energy': 3715.875977, 'l1_curr': 2.198126, 'q_power': 47.993553, 'power': 4.040904, 'pv2_volt': 223.690811, 'pv3_volt': 187.547989, 'pv2_curr': 3.269794, 'temperature': 41.982113, 'pv1_volt': 237.396057, 'l1_power': 14.620568, 'pf': 0.645407, 'l1_dci': 5.430965, 'l1_volt': 194.126541, 'l1_pf': 0.382423, 'l1_freq': 44.522514, 'pv3_curr': 8.997447, 'pv1_curr': 7.15674}}

devices = [{'devtype': 'demo', 'devid': 'demo_gentleman_1'},
           {'devtype': 'demo', 'devid': 'demo_gentleman_2'},
           {'devtype': 'candtu', 'devid': 'candtu_gentleman_1'},
           {'devtype': 'candtu', 'devid': 'candtu_gentleman_2'},
           {'devtype': 'inverter', 'devid': 'inverter_gentleman_1'},
           {'devtype': 'inverter', 'devid': 'inverter_gentleman_2'},
           {'devtype': 'collector', 'devid': 'collector_gentleman_1'},
           {'devtype': 'collector', 'devid': 'collector_gentleman_2'},
           {'devtype': 'temperature', 'devid': 'temperature_gentleman_1'},
           {'devtype': 'temperature', 'devid': 'temperature_gentleman_2'}]
status_dict = {'candtu': {'clientip': "string", 'DevStat': 0, 'CfgInfo': 0, 'SDStat': 0},
               'inverter': {'safety_spec': 0, 'clientip': 0, 'today_runtime': 0, 'sw_ver2': 0, 'total_runtime': 0, 'sw_ver1': 0},
               'temperature': {'clientip': 0, 'sw_version': 0},
               'demo': {'clientip': "string", 'sw_version': 0, 'settings': 0},
               'collector': {'max_inverters': 0, 'sw_ver2': 0, 'communication': 0, 'heart_beat_time': 0, 'hw_ver': 0, 'sw_ver1': 0, 'gw_addr': 0, 'sample_rate': 0, 'clientip': 0, 'report_rate': 0, 'signal_strength': 0, 'mac_address': 0, 'kit_work_mode': 0, 'ip_addr': 0, 'dns_addr': 0, 'ap_kit_version': 0}}
# data = {
#       "total_energy": 1000,
#       "today_energy": 1000,
#       "temperature": 35,
#       "gfci": 55,
#       "bus_volt": 66,
#       "power": 2000,
#       "q_power": 500,
#       "pf": 0.5,
#       "pv1_volt": 202,
#       "pv1_curr": 222,
#       "pv2_volt": 212,
#       "pv2_curr": 15,
#       "pv3_volt": 214,
#       "pv3_curr": 15,
#       "l1_volt": 212,
#       "l1_curr": 45,
#       "l1_freq": 45,
#       "l1_dci": 25,
#       "l1_power": 22,
#       "l1_pf": 0.5
#     }

#coding=utf_8
#Author=Cher Chan
#Date=2018-4-9

import unittest
import requests
import time
import paho.mqtt.client as mqtt
from db_fixture.mqtt_topic import *
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.device_for_test import DeviceForTest,devtype_model_dict,status
devices = [{'devtype': 'demo', 'devid': 'demo_gentleman_1'},
           {'devtype': 'demo', 'devid': 'demo_gentleman_2'},
           {'devtype': 'candtu', 'devid': 'candtu_gentleman_1'},
           {'devtype': 'candtu', 'devid': 'candtu_gentleman_2'},
           {'devtype': 'inverter', 'devid': 'inverter_gentleman_1'},
           {'devtype': 'inverter', 'devid': 'inverter_gentleman_2'},
           {'devtype': 'collector', 'devid': 'collector_gentleman_1'},
           {'devtype': 'collector', 'devid': 'collector_gentleman_2'},
           {'devtype': 'temperature', 'devid': 'temperature_gentleman_1'},
           {'devtype': 'temperature', 'devid': 'temperature_gentleman_2'}]
status_dict = {'candtu': {'clientip': "string", 'DevStat': 0, 'CfgInfo': 0, 'SDStat': 0},
               'inverter': {'safety_spec': 0, 'clientip': 0, 'today_runtime': 0, 'sw_ver2': 0, 'total_runtime': 0, 'sw_ver1': 0},
               'temperature': {'clientip': 0, 'sw_version': 0},
               'demo': {'clientip': "string", 'sw_version': 0, 'settings': 0},
               'collector': {'max_inverters': 0, 'sw_ver2': 0, 'communication': 0, 'heart_beat_time': 0, 'hw_ver': 0, 'sw_ver1': 0, 'gw_addr': 0, 'sample_rate': 0, 'clientip': 0, 'report_rate': 0, 'signal_strength': 0, 'mac_address': 0, 'kit_work_mode': 0, 'ip_addr': 0, 'dns_addr': 0, 'ap_kit_version': 0}}
class InitialForPublishingStatus(object):
    def setUp(self):
        global devices, TestData, user, Auth, device_schema
        devices_for_test = DeviceForTest(devices=devices)
        # devices_for_test.device_register()
        session = requests.Session()
        user = UsersForTest(num=0, session=session)
        user.username = '12399999987'
        user.password = '12399999987'
        user.mobile = '12399999987'
        user.email = '99999987@zlg.cn'
        user.create_users(isagent=False)
        Auth = devices_for_test.get_auth()
        # device_schema = UsersForTest().get_device_schema().json()
        # for device_type in device_schema:
        #     status[device_type['type']] = []
        #     for s in device_type['status']:
        #         status[device_type['type']].append(s)

    def tearDown(self):
        global devices, TestData, user, Auth, status, device_schema
        # user.login()
        # user.delete_users()

def publish_device_status_test(device,payload):
    '''传入device，发布payload，然后登录API查看设备信息'''
    global user
    client = DeviceForTest().login_for_call(Auth=Auth,device=device)
    user.login()
    # group = user.create_device_group(payload={"groupname":"plant_1","desc":"string"})
    # groupid = group.json()['data']['groupid']
    # user.add_device(groupid=groupid,payload=device)
    data = '\0'
    for key in payload:
        data = data + key + '\0' + str(payload[key]) + '\0'
    client.publish(topic=(STR_TOPIC_REPORT_DATA % (device['devtype'],device['devid'])),payload=data,qos=QOS,retain=False)
    time.sleep(1)
    client.publish(topic=(STR_TOPIC_OFFLINE % (device['devtype'], device['devid'])), qos=QOS)
    client.disconnect()
    client.loop_stop()
    user.login()
    r = user.device_data_inquery(devid=device['devid'],devtype=device['devtype'])
    if r.status_code == 200:
        result = r.json()
        # delete_elements = ['devid','model','registertime','onlinetime','offlinetime','devtype','time','owner','devname','status','uri','jwt','resources','agent']
        # for element in delete_elements:
        #     del result[element]
        return result
    else:
        return r.status_code
    
class UploadStatusTest(unittest.TestCase):
    '''模拟设备上传状态'''
    @classmethod
    def setUpClass(cls):
        InitialForPublishingStatus().setUp()
    @classmethod
    def tearDownClass(cls):
        InitialForPublishingStatus().tearDown()
    def setUp(self):
        global devices, TestData, user, Auth, status, device_schema
        self.status = status
    def tearDown(self):
        print(self.result)
    def test_publish_device_status_devtype_demo_right(self):
        '''devtype=demo的设备上传状态'''
        self.result = publish_device_status_test(device={'devtype': 'inverter', 'devid': 'inverter_gentleman_1'},payload=data_1['data'])
        self.result = publish_device_status_test(device={'devtype': 'inverter', 'devid': 'inverter_gentleman_1'},payload=data_2['data'])
        self.assertEqual(self.result,data_1)
    def


if __name__ == '__main__':
    unittest.main(verbosity=2)

    # for device in data['devices']:
    #     del device["id"]
    #     del device['model']
    #     del device['type']
    #     for item in device['data']:
    #         device['data'][item] = device['data'][item]['value']
    #     print(device)



# group = {
#   "plant_type": 0,
#   "net_type": 3,
#   "province": "广东",
#   "city": "广州",
#   "district": "天河",
#   "address": "黄州工业区",
#   "area": 50,
#   "max_power":3000,
#   "time_zone": 34,
#   "direction": 30,
#   "angle": 30,
#   "power_price_buy": 0.6,
#   "power_price_sale": 0.7,
#
#   "installer": "致远电子",
#   "operator": "致远电子",
#   "subsidy_national": 0.2,
#   "subsidy_national_duration": 555,
#   "subsidy_province": 0.1,
#   "subsidy_province_duration": 333,
#   "subsidy_city": 0.1,
#   "subsidy_city_duration": 111,
#   "cost": 100000,
#   "subsidy": 10000,
#   "loan_rate": 10,
#   "interest_rates": 0.01,
#   "loan_duration": 5,
#   "pay_type": 0,
#   "longitude": 20,
#   "latitude": 100
# }