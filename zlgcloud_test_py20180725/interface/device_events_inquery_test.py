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

def get_device_event_test(url,login_user,filter="",descend="",skip="",limit="",aggregation="",login_or_not=1):
    '''参数化编程，login_user：登录的账号，payload：传入的数据，login_or_not：1：登录，0：不登录，2：登录后再退出'''
    if (filter == "" and descend == "" and skip  == "" and limit == "" and aggregation == "") == True:
        base_url = url
    else:
        base_url = url+"?" + filter + descend + skip + limit + aggregation
    session = requests.Session()
    user = UsersForTest(int(login_user['mobile'][-2:]),session)
    if login_or_not == 1:
        user.login()
        r = session.get(base_url)
    elif login_or_not == 0:
        r = requests.get(base_url)
    else:
        user.login()
        user.logout()
        r = session.get(base_url)
    if r.status_code == 200:
        if aggregation != "":
            return r.json()['count']
        else:
            return r.json()['data']
    else:
        return r.status_code

class DevicesEventsInqueryTest(unittest.TestCase):  #####与开发确认数据的取值范围
    '''查询满足条件的设备事件 接口测试
    每条用例前提条件：创建两个普通用户，每个用户添加三条devid不等、time不等的设备事件'''

    def setUp(self):
        self.base_url = "https://zlab.zlgcloud.com:443/v1/events"
        self.TestData = InitialData(87,87,87,89)
        self.users_device_events_arr = self.TestData.users_device_events(3)
        self.user_0 = self.users_device_events_arr[0]
        self.user_1 = self.users_device_events_arr[1]
    def tearDown(self):
        print(self.result)
        self.TestData.delete_all_device_events()
        self.TestData.delete_all_users()
    def test_get_device_events_null(self):
        '''登录普通用户，传入参数为空'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_filter_time_right(self):
        '''登录普通用户，filter传入time=该用户包含的事件的time'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + str(self.user_0['device_events'][0]['time']) + "%7D","","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_time_ls_1(self):
        '''登录普通用户，filter传入time=该用户包含的事件的time少一位字符'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + str(self.user_0['device_events'][0]['time'])[:-1] + "%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_time_not_exist(self):
        '''登录普通用户，filter传入time=不存在的time'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + '454545845' + "%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_time_of_other_user(self):
        '''登录普通用户，filter传入time=其他用户包含的事件的time'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22time%22%3A%20" + str(self.user_1['device_events'][0]['time']) + "%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_eventtype_right(self):
        '''登录普通用户，filter传入eventtype=该用户包含的事件的eventtype'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + self.user_0['device_events'][1]['eventtype'] + "%22%7D","","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][1:2])
    def test_get_device_event_filter_eventtype_ls_1(self):
        '''登录普通用户，filter传入eventtype=该用户包含的事件的eventtype少一位字符'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + self.user_0['device_events'][0]['eventtype'][:-1] + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_eventtype_not_exist(self):
        '''登录普通用户，filter传入eventtype=不存在的eventtype'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventtype%22%3A%20%22" + 'sfgsgsdf' + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_devtype_right(self):
        '''登录普通用户，filter传入devtype=该用户包含的事件的devtype'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%20%22" + self.user_0['device_events'][0]['devtype'] + "%22%7D","","","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_filter_devtype_ls_1(self):
        '''登录普通用户，filter传入devtype=该用户包含的事件的devtype少一位字符'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%20%22" + self.user_0['device_events'][0]['devtype'][:-1] + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_devtype_not_exist(self):
        '''登录普通用户，filter传入devtype=不存在的devtype'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devtype%22%3A%20%22" + 'sgfdsgdfg' + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_devid_right(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_devid_ls_1(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid少一位字符'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'][:-1] + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_devid_not_exist(self):
        '''登录普通用户，filter传入devid=不存在的devid'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + 'sgfdsgdfg' + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_devid_of_other_user(self):
        '''登录普通用户，filter传入devid=其他用户包含的事件的devid'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_1['device_events'][0]['devid'] + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_owner_right(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_filter_owner_ls_1(self):  ##存在Bug
        '''登录普通用户，filter传入owner=该用户包含的事件的username少一位字符'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'][:-1] + "%22%7D","","","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_event_filter_owner_not_exist(self): ##存在Bug
        '''登录普通用户，filter传入owner=不存在的username'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + 'sgfdsgdfg' + "%22%7D","","","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_event_filter_owner_of_other_user(self): ##存在Bug
        '''登录普通用户，filter传入owner=其他用户包含的事件的username'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_1['username'] + "%22%7D","","","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_event_filter_unread_right(self):
        '''登录普通用户，filter传入unread=true'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22unread%22%3A%20" + 'true' + "%7D","","","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_filter_unread_false(self):
        '''登录普通用户，filter传入unread=false'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22unread%22%3A%20" + 'false' + "%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_unread_other_word(self):
        '''登录普通用户，filter传入unread=false'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22unread%22%3A%20" + 'sgsdf' + "%7D","","","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_event_filter_unread_true_ls_1(self):
        '''登录普通用户，filter传入unread=false'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22unread%22%3A%20" + 'tru' + "%7D","","","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_event_filter_eventid_right(self):
        '''登录普通用户，filter传入eventid=该用户包含的事件的eventid'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + self.user_0['device_events'][0]['eventid'] + "%22%7D","","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_eventid_ls_1(self):
        '''登录普通用户，filter传入eventid=该用户包含的事件的eventid少一位字符'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + self.user_0['device_events'][0]['eventid'][:-1] + "%22%7D","","","","",1)
        self.assertEqual(self.result,500)
    def test_get_device_event_filter_eventid_not_exist(self):
        '''登录普通用户，filter传入eventid=不存在的eventid'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + 'sgfdsgdfg' + "%22%7D","","","","",1)
        self.assertEqual(self.result,500)
    def test_get_device_event_filter_eventid_of_other_user(self):
        '''登录普通用户，filter传入eventid=其他用户包含的事件的eventid'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + self.user_1['device_events'][0]['eventid'] + "%22%7D","","","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_eventid_devid(self):
        '''登录普通用户，filter传入eventid=该用户包含的事件的eventid和devid'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22eventid%22%3A%20%22" + self.user_0['device_events'][0]['eventid'] + "%22%2C%22" + "devid" + '%22%3A%20%22' + self.user_0['device_events'][0]['devid'] + '%22%7D',"","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_descend_true(self):
        '''登录普通用户，filter传入eventid=其他用户包含的事件的eventid'''
        result = get_device_event_test(self.base_url,self.user_0,"","descend=true","","","",1)
        self.result = (result[0]['time'] >= result[1]['time'] >= result[2]['time'])
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_descend_false(self):
        '''登录普通用户，传入descend=true'''
        result = get_device_event_test(self.base_url,self.user_0,"","descend=false","","","",1)
        self.result = (result[0]['time'] <= result[1]['time'] <= result[2]['time'])
        self.assertEqual(self.result,True)
    def test_get_device_event_skip_0(self):
        '''登录普通用户，传入skip=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=0","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_skip_1(self):
        '''登录普通用户，传入skip=1'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=1","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_skip_2(self):
        '''登录普通用户，传入skip=2'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=2","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_3(self):
        '''登录普通用户，传入skip=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=3","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_skip_4(self):
        '''登录普通用户，传入skip=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=4","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_skip_illegal_character(self):
        '''登录普通用户，传入skip=非法字符串'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=dthtsdfg","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_event_limit_0(self):
        '''登录普通用户，传入limit=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","limit=0","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_limit_1(self):
        '''登录普通用户，传入limit=1'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","limit=1","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_limit_2(self):
        '''登录普通用户，传入limit=2'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","limit=2","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_limit_3(self):
        '''登录普通用户，传入limit=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","limit=3","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_limit_4(self):
        '''登录普通用户，传入limit=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","limit=4","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_limit_illegal_character(self):
        '''登录普通用户，传入limit=非法字符串'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","limit=dthtsdfg","","",1)
        self.assertEqual(self.result,400)
    def test_get_device_event_aggregation_count(self):
        '''登录普通用户，传入limit=2'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","","","aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_event_aggregation_count_ls_1(self):
        '''登录普通用户，传入limit=2'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","","","aggregation=coun",1)
        self.assertEqual(self.result,500)
    def test_get_device_event_filter_owner_and_descend_true(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username和descend=true'''
        result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=true","","","",1)
        self.result = (result[0]['time'] >= result[1]['time'] >= result[2]['time'])
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_owner_and_descend_false(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username和descend=true'''
        result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=false","","","",1)
        self.result = (result[0]['time'] <= result[1]['time'] <= result[2]['time'])
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_devid_and_descend_true(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid和descend=true'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","&descend=true","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_devid_and_descend_false(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid和descend=true'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","&descend=false","","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_devid_skip_0(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid和skip=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","","&skip=0","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_devid_skip_1(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid和skip=1'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","","&skip=1","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_owner_skip_0(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和skip=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&skip=0","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_filter_owner_skip_1(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和skip=1'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&skip=1","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_filter_owner_skip_2(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和skip=2'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&skip=2","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_filter_owner_skip_3(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和skip=2'''
        self.result =get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&skip=3","","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_filter_devid_limit_0(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid和limit=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","","&limit=0","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_devid_limit_1(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid和limit=1'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","","&limit=1","","",1)
        self.assertEqual(self.result,self.user_0['device_events'][0:1])
    def test_get_device_event_filter_owner_limit_0(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和limit=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&limit=0","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_filter_owner_limit_1(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和limit=1'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&limit=1","","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_filter_owner_limit_2(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和limit=2'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&limit=2","","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_filter_owner_limit_3(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的owner和limit=2'''
        self.result =get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['device_events'][0]['owner'] + "%22%7D","","&limit=3","","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_filter_devid_aggregation_count(self):
        '''登录普通用户，filter传入devid=该用户包含的事件的devid和aggregation=count'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22devid%22%3A%20%22" + self.user_0['device_events'][0]['devid'] + "%22%7D","","","","&aggregation=count",1)
        self.assertEqual(self.result,1)
    def test_get_device_event_descend_true_skip_0(self):
        '''登录普通用户，传入descend=true和skip=0'''
        result = get_device_event_test(self.base_url,self.user_0,"","descend=true","&skip=0","","",1)
        if len(result) == 3:
            self.result = (result[0]['time'] >= result[1]['time'] >= result[2]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_descend_true_skip_1(self):
        '''登录普通用户，传入descend=true和skip=0'''
        result = get_device_event_test(self.base_url,self.user_0,"","descend=true","&skip=1","","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] >= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_descend_true_limit_0(self):
        '''登录普通用户，传入descend=true和limit=0'''
        result = get_device_event_test(self.base_url,self.user_0,"","descend=true","&limit=0","","",1)
        if len(result) == 3:
            self.result = (result[0]['time'] >= result[1]['time'] >= result[2]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_descend_true_limit_2(self):
        '''登录普通用户，传入descend=true和limit=2'''
        result = get_device_event_test(self.base_url,self.user_0,"","descend=true","&limit=2","","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] >= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_descend_aggregation_count(self):
        '''登录普通用户，传入descend=true和aggregation=count'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","descend=true","","","&aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_event_skip_0_limit_0(self):
        '''登录普通用户，传入skip=0和limit=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=0","&limit=0","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_skip_0_limit_1(self):
        '''登录普通用户，传入skip=0和limit=1'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=0","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_0_limit_2(self):
        '''登录普通用户，传入skip=0和limit=2'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=0","&limit=2","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_skip_0_limit_3(self):
        '''登录普通用户，传入skip=0和limit=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=0","&limit=3","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_skip_0_limit_4(self):
        '''登录普通用户，传入skip=0和limit=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=0","&limit=4","",1)
        self.result.sort(key=str)
        self.user_0['device_events'].sort(key=str)
        self.assertEqual(self.result,self.user_0['device_events'])
    def test_get_device_event_skip_1_limit_0(self):
        '''登录普通用户，传入skip=1和limit=0'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=1","&limit=0","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_skip_1_limit_1(self):
        '''登录普通用户，传入skip=1和limit=1'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=1","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_1_limit_2(self):
        '''登录普通用户，传入skip=1和limit=2'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=1","&limit=2","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_skip_1_limit_3(self):
        '''登录普通用户，传入skip=1和limit=3'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=1","&limit=3","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_skip_1_limit_4(self):
        '''登录普通用户，传入skip=1和limit=3'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=1","&limit=4","",1))
        self.assertEqual(self.result,2)
    def test_get_device_event_skip_2_limit_0(self):
        '''登录普通用户，传入skip=2和limit=0'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=2","&limit=0","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_2_limit_1(self):
        '''登录普通用户，传入skip=2和limit=1'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=2","&limit=1","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_2_limit_2(self):
        '''登录普通用户，传入skip=2和limit=2'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=2","&limit=2","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_2_limit_3(self):
        '''登录普通用户，传入skip=2和limit=3'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=2","&limit=3","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_2_limit_4(self):
        '''登录普通用户，传入skip=2和limit=3'''
        self.result = len(get_device_event_test(self.base_url,self.user_0,"","","skip=2","&limit=4","",1))
        self.assertEqual(self.result,1)
    def test_get_device_event_skip_3_limit_0(self):
        '''登录普通用户，传入skip=3和limit=0'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=3","&limit=0","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_skip_3_limit_1(self):
        '''登录普通用户，传入skip=3和limit=1'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=3","&limit=1","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_skip_3_limit_2(self):
        '''登录普通用户，传入skip=3和limit=2'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=3","&limit=2","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_skip_3_limit_3(self):
        '''登录普通用户，传入skip=3和limit=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=3","&limit=3","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_skip_3_limit_4(self):
        '''登录普通用户，传入skip=3和limit=3'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=3","&limit=4","",1)
        self.assertEqual(self.result,[])
    def test_get_device_event_skip_2_aggregation_count(self):
        '''登录普通用户，传入skip=2和aggregation=count'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","skip=2","","&aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_event_limit_2_aggregation_count(self):
        '''登录普通用户，传入limit=2和aggregation=count'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","limit=2","","&aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_event_filter_owner_and_descend_true_skip_1(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username、descend=true和skip=1'''
        result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=true","&skip=1","","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] >= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_owner_and_descend_false_skip_1(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username、descend=false和skip=1'''
        result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=false","&skip=1","","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] <= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_owner_and_descend_true_limit_2(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username、descend=true和limit=2'''
        result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=true","&limit=2","","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] >= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_owner_and_descend_false_limit_2(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username、descend=false和limit=2'''
        result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=false","&limit=2","","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] <= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_owner_and_descend_false_aggregation_count(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username和descend=true'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=","","","&aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_event_descend_true_skip_1_limit_2(self):
        '''登录普通用户，传入descend=true、skip=2和limit=2'''
        result = get_device_event_test(self.base_url,self.user_0,"","descend=true","&skip=1","&limit=2","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] >= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_owner_and_descend_false_skip_1_limit_2(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username、descend=false和limit=2'''
        result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=false","&skip=1","&limit=2","",1)
        if len(result) == 2:
            self.result = (result[0]['time'] <= result[1]['time'])
        else:
            self.result = False
        self.assertEqual(self.result,True)
    def test_get_device_event_filter_owner_and_descend_false_skip_1_limit_2_aggregation_count(self):
        '''登录普通用户，filter传入owner=该用户包含的事件的username、descend=false和limit=2'''
        self.result = get_device_event_test(self.base_url,self.user_0,"filter=%7B%22owner%22%3A%20%22" + self.user_0['username'] + "%22%7D","&descend=false","&skip=1","&limit=2","&aggregation=count",1)
        self.assertEqual(self.result,3)
    def test_get_device_event_filter_not_login(self):
        '''不登录'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","","","",0)
        self.assertEqual(self.result,401)
    def test_get_device_event_filter_logout(self):
        '''登录后退出'''
        self.result = get_device_event_test(self.base_url,self.user_0,"","","","","",2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()

