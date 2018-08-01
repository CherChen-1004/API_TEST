# coding=utf_8
# Author=Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest
from db_fixture.test_data import InitialData
from db_fixture.test_data import device_event_test_data_arr

'''返回码如下：
            200 操作成功
            400	无效参数
            401 没有登录
            500 服务器内部错误'''
def delete_device_events_test(url,login_user,filter="",login_or_not=1):
    '''参数化编程，login_user:登录用户，filter：传入参数，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    if filter == "":
        base_url = url
    else:
        base_url = url + '?' + filter
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.delete(base_url)
    elif login_or_not == 0:
        r = requests.delete(base_url)
    else:
        user.login()
        user.logout()
        r = session.delete(base_url)
    if r.status_code == 200:
        return r.json()['data']['n']
    else:
        return r.status_code

class DevicesEventsDeleteTest(unittest.TestCase):  #####与开发确认数据的取值范围
    '''删除满足条件的设备事件 接口测试
    每条用例前提条件：创建两个普通用户，每个用户添加三条devid不等、time不等的设备事件'''
    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/events"
        self.TestData = InitialData(85,85,85,87)
        self.users_device_events_arr = self.TestData.users_device_events(3)
        self.user_0 = self.users_device_events_arr[0]
        self.user_1 = self.users_device_events_arr[1]
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_device_events()
        self.TestData.delete_all_users()
    def test_delete_device_event_null(self):
        '''登录普通用户，传入参数为空'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"",1)
        self.assertEqual(self.result,3)
    def test_delete_device_event_name_right(self):
        '''登录普通用户，传入该用户所包含的设备的name'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22name%22%3A%20%22" + self.user_0['device_events'][0]['name'] + "%22%7D",1)
        self.assertEqual(self.result,2)
    def test_delete_device_event_name_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的name少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22name%22%3A%20%22" + self.user_0['device_events'][0]['name'][:-1] + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_name_not_exist(self):
        '''登录普通用户，传入不存在的name'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22name%22%3A%20%22" + 'sgedhgdfg' + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_time_right(self):
        '''登录普通用户，传入该用户所包含的事件的time'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + str(self.user_0['device_events'][0]['time']) + "%7D",1)
        self.assertEqual(self.result,1)
    def test_delete_device_event_time_ls_1(self):
        '''登录普通用户，传入该用户所包含的时间的time少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + str(self.user_0['device_events'][0]['time'])[:-1] + "%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_time_wrong(self):
        '''登录普通用户，传入不存在的time'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + '46546516' + "%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_time_of_other_user(self):
        '''登录普通用户，传入其他用户包含事件的time'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + str(self.user_1['device_events'][0]['time']) + "%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_eventtype_right(self):
        '''登录普通用户，传入该用户所包含的设备的eventtype'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + self.user_0['device_events'][0]['eventtype'] + "%22%7D",1)
        self.assertEqual(self.result,2)
    def test_delete_device_event_eventtype_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的eventtype少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + self.user_0['device_events'][0]['eventtype'][:-1] + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_eventtype_not_exist(self):
        '''登录普通用户，传入不存在的eventtype'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + 'sgedhgdfg' + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_devtype_right(self):
        '''登录普通用户，传入该用户所包含的设备的devtype'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%20%22" + self.user_0['device_events'][0]['devtype'] + "%22%7D",1)
        self.assertEqual(self.result,3)
    def test_delete_device_event_devtype_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devtype少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%20%22" + self.user_0['device_events'][0]['devtype'][:-1] + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_devtype_not_exist(self):
        '''登录普通用户，传入不存在的devtype'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%20%22" + 'sgedhgdfg' + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_devid_right(self):
        '''登录普通用户，传入该用户所包含的设备的devid'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D",1)
        self.assertEqual(self.result,1)
    def test_delete_device_event_devid_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的devid少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'][:-1] + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_devid_not_exist(self):
        '''登录普通用户，传入不存在的devid'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + 'sgedhgdfg' + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_devid_of_other_user(self):
        '''登录普通用户，传入其他用户的devid'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_1['device_events'][0]['devid'] + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_owner_right(self):
        '''登录普通用户，传入该用户所包含的设备的owner'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D",1)
        self.assertEqual(self.result,3)
    def test_delete_device_event_owner_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的owner少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'][:-1] + "%22%7D",1)
        self.assertEqual(self.result,400)
    def test_delete_device_event_owner_not_exist(self):
        '''登录普通用户，传入不存在的owner'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + 'sgedhgdfg' + "%22%7D",1)
        self.assertEqual(self.result,400)
    def test_delete_device_event_owner_of_other_user(self):
        '''登录普通用户，传入其他用户的owner'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_1['device_events'][0]['owner'] + "%22%7D",1)
        self.assertEqual(self.result,400)
    def test_delete_device_event_unread_right(self):
        '''登录普通用户，传入该用户所包含的设备的unread'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22unread%22%3A%20" + 'true' + "%7D",1)
        self.assertEqual(self.result,3)
    def test_delete_device_event_unread_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的unread少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22unread%22%3A%20" + 'tru' + "%7D",1)
        self.assertEqual(self.result,400)
    def test_delete_device_event_unread_not_exist(self):
        '''登录普通用户，传入不存在的unread'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22unread%22%3A%20" + 'sgedhgdfg' + "%7D",1)
        self.assertEqual(self.result,400)
    def test_delete_device_event_eventid_right(self):
        '''登录普通用户，传入该用户所包含的设备的eventid'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + self.user_0['device_events'][0]['eventid'] + "%22%7D",1)
        self.assertEqual(self.result,1)
    def test_delete_device_event_eventid_ls_1(self):
        '''登录普通用户，传入该用户所包含设备的eventid少一位字符'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + self.user_0['device_events'][0]['eventid'][:-1] + "%22%7D",1)
        self.assertEqual(self.result,500)
    def test_delete_device_event_eventid_not_exist(self):
        '''登录普通用户，传入不存在的eventid'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + 'sgedhgdfg' + "%22%7D",1)
        self.assertEqual(self.result,500)
    def test_delete_device_event_eventid_of_other_user(self):
        '''登录普通用户，传入其他用户的eventid'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + self.user_1['device_events'][0]['eventid'] + "%22%7D",1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_eventtype_and_name_right(self):
        '''登录普通用户，传入该用户所包含的设备的eventtype和name'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + self.user_0['device_events'][0]['eventtype'] + "%22%2C%22name%22%3A%20%22" + self.user_0['device_events'][0]['name'] + "%22%7D" ,1)
        self.assertEqual(self.result,2)
    def test_delete_device_event_eventtype_and_name_wrong(self):
        '''登录普通用户，传入该用户所包含的设备的eventtype和其他用户的name'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + self.user_0['device_events'][0]['eventtype'] + "%22%2C%22name%22%3A%20%22" + self.user_1['device_events'][0]['name'] + "%22%7D" ,1)
        self.assertEqual(self.result,0)
    def test_delete_device_event_not_login(self):
        '''登录普通用户，传入该用户所包含的设备的name'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22name%22%3A%20%22" + self.user_0['device_events'][0]['name'] + "%22%7D",0)
        self.assertEqual(self.result,401)
    def test_delete_device_event_logout(self):
        '''登录普通用户，传入该用户所包含的设备的name'''
        self.result = delete_device_events_test(self.base_url,self.user_0,"filter=%7B%22name%22%3A%20%22" + self.user_0['device_events'][0]['name'] + "%22%7D",2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()