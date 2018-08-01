#coding=utf_8
#Date=2018-4-9

import unittest
import requests
import json
import time
import paho.mqtt.client as mqtt
from db_fixture.mqtt_topic import *
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.device_for_test import DeviceForTest,devtype_model_dict,status
from db_fixture import test_data
from db_fixture.test_data import test_data_path
# devices = [{'devtype': 'demo', 'devid': 'demo_gentleman_1'}]
devices = [{'devtype': 'candtu', 'devid': 'candtu_gentleman_1'},
           {'devtype': 'inverter', 'devid': 'inverter_gentleman_1'},
           {'devtype': 'collector', 'devid': 'collector_gentleman_1'},
           {'devtype': 'temperature', 'devid': 'temperature_gentleman_1'},
           {'devtype': 'candtu', 'devid': 'candtu_gentleman_2'},
           {'devtype': 'inverter', 'devid': 'inverter_gentleman_2'},
           {'devtype': 'collector', 'devid': 'collector_gentleman_2'},
           {'devtype': 'temperature', 'devid': 'temperature_gentleman_2'}]
users = None
first_user_num,second_user_num = 96,97
devtype_commands_dict = {'candtu': ['CfgReq', 'Cfg', 'CfgUpdate', 'StartRec', 'StopRec', 'ClrDev', 'GetRecInfo', 'GetRecTypeInfo', 'GetRecData', 'CancelGetRec', 'GetLog', 'CancelGetLog', 'sync_time', 'upgrade', 'req_report', 'pass_through'],
                         'inverter': ['set', 'sync_time', 'upgrade', 'req_report', 'pass_through'],
                         'demo': ['set_report_interval', 'sync_time', 'upgrade', 'req_report', 'pass_through'],
                         'collector': ['sync_time', 'upgrade', 'req_report', 'pass_through'],
                         'temperature': ['set_report_interval', 'sync_time', 'upgrade', 'req_report', 'pass_through']}
devtype_commands_args_dict = {'candtu': {'commands': {'GetRecData': {'args': {'StopTime': 123, 'RecType': 123, 'StartTime': 123}},
                                                      'StopRec': {'args': {}},
                                                      'sync_time': {'args': {'time': 123}},
                                                      'CfgReq': {'args': {}},
                                                      'notify_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}},
                                                      'CancelGetRec': {'args': {'RecType': 123}},
                                                      'Cfg': {'args': {'CfgInfo': 'abc'}},
                                                      'exec_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}},
                                                      'req_report': {'args': {}},
                                                      'pass_through': {'args': {'raw': 'abc'}},
                                                      'DevNameUpdate': {'args': {'devname': 'abc'}},
                                                      'CfgUpdate': {'args': {}},
                                                      'GetRecTypeInfo': {'args': {'StopTime': 123, 'RecType': 123, 'StartTime': 123}},
                                                      'StartRec': {'args': {}},
                                                      'ClrDev': {'args': {}},
                                                      'GetRecInfo': {'args': {'RecType': 123}}}},
                              'collector': {'commands': {'exec_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}},
                                                         'sync_time': {'args': {'time': 123}},
                                                         'notify_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}},
                                                         'pass_through': {'args': {'raw': 'abc'}},
                                                         'req_report': {'args': {}}}},
                              'temperature': {'commands': {'exec_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}},
                                                           'req_report': {'args': {}},
                                                           'pass_through': {'args': {'raw': 'abc'}},
                                                           'set_report_interval': {'args': {'value': 123}},
                                                           'sync_time': {'args': {'time': 123}},
                                                           'notify_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}}}},
                              'demo': {'commands': {'exec_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}},
                                                    'req_report': {'args': {}},
                                                    'pass_through': {'args': {'raw': 'abc'}},
                                                    'set_report_interval': {'args': {'value': 123}},
                                                    'sync_time': {'args': {'time': 123}},
                                                    'notify_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}}}},

                              'inverter': {'commands': {'exec_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}},
                                                        'req_report': {'args': {}},
                                                        'set': {'args': {'value': 'abc', 'name': 'abc'}},
                                                        'pass_through': {'args': {'raw': 'abc'}},
                                                        'sync_time': {'args': {'time': 123}},
                                                        'notify_upgrade': {'args': {'model': 'abc', 'version': 'abc', 'url': 'abc'}}}}}

# devtype_commands_args_dict = {'candtu': {'commands': {'pass_through': {'args': {'raw': 'abc'}},
#                                                       'Cfg': {'args': {'CfgInfo': 'abc'}},
#                                                       'DevNameUpdate': {'args': {'devname': 'abc'}},
#                                                       'StopRec': {'args': {}},
#                                                       'StartRec': {'args': {}},
#                                                       'ClrDev': {'args': {}},
#                                                       'sync_time': {'args': {'time': 123}},
#                                                       'CancelGetRec': {'args': {'RecType': 123}},
#                                                       'GetRecInfo': {'args': {'RecType': 123}},
#                                                       'notify_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                       'GetRecData': {'args': {'RecType': 123, 'StopTime': 123, 'StartTime': 123}},
#                                                       'CfgReq': {'args': {}},
#                                                       'FwUpdate': {'args': {}},
#                                                       'GetRecTypeInfo': {'args': {'RecType': 123, 'StopTime': 123, 'StartTime': 123}},
#                                                       'CfgUpdate': {'args': {}},
#                                                       'exec_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                       'req_report': {'args': {}}}},
#                               'temperature': {'commands': {'sync_time': {'args': {'time': 123}},
#                                                            'notify_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                            'exec_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                            'set_report_interval': {'args': {'value': 123}},
#                                                            'pass_through': {'args': {'raw': 'abc'}},
#                                                            'req_report': {'args': {}}}},
#                               'collector': {'commands': {'sync_time': {'args': {'time': 123}},
#                                                          'req_report': {'args': {}},
#                                                          'notify_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                          'pass_through': {'args': {'raw': 'abc'}},
#                                                          'exec_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}}}},
#                               'demo': {'commands': {'sync_time': {'args': {'time': 123}},
#                                                     'notify_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                     'exec_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                     'set_report_interval': {'args': {'value': 123}},
#                                                     'pass_through': {'args': {'raw': 'abc'}},
#                                                     'req_report': {'args': {}}}},
#                               'inverter': {'commands': {'sync_time': {'args': {'time': 123}},
#                                                         'notify_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                         'exec_upgrade': {'args': {'model': 'abc', 'url': 'abc', 'version': 'abc'}},
#                                                         'set': {'args': {'value': 'abc', 'name': 'abc'}},
#                                                         'pass_through': {'args': {'raw': 'abc'}},
#                                                         'req_report': {'args': {}}}}}

devtype_commands_args_dict_wrong = {'temperature': {'commands': {'req_report': {'args': {}},
                                                            'pass_through': {'args': {'raw': 234}},
                                                            'upgrade': {'args': {'version': 234, 'model': 234, 'url': 234}},
                                                            'sync_time': {'args': {'time': 'string'}},
                                                            'set_report_interval': {'args': {'value': 'string'}}}},
                               'collector': {'commands': {'req_report': {'args': {}},
                                                          'pass_through': {'args': {'raw': 234}},
                                                          'upgrade': {'args': {'version': 234, 'model': 234, 'url': 234}},
                                                          'sync_time': {'args': {'time': 'string'}}}},
                               'candtu': {'commands': {'GetRecInfo': {'args': {'RecType': 'string'}},
                                                       'CancelGetLog': {'args': {}},
                                                       'CfgReq': {'args': {'CfgInfo': 234}},
                                                       'GetRecTypeInfo': {'args': {'StopTime': 'string', 'RecType': 'string', 'StartTime': 'string'}},
                                                       'CfgUpdate': {'args': {}},
                                                       'StopRec': {'args': {}},
                                                       'GetRecData': {'args': {'StopTime': 'string', 'RecType': 'string', 'StartTime': 'string'}},
                                                       'upgrade': {'args': {'version': 234, 'model': 234, 'url': 234}},
                                                       'CancelGetRec': {'args': {'RecType': 'string'}},
                                                       'Cfg': {'args': {}},
                                                       'pass_through': {'args': {'raw': 234}},
                                                       'StartRec': {'args': {}},
                                                       'req_report': {'args': {}},
                                                       'sync_time': {'args': {'time': 'string'}},
                                                       'GetLog': {'args': {}}, 'ClrDev': {'args': {}}}},
                               'inverter': {'commands': {'req_report': {'args': {}},
                                                         'set': {'args': {'value': 234, 'name': 234}},
                                                         'upgrade': {'args': {'version': 234, 'model': 234, 'url': 234}},
                                                         'sync_time': {'args': {'time': 'string'}},
                                                         'pass_through': {'args': {'raw': 234}}}},
                               'demo': {'commands': {'req_report': {'args': {}},
                                                     'pass_through': {'args': {'raw': 234}},
                                                     'upgrade': {'args': {'version': 234, 'model': 234, 'url': 234}},
                                                     'sync_time': {'args': {'time': 'string'}},
                                                     'set_report_interval': {'args': {'value': 'string'}}}}}
def get_device_command_arr(devices=[]):
    '''获得devtype_commands_dict的字典，不做实际调用，只用于命令查看，每次更新服务器时单独调用查看'''
    admin = UsersForTest()
    admin.username = 'admin'
    admin.password = 'admin123'
    admin.login()
    device_command_dict = {}
    for device in devices[0:4]:
        result = admin.get_device_commands(device['devtype'],device['devid']).json()
        device_command_dict[device['devtype']] = [command['name'] for command in result]
    return device_command_dict

json_file = test_data.test_data_path + '/' + 'device_schema.json'
def get_command_args_dict_from_json(json_file):
    '''读取json文件，获得type-command-args-dict，用于发送命令正常测试,每次服务器更新时更新一次json文件，并执行一次该函数'''
    with open(file=json_file,mode='r',encoding='utf-8',errors='ignore') as f:
        content = f.read()
        content_json = json.loads(content)
        command_dict = {}
        for type in content_json:
            command_dict[type['type']] = {}
            command_dict[type['type']]['commands'] = type['commands']
            for command_piece in command_dict[type['type']]['commands']:
                del command_dict[type['type']]['commands'][command_piece]['comment']
                if 'args' in command_dict[type['type']]['commands'][command_piece]:
                    for arg in command_dict[type['type']]['commands'][command_piece]['args']:
                        if command_dict[type['type']]['commands'][command_piece]['args'][arg] == {}:
                            command_dict[type['type']]['commands'][command_piece]['args'][arg] = {}
                        else:
                            if command_dict[type['type']]['commands'][command_piece]['args'][arg]['type'] == 'number':
                                command_dict[type['type']]['commands'][command_piece]['args'][arg] = 123
                            else:
                                command_dict[type['type']]['commands'][command_piece]['args'][arg] = 'abc'
                else:
                    command_dict[type['type']]['commands'][command_piece] = {}
                    command_dict[type['type']]['commands'][command_piece]['args'] = {}
    return command_dict
class InitialForSendingCommand(object):
    def setUp(self):
        global devices, TestData, user, device_schema,first_user_num,second_user_num
        # devices_for_test = DeviceForTest(devices=devices)
        # devices_for_test.device_register()
        TestData = InitialData(first_user_num=first_user_num,last_user_num=second_user_num+1)
        users = TestData.create_users()
        user_1 = UsersForTest(num=first_user_num)
        user_2 = UsersForTest(num=second_user_num)
        user_1.login()
        groupid = user_1.create_device_group(payload={"groupname":"abcdefgh"}).json()['data']['groupid']
        for device in devices[0:5]:
            user_1.add_device(groupid=groupid,payload=device)
        # Auth = devices_for_test.get_auth()
    def tearDown(self):
        global TestData
        TestData.delete_all_users()
def sending_command_test(url,user_num,device,timeout='',cmd='',args={},login_or_not=1):
    '''发送命令道指定的设备测试用例入口，登录设备，通过API登录普通用户，在发送命令的API接口发送命令给指定设备，在设备端接收命令'''
    # global Auth
    if timeout == '':
        base_url = url + device['devid'] + '/commands/'+ cmd + '?devtype=' + device['devtype']
    else:
        base_url = url + device['devid'] + '/commands/'+ cmd + '?devtype=' + device['devtype'] + '&timeout=' + timeout
    print(base_url)
    session = requests.Session()
    DeviceTest = DeviceForTest(devices=[device])
    Auth = DeviceTest.get_auth()
    client =DeviceTest.login_for_call(Auth=Auth, device=device)
    print(Auth)
    user = UsersForTest(num=user_num,session=session)
    if login_or_not == 1:
        user.login()
        r = session.put(url=base_url,json=args)
    elif login_or_not == 0:
        r = requests.put(url=base_url,json=args)
    else:
        user.login()
        user.logout()
        r = session.put(url=base_url, json=args)
    client.publish(topic=(STR_TOPIC_OFFLINE % (device['devtype'], device['devid'])), qos=QOS)
    client.disconnect()
    client.loop_stop()
    print(r.json())
    return r.status_code

class SendingCommandTest(unittest.TestCase):
    '''模拟设备发送状态测试'''
    @classmethod
    def setUpClass(cls):
        print('---------Start-----------')
        InitialForSendingCommand().setUp()
    @classmethod
    def tearDownClass(cls):
        InitialForSendingCommand().tearDown()
        print('----------End-------------')
    def setUp(self):
        self.base_url = 'https://zlab.zlgcloud.com/v1/devices/'
        print('action')
    def tearDown(self):
        print(self.result)
    # def test_send_command_demo_right(self):
    #     '''循环发送demo设备所支持的命令和附带正确的参数'''
    #     for command in devtype_commands_args_dict['demo']['commands']:
    #         with self.subTest():
    #             self.result = sending_command_test(url=self.base_url,user_num=first_user_num,device={'devtype': 'demo', 'devid': 'demo_gentleman_1'},timeout='',cmd=command,args=devtype_commands_args_dict['demo']['commands'][command]['args'])
    #             print(self.result)
    #             self.assertEqual(self.result,200)
    def test_send_command_candtu_right(self):
        '''循环发送candtu设备所支持的命令和附带正确的参数'''
        for command in devtype_commands_args_dict['candtu']['commands']:
            with self.subTest():
                self.result = sending_command_test(url=self.base_url,user_num=first_user_num,device={'devtype': 'candtu', 'devid': 'candtu_gentleman_1'},timeout='',cmd=command,args=devtype_commands_args_dict['candtu']['commands'][command]['args'])
                print(self.result)
                print(command)
                self.assertEqual(self.result,200)
    def test_send_command_inverter_right(self):
        '''循环发送inverter设备所支持的命令和附带正确的参数'''
        for command in devtype_commands_args_dict['inverter']['commands']:
            with self.subTest():
                self.result = sending_command_test(url=self.base_url,user_num=first_user_num,device={'devtype': 'inverter', 'devid': 'inverter_gentleman_1'},timeout='',cmd=command,args=devtype_commands_args_dict['inverter']['commands'][command]['args'])
                print(self.result)
                self.assertEqual(self.result,200)
    def test_send_command_collector_right(self):
        '''循环发送collector设备所支持的命令和附带正确的参数'''
        for command in devtype_commands_args_dict['collector']['commands']:
            with self.subTest():
                self.result = sending_command_test(url=self.base_url,user_num=first_user_num,device={'devtype': 'collector', 'devid': 'collector_gentleman_1'},timeout='',cmd=command,args=devtype_commands_args_dict['collector']['commands'][command]['args'])
                print(self.result)
                self.assertEqual(self.result,200)
    def test_send_command_temperature_right(self):
        '''循环发送temperature设备所支持的命令和附带正确的参数'''
        for command in devtype_commands_args_dict['temperature']['commands']:
            with self.subTest():
                self.result = sending_command_test(url=self.base_url,user_num=first_user_num,device={'devtype': 'temperature', 'devid': 'temperature_gentleman_1'},timeout='',cmd=command,args=devtype_commands_args_dict['temperature']['commands'][command]['args'])
                print(self.result)
                self.assertEqual(self.result,200)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    #下面更新devtype_commands_args_dict
    # r = get_command_args_dict_from_json(test_data_path+'/device_schema.json')
    # print(r)