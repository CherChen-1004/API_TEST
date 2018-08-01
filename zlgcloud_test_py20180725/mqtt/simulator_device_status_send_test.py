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
        user = UsersForTest(num=429, session=session)
        user.create_users(isagent=False)
        Auth = devices_for_test.get_auth()
        # device_schema = UsersForTest().get_device_schema().json()
        # for device_type in device_schema:
        #     status[device_type['type']] = []
        #     for s in device_type['status']:
        #         status[device_type['type']].append(s)

    def tearDown(self):
        global devices, TestData, user, Auth, status, device_schema
        user.login()
        user.delete_users()

def publish_device_status_test(device,payload):
    '''传入device，发布payload，然后登录API查看设备信息'''
    global user
    client = DeviceForTest().login_for_call(Auth=Auth,device=device)
    data = '\0'
    for key in payload:
        data = data + key + '\0' + str(payload[key]) + '\0'
    client.publish(topic=(STR_TOPIC_REPORT_STATUS % (device['devtype'],device['devid'])),payload=data,qos=QOS,retain=False)
    time.sleep(3)
    client.disconnect()
    client.loop_stop()
    user.login()
    r = user.get_device_info(device)
    if r.status_code == 200:
        result = r.json()
        delete_elements = ['devid','model','registertime','onlinetime','offlinetime','devtype','time','owner','devname','status','uri','jwt','resources']
        for element in delete_elements:
            del result[element]
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
        payload = {'clientip': "string", 'sw_version': 0, 'settings': 0}
        self.result = publish_device_status_test(device=devices[0],payload=payload)
        self.assertEqual(self.result,payload)
    def test_publish_device_status_devtype_candtu_right(self):
        '''devtype=candtu的设备上传状态'''
        payload = {'clientip': "string", 'DevStat': 0, 'CfgInfo': 0, 'SDStat': 0}
        self.result = publish_device_status_test(device=devices[2],payload=payload)
        self.assertEqual(self.result,payload)
    def test_publish_device_status_devtype_inverter_right(self):
        '''devtype=inverter的设备上传状态'''
        payload = {'safety_spec': 0, 'clientip': 'string', 'today_runtime': 0, 'sw_ver2': 0, 'total_runtime': 0, 'sw_ver1': 0}
        self.result = publish_device_status_test(device=devices[4],payload=payload)
        self.assertEqual(self.result,payload)
    def test_publish_device_status_devtype_collector_right(self):
        '''devtype=collector的设备上传状态'''
        payload = {'max_inverters': 0, 'sw_ver2': 0, 'communication': 'string', 'heart_beat_time': 0, 'hw_ver': 0, 'sw_ver1': 0, 'gw_addr': "string", 'sample_rate': 0, 'clientip': 'string', 'report_rate': 0, 'signal_strength': 0, 'mac_address': 'mac_address', 'kit_work_mode': "string", 'ip_addr': "string", 'dns_addr': "string", 'ap_kit_version': 0}
        self.result = publish_device_status_test(device=devices[6],payload=payload)
        self.assertEqual(self.result,payload)
    def test_publish_device_status_devtype_temperature_right(self):
        '''devtype=temperature的设备上传状态'''
        payload = {'clientip': 'string', 'sw_version': 0}
        self.result = publish_device_status_test(device=devices[8],payload=payload)
         self.assertEqual(self.result,payload)
    def test_publish_device_status_devtype_demo_wrong_key(self):
        '''devtype=demo的设备上传状态的message中包含错误的key'''
        payload_1 = {'clientip': "string1", 'sw_version': 234, 'settings': 45}
        payload_2 = {'clientip': "string1", 'sw_version': 234, 'settings': 45,'wrong_key':45}
        result_1 = publish_device_status_test(device=devices[0],payload=payload_1)
        self.result = publish_device_status_test(device=devices[0],payload=payload_2)
        self.assertEqual(self.result,{'clientip': "string1", 'sw_version': 234, 'settings': 45})
    def test_publish_device_status_devtype_candtu_wrong_key(self):
        '''devtype=candtu的设备上传状态的message中包含错误的key'''
        payload_1 = {'clientip': "string34", 'DevStat': 34, 'CfgInfo': 54, 'SDStat': 4}
        payload_2 = {'clientip': "string34", 'DevStat': 34, 'CfgInfo': 54, 'SDStat': 4,'wrong_key':43}
        result_1 = publish_device_status_test(device=devices[2],payload=payload_1)
        self.result = publish_device_status_test(device=devices[2],payload=payload_2)
        self.assertEqual(self.result,payload_1)
    def test_publish_device_status_devtype_inverter_wrong_key(self):
        '''devtype=inverter的设备上传状态的message中包含错误的key'''
        payload_1 = {'safety_spec': 43, 'clientip': 'stringdgfdf', 'today_runtime': 345, 'sw_ver2': 345, 'total_runtime': 543, 'sw_ver1': 76}
        payload_2 = {'safety_spec': 43, 'clientip': 'stringdgfdf', 'today_runtime': 345, 'sw_ver2': 345, 'total_runtime': 543, 'sw_ver1': 76,'wrong_key':345}
        result_1 = publish_device_status_test(device=devices[4],payload=payload_1)
        self.result = publish_device_status_test(device=devices[4],payload=payload_2)
        self.assertEqual(self.result,payload_1)
    def test_publish_device_status_devtype_collector_wrong_key(self):
        '''devtype=collector的设备上传状态的message中包含错误的key'''
        payload_1 = {'max_inverters': 345, 'sw_ver2': 23, 'communication': 'string43534', 'heart_beat_time': 45, 'hw_ver': 45, 'sw_ver1': 234, 'gw_addr': "string3456dfgt", 'sample_rate': 45, 'clientip': 'stridtsdfng', 'report_rate': 45, 'signal_strength': 324, 'mac_address': 'mac_address', 'kit_work_mode': "dsgfsdf", 'ip_addr': "string", 'dns_addr': "string", 'ap_kit_version': 0}
        payload_2 = {'wrong_key':'345sdf','max_inverters': 345, 'sw_ver2': 23, 'communication': 'string43534', 'heart_beat_time': 45, 'hw_ver': 45, 'sw_ver1': 234, 'gw_addr': "string3456dfgt", 'sample_rate': 45, 'clientip': 'stridtsdfng', 'report_rate': 45, 'signal_strength': 324, 'mac_address': 'mac_address', 'kit_work_mode': "dsgfsdf", 'ip_addr': "string", 'dns_addr': "string", 'ap_kit_version': 0}
        result_1 = publish_device_status_test(device=devices[6],payload=payload_1)
        self.result= publish_device_status_test(device=devices[6],payload=payload_2)
        self.assertEqual(self.result,payload_1)
    def test_publish_device_status_devtype_temperature_wrong_key(self):
        '''devtype=temperature的设备上传状态的message中包含错误的key'''
        payload_1 = {'clientip': 'string', 'sw_version': 0}
        payload_2 = {'clientip': 'string', 'sw_version': 0}
        result_1 = publish_device_status_test(device=devices[8],payload=payload_1)
        self.result = publish_device_status_test(device=devices[8],payload=payload_2)
        self.assertEqual(self.result,payload_1)
if __name__ == '__main__':
    unittest.main(verbosity=2)