# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData

'''返回码如下：
            200 操作成功
            400	无效参数
            401 没有登录
            500 服务器内部错误'''

def update_device_events_status_test(url,login_user,eventid,payload,login_or_not=1):
    '''参数化编程，login_user：登录的账号，payload：传入的数据，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    base_url = url + eventid
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        r1 = user.login()
        r = session.put(base_url,json=payload)
    elif login_or_not == 0:
        r = requests.put(base_url,json=payload)
    else:
        user.login()
        user.logout()
        r = session.put(base_url,json=payload)
    if r.status_code == 200:
        return r.json()['data']['unread']
    else:
        return r.status_code

class DevicesEventsStatusUpdateTest(unittest.TestCase):  #####与开发确认数据的取值范围
    '''更新指定事件的状态 接口测试
    每条用例前提条件：创建两个普通用户，每个用户添加三条devid不等、time不等的设备事件'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/events/"
        self.TestData = InitialData(81,81,81,83)
        self.users_device_events_arr = self.TestData.users_device_events(3)
        self.user_0 = self.users_device_events_arr[0]
        self.user_1 = self.users_device_events_arr[1]

    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_device_events()
        self.TestData.delete_all_users()
    def test_update_event_status_True(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {"unread": True}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,1)
        self.assertEqual(self.result,True)
    def test_update_event_status_False(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {"unread": False}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,1)
        self.assertEqual(self.result,False)
    def test_update_event_status_time(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {'time':3565}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_event_status_devid(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {'devid':"sfsagergwertgw3etgdsf"}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_event_status_devtype(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {'devtype':"sfsagergwertgw3etgdsf"}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_event_status_eventtype(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {'eventtype':"error"}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,1)
        self.assertEqual(self.result,400)
    def test_update_event_status_eventid_ls_1(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {"unread": True}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'][:-1],payload,1)
        self.assertEqual(self.result,400)
    def test_update_event_status_eventid_of_other_user(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {"unread": True}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_1['device_events'][0]['eventid'],payload,1)
        self.assertEqual(self.result,404)
    def test_update_event_status_eventid_not_exist(self):
        '''登录普通用户，传入该用户包含的事件的eventid和unread=False'''
        payload = {"unread": True}
        self.result = update_device_events_status_test(self.base_url,self.user_0,"0a1a2d3e4e5g6d7s8e9f0f1f",payload,1)
        self.assertEqual(self.result,500)
    def test_update_event_status_not_login(self):
        '''不登陆，传入该用户包含的事件的eventid和unread=False'''
        payload = {"unread": True}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,0)
        self.assertEqual(self.result,401)
    def test_update_event_status_logout(self):
        '''登录后再退出，传入该用户包含的事件的eventid和unread=False'''
        payload = {"unread": True}
        self.result = update_device_events_status_test(self.base_url,self.user_0,self.user_0['device_events'][0]['eventid'],payload,2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    for n in range(81,83):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()