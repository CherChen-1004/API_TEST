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

def update_device_events_test(url,login_user,filter,payload,login_or_not=1):
    '''参数化编程，login_user：登录的账号，payload：传入的数据，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    if filter == "":
        base_url = url
    else:
        base_url = url + '?' + filter
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.put(base_url,json=payload)
    elif login_or_not == 0:
        r = requests.put(base_url,json=payload)
    else:
        user.login()
        user.logout()
        r = session.put(base_url,json=payload)
    if r.status_code == 200:
        return r.json()['data']
    else:
        return r.status_code

class DevicesEventsUpdateTest(unittest.TestCase):  #####与开发确认数据的取值范围
    '''更新满足条件的设备事件 接口测试
    每条用例前提条件：创建两个普通用户，每个用户添加三条devid不等、time不等的设备事件'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com/v1/events"
        self.TestData = InitialData(88,88,88,90)
        self.users_device_events_arr = self.TestData.users_device_events(3)
        self.user_0 = self.users_device_events_arr[0]
        self.user_1 = self.users_device_events_arr[1]

    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_device_events()
        self.TestData.delete_all_users()
    def test_update_device_events_filter_null_unread_true_to_false(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入unread=false'''
        payload = {"unread": False}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,{"n": 3,"nModified": 3,"ok": 1})
    def test_update_device_events_filter_null_unread_false_to_true(self):
        '''登录普通用户，filter传入为空，原始状态设为false，info传入unread=true'''
        payload1 = {"unread": False}
        payload = {"unread": True}
        r1 = update_device_events_test(self.base_url,self.user_0,"",payload1,1)
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload)
        self.assertEqual(self.result,{"n": 3,"nModified": 3,"ok": 1})
    def test_update_device_events_filter_null_unread_true_to_true(self):
        '''登录普通用户，filter传入为空，原始状态设为true，info传入unread=true'''
        payload = {"unread": True}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,{"n": 3,"nModified": 0,"ok": 1})
    def test_update_device_events_filter_null_name_wrong(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入错误的name'''
        payload = { "name": "abc"}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_name_for_wrong_type(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入name对应错误的事件类型'''
        payload = { "name": "temperature_too_high"}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_time(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入错误的time'''
        payload = { "time": 45675788}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_eventtype_wrong(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入错误的eventtype'''
        payload = { "eventtype": 'dsfsdg'}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_eventtype_for_wrong_type(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入eventtype对应错误的事件类型'''
        payload = { "eventtype": "error"}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_devtype_wrong(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入错误的devtype'''
        payload = { "devtype": 'dsfsdg'}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_devid_not_exist(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入错误的devid'''
        payload = { "devid": 'dsfsdg'}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_devid_of_other_user(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入其他用户包含的设备的devid'''
        session = requests.Session()
        user = UsersForTest(int(self.user_1['mobile'][-2:]),session)
        user.login()
        group = user.create_device_group({"groupname":"device_events_update"})
        # print(group.json())
        if group.status_code == 201:
            groupid = group.json()['data']['groupid']
            r1 = user.add_device(groupid,{"devid":"test_3","devtype":"inverter"})
            payload = {"devid":"test_3"}
            self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
            user.login()
            r2 = user.delete_device_groups(groupid)
            # print(r2.json())
        else:
            self.result = False
        self.assertEqual(self.result,400)

    def test_update_device_events_filter_null_uri(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入其他用户的username'''
        payload = { "uri": 'sagrgter'}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_eventid(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入其他用户的username'''
        payload = { "eventid": 'sdgfew4gtsdfg'}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_name(self):
        '''登录普通用户，filter传入name=该用户包含的一个设备事件的name'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%22" + self.user_0['device_events'][0]['name'] + "",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_name_ls_1(self):
        '''登录普通用户，filter传入name=该用户包含的一个设备事件的name少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%22" + self.user_0['device_events'][0]['name'][:-1] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 0, 'nModified': 0})
    def test_update_device_events_filter_time(self):
        '''登录普通用户，filter传入time=该用户包含的一个设备事件的time'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A" + str(self.user_0['device_events'][0]['time']) + "%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 1, 'nModified': 1})
    def test_update_device_events_filter_time_ls_1(self):
        '''登录普通用户，filter传入time=该用户包含的一个设备事件的time少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A" + str(self.user_0['device_events'][0]['time'])[:-1] + "%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 0, 'nModified': 0})
    def test_update_device_events_filter_eventtype(self):
        '''登录普通用户，filter传入eventtype=该用户包含的一个设备事件的eventtype'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%22" + self.user_0['device_events'][0]['eventtype'] + "%22%7D",payload,1)
        self.assertEqual(self.result,{"n": 2,"nModified": 2,"ok": 1})
    def test_update_device_events_filter_eventtype_ls_1(self):
        '''登录普通用户，filter传入eventtype=该用户包含的一个设备事件的eventtype少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%22" + self.user_0['device_events'][0]['eventtype'][:-1] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 0, 'nModified': 0})
    def test_update_device_events_filter_devtype(self):
        '''登录普通用户，filter传入devtype=该用户包含的一个设备事件的devtype'''
        payload = { "unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%22" + self.user_0['device_events'][0]['devtype'] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 3, 'nModified': 3})
    def test_update_device_events_filter_devtype_ls_1(self):
        '''登录普通用户，filter传入devtype=该用户包含的一个设备事件的devtype少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%22" + self.user_0['device_events'][0]['devtype'][:-1] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'nModified': 0, 'n': 0})
    def test_update_device_events_filter_devid(self):
        '''登录普通用户，filter传入devid=该用户包含的一个设备事件的devid'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%22" + self.user_0['device_events'][0]['devid'] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 1, 'nModified': 1})
    def test_update_device_events_filter_devid_ls_1(self):
        '''登录普通用户，filter传入devid=该用户包含的一个设备事件的devid少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%22" + self.user_0['device_events'][0]['devid'][:-1] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 0, 'nModified': 0})
    def test_update_device_events_filter_owner(self):
        '''登录普通用户，filter传入owner=该用户包含的一个设备事件的owner'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%22" + self.user_0['device_events'][0]['owner'] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 3, 'nModified': 3})
    def test_update_device_events_filter_owner_ls_1(self):
        '''登录普通用户，filter传入owner=该用户包含的一个设备事件的owner少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%22" + self.user_0['device_events'][0]['owner'][:-1] + "%22%7D",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_unread(self):
        '''登录普通用户，filter传入unread=该用户包含的一个设备事件的unread'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%20%22unread%22%3A" + 'true' + "%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 3, 'nModified': 3})
    def test_update_device_events_filter_unread_ls_1(self):
        '''登录普通用户，filter传入unread=该用户包含的一个设备事件的unread少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%20%22unread%22%3A" + 'tru' + "%7D",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_eventid(self):
        '''登录普通用户，filter传入eventid=该用户包含的一个设备事件的eventid'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%22" + self.user_0['device_events'][0]['eventid'] + "%22%7D",payload,1)
        self.assertEqual(self.result,{'ok': 1, 'n': 1, 'nModified': 1})
    def test_update_device_events_filter_eventid_ls_1(self):
        '''登录普通用户，filter传入eventid=该用户包含的一个设备事件的eventid少一位字符'''
        payload = {"unread":False}
        self.result = update_device_events_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%22" + self.user_0['device_events'][0]['eventid'][:-1] + "%22%7D",payload,1)
        self.assertEqual(self.result,500)
    def test_update_device_events_filter_null_unread_and_time(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入unread=false'''
        payload = {"unread": False,"time":34534}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_unread_and_devid(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入unread=false'''
        payload = {"unread": False,"devid":"sfsagergwertgw3etgdsf"}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_unread_and_devtype(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入unread=false'''
        payload = {"unread": False,"deytype":"sfsagergwertgw3etgdsf"}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
    def test_update_device_events_filter_null_unread_and_eventtype(self):
        '''登录普通用户，filter传入为空，原始状态设为True，info传入unread=false'''
        payload = {"unread": False,"eventtype":"error"}
        self.result = update_device_events_test(self.base_url,self.user_0,"",payload,1)
        self.assertEqual(self.result,400)
if __name__ == '__main__':
    for n in range(89,91):
        user = UsersForTest(n)
        user.login()
        user.delete_users()
    unittest.main()

