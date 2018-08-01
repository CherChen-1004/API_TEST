#coding=utf_8
import unittest
import requests
import time
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from db_fixture.mqtt_topic import *
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.device_for_test import DeviceForTest,devtype_model_dict
devices = [{'devtype':'inverter','devid':'pretty_girl_1'},
                   {'devtype':'collector','devid':'pretty_girl_2'},
                   {'devtype':'temperature','devid':'pretty_girl_3'},
                   {'devtype':'inverter','devid':'pretty_girl_4'},
                   {'devtype':'collector','devid':'pretty_girl_5'},
                   {'devtype':'temperature','devid':'pretty_girl_6'}]
users_for_firmware_test = []
user = None
Auth = {}


client = DeviceForTest()
def uploaddatatest(device,data,login_user_num=0):
    '''传入device，发布data，然后登录API查看数据'''
    client = DeviceForTest().login_for_call(Auth=Auth,device=device)
    client.publish(topic=(STR_TOPIC_REPORT_DATA % (device['devtype'],device['devid'])),payload=data,qos=QOS,retain=False)
    time.sleep(3)
    client.disconnect()
    client.loop_stop()
    session = requests.Session()
    user = UsersForTest(num=login_user_num,session=session)
    user.login()
    r = user.device_data_inquery(devtype=device['devtype'],devid=device['devid'])
    if r.status_code == 200:
        return r.json()['data']
    else:
        return r.status_code

class UploadDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global users_for_firmware_test,devices,TestData,user,Auth
        devices_for_test = DeviceForTest(devices=devices)
        # devices_for_test.device_register()
        session = requests.Session()
        user = UsersForTest(num=429,session=session)
        user.create_users(isagent=False)
        Auth = devices_for_test.get_auth()
    @classmethod
    def tearDownClass(cls):
        global users_for_firmware_test, devices, user
        user.login()
        # for device in devices:
        #     r1 = user.delete_device_data(devtype=device['devtype'],devid=device['devid'])
            # print(r1.json())
        user.delete_users()
    def tearDown(self):
        print(self.result)
    def test_upload_message_device_1(self):
        print('test1')
        self.result = uploaddatatest(device={'devtype':'inverter','devid':'12344321'},data='\0'+"pv1_volt" +'\0'+'215.2'+ '\0' + 'pv2_volt' +'\0' + '209'+'\0'+'pv3_volt'+ '\0' + '212'+'\0'+ '\0'+'pv1_curr'+'\0'+'8'+'\0',login_user_num=429)
        self.assertEqual(self.result, {"today_energy":0})
    # def test_2(self):
    #     print('test_2')


if __name__ == '__main__':
    unittest.main(verbosity=2)