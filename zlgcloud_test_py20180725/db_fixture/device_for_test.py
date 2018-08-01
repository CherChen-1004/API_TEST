#coding=utf-8
#-*- coding:utf-8 -*-
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from db_fixture.mqtt_topic import *
import time
import requests
from db_fixture.test_data import UsersForTest

devtype_model_dict= {'inverter':'INV0001-ZLG','demo':'demo01','candtu':'CANDTU-200UWGR','collector':'WM6232PU','temperature':'temp01'}
status = {'temperature': ['clientip', 'sw_version'],
          'candtu': ['SDStat', 'DevStat', 'clientip', 'CfgInfo'],
          'collector': ['communication', 'hw_ver', 'ap_kit_version', 'kit_work_mode', 'ip_addr', 'clientip', 'gw_addr', 'report_rate', 'sw_ver1', 'heart_beat_time', 'dns_addr', 'sw_ver2', 'sample_rate', 'signal_strength', 'mac_address', 'max_inverters'],
          'inverter': ['sw_ver1', 'clientip', 'sw_ver2', 'total_runtime', 'safety_spec', 'today_runtime'], 'demo': ['settings', 'sw_version', 'clientip']}
status_dict = {'candtu': {'clientip': "string", 'DevStat': 0, 'CfgInfo': 0, 'SDStat': 0},
               'inverter': {'safety_spec': 0, 'clientip': 0, 'today_runtime': 0, 'sw_ver2': 0, 'total_runtime': 0, 'sw_ver1': 0},
               'temperature': {'clientip': 0, 'sw_version': 0},
               'demo': {'clientip': "string", 'sw_version': 0, 'settings': 0},
               'collector': {'max_inverters': 0, 'sw_ver2': 0, 'communication': 0, 'heart_beat_time': 0, 'hw_ver': 0, 'sw_ver1': 0, 'gw_addr': 0, 'sample_rate': 0, 'clientip': 0, 'report_rate': 0, 'signal_strength': 0, 'mac_address': 0, 'kit_work_mode': 0, 'ip_addr': 0, 'dns_addr': 0, 'ap_kit_version': 0}}
message_from_broker = None
class DeviceForTest(object):
    '''注册指定设备'''
    def __init__(self,devices=[]):
        self.devices = devices
        self.payload = {"username": "zlgdevice", "password": "demo+123=demo123","devices": self.devices}
        self.url = "https://zlab.zlgcloud.com:8143/v1/login"
    def get_auth(self):
        auth_result = {}
        r = requests.post(url=self.url,json=self.payload,verify=False)
        if r.status_code == 200:
            print(r.json())
            try:
                auth_result['host'] = r.json()['data']['mqtt']['host']
                auth_result['port'] = r.json()['data']['mqtt']['port']
                auth_result['username'] = r.json()['data']['clientip']
                auth_result['password'] = r.json()['data']['token']
                auth_result['client_id'] = r.json()['data']['clientip']
            except:
                auth_result['host'] = r.json()['data']['mqtt']['host']
                auth_result['port'] = r.json()['data']['mqtt']['sslport']
                auth_result['username'] = r.json()['data']['clientip']
                auth_result['password'] = r.json()['data']['token']
                auth_result['client_id'] = r.json()['data']['clientip']
            print('token',auth_result['password'])
        else:
            print('Get token failed!!!')
        return auth_result

    def on_publish(self,client, userdata, mid):
        print('----on pub ---')
        print('userdata:', userdata)
        print('mid:', mid)
        print('---end pub---')

    def on_message(self,client, userdata, msg):
        global message_from_broker
        message_from_broker = msg
        print('---on msg---')
        print('topic:%s' % msg.topic)
        print('payload: %s' % msg.payload)
        print('qos:%d' % msg.qos)
        print('--- end msg ---')
        if b'cmdid' in  msg.payload:
            payload_list = str(msg.payload,encoding='utf-8').split('\0')[1:][:-1]
            topic_list = msg.topic.split('/')[1:]
            device = {'devtype':topic_list[2],'devid':topic_list[3]}
            payload_dict = {}
            for n in range(int(len(payload_list) / 2)):
                payload_dict[payload_list[2 * n]] = payload_list[2 * n + 1]
            client.publish(topic=(STR_TOPIC_REPORT_RESULT % (device['devtype'], device['devid'])),
                           payload='\0' + 'cmdid' + '\0' + payload_dict['cmdid'] + '\0' + 'result' + '\0' + '1' + '\0' + 'msg' + '\0' + 'success' + '\0')
    def return_message_from_broker(self):
        global message_from_broker
        return message_from_broker
    def on_log(self,client, userdata, level, buf):
        if level == MQTT_LOG_INFO:
            head = 'INFO'
        elif level == MQTT_LOG_NOTICE:
            head = 'NOTICE'
        elif level == MQTT_LOG_ERR:
            head = 'ERR'
        elif level == MQTT_LOG_WARNING:
            head = 'WARN'
        elif level == MQTT_LOG_DEBUG:
            head = 'DEBUG'
        else:
            head = level
        print('%s: %s' % (head, buf))

    def on_connect(self,client, userdata, flag, rc):
        global STR_TOPIC_DEVICE, STR_TOPIC_BROADCAST, STR_TOPIC_BROADCAST_PREFIX, STR_TOPIC_BROADCAST_DEVTYPE, QOS
        print('---on connect ---')
        print('flag=', flag)
        print('connection re:',rc)
        if rc == 0:
            print('---ask sub ---')
            # for device in self.devices:
            #     s_rc = client.subscribe([(STR_TOPIC_DEVICE % (device['devtype'], device['devid']), QOS),
            #                              (STR_TOPIC_BROADCAST, QOS),
            #                              ((STR_TOPIC_BROADCAST_PREFIX + devtype_model_dict[device['devtype']]), QOS),
            #                              ((STR_TOPIC_BROADCAST_DEVTYPE % device['devtype']), QOS)])

            s_rc = client.subscribe(STR_TOPIC_BROADCAST, QOS)
            if s_rc[0] == 0:
                print('sub successed')
            else:
                print('sub failed')
            print('--- end ask sub ---')
        else:
            print('connect failed')
        print('--- end on connect ---')


    def on_subscibe(self,mq, userdata, mid, granted_qos):
        # global STR_TOPIC_DEVICE,STR_TOPIC_BROADCAST,STR_TOPIC_BROADCAST_PREFIX,STR_TOPIC_BROADCAST_DEVTYPE,QOS
        # global devices
        print('--- on sub ---')
        print('userdata:', userdata)
        print('mid: ', mid)
        print('granted_qos:', granted_qos)

    def callback_function(self,client, userdata, msg):
        print('--- callback ---')
        print('topic:%s' % msg.topic)
        print('payload: %s' % msg.payload)
        print('qos: %d' % msg.qos)
        terms = msg.payload.split(' ')
        if len(terms) > 0:
            term = terms[-1]
            print('term:%s' % term)
        print('--- callback end ---')
    def login_for_call(self,Auth,device):
        '''供给外部调用，且提供client接口，提供直接操作'''
        if Auth == {}:
            raise ValueError('Get Authentication Failed')
        else:
            print(Auth)
            username = Auth['username']
            password = Auth['password']
            host = Auth['host']
            port = Auth['port']
            clientID = Auth['client_id']
            client = mqtt.Client(client_id=clientID, userdata=None, protocol=mqtt.MQTTv31, clean_session=0)
            client.username_pw_set(username, password)
            client.on_publish = self.on_publish
            client.on_message = self.on_message
            client.on_log = self.on_log
            client.on_connect = self.on_connect
            client.on_subscribe = self.on_subscibe
            client.connect(host, port, 60)
            client.loop_start()
            info_register = client.publish(topic=(STR_TOPIC_REGISTER % (device['devtype'], device['devid'])),payload='\0model\0'+devtype_model_dict[device['devtype']]+'\0', qos=QOS)
            info_online = client.publish(topic=(STR_TOPIC_ONLINE % (device['devtype'], device['devid'])), payload='\0model\0'+devtype_model_dict[device['devtype']]+'\0',qos=QOS)
            # info_online.wait_for_publish()
            client.subscribe(STR_TOPIC_DEVICE % (device['devtype'], device['devid']), QOS)
            client.subscribe(STR_TOPIC_BROADCAST, QOS)
            client.subscribe(STR_TOPIC_BROADCAST_PREFIX + devtype_model_dict[device['devtype']], QOS)
            client.subscribe(STR_TOPIC_DEVICE % (device['devtype'], device['devid']), QOS)
            time.sleep(1)
            return client

    def login_self(self, waiting_for_ask=False,if_disconnect=True):
        '''登录：包括发布register和online的消息'''
        global STR_TOPIC_REGISTER, STR_TOPIC_ONLINE, STR_TOPIC_OFFLINE, QOS
        Auth = self.get_auth()
        if Auth == {}:
            raise ValueError('Get Authentication Failed')
        else:
            username = Auth['username']
            password = Auth['password']
            # print('password:',password)
            host = Auth['host']
            port = Auth['port']
            clientID = Auth['client_id']
            client = mqtt.Client(client_id=clientID, userdata=None, protocol=mqtt.MQTTv31, clean_session=0)
            client.username_pw_set(username, password)
            client.on_publish = self.on_publish
            client.on_message = self.on_message
            client.on_log = self.on_log
            client.on_connect = self.on_connect
            client.on_subscribe = self.on_subscibe
            client.connect(host, port, 60)
            client.loop_start()
            for device in self.devices:
                info_register = client.publish(topic=(STR_TOPIC_REGISTER % (device['devtype'], device['devid'])), payload='\0model\0'+devtype_model_dict[device['devtype']]+'\0',qos=QOS)
                info_online = client.publish(topic=(STR_TOPIC_ONLINE % (device['devtype'], device['devid'])),payload='\0model\0'+devtype_model_dict[device['devtype']]+'\0', qos=QOS)
                if waiting_for_ask == True:
                    info_online.wait_for_publish()
                time.sleep(2)
                client.publish(topic=(STR_TOPIC_OFFLINE % (device['devtype'], device['devid'])), qos=QOS)
            if if_disconnect == True:
                client.disconnect()
                print('connection stop')
                client.loop_stop()
    def device_register(self):
        self.login_self(waiting_for_ask=False,if_disconnect=True)
        self.login_self(waiting_for_ask=False,if_disconnect=True)

if __name__ == "__main__":
    # device_list = [{'devtype':"inverter","devid":'type'}]
    devices = [{'devtype': 'candtu', 'devid': 'candtu_gentleman_1'},
               {'devtype': 'inverter', 'devid': 'inverter_gentleman_1'},
               {'devtype': 'collector', 'devid': 'collector_gentleman_1'},
               {'devtype': 'temperature', 'devid': 'temperature_gentleman_1'},
               {'devtype': 'candtu', 'devid': 'candtu_gentleman_2'},
               {'devtype': 'inverter', 'devid': 'inverter_gentleman_2'},
               {'devtype': 'collector', 'devid': 'collector_gentleman_2'},
               {'devtype': 'temperature', 'devid': 'temperature_gentleman_2'}]
    device_list = [{'devtype':'inverter','devid':'api_test_inverter_'+str(n)} for n in range(50,100)]
    R = DeviceForTest(devices)
    R.device_register()
    # status_dict = {}
    # for key in status:
    #     a = {}
    #     for s in status[key]:
    #         a[s] = 0
    #     status_dict[key] = a
    # print(status_dict)
