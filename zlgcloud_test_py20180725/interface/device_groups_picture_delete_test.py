#coding=utf-8
#Author = Cher Chan

import unittest
import requests
from db_fixture.test_data import UsersForTest,InitialData
from db_fixture import test_data

'''返回码如下：
            200  操作成功
            400  无效参数
            401  没有登录
            500  服务器错误'''
class InitialForDeviceGroupPicture(object):
    def __init__(self,first_user_num,last_user_num,index_max):
        self.first_user_num = first_user_num
        self.last_user_num = last_user_num
        self.index_max = index_max
        self.photo_path = test_data.test_data_path + "\\test_photos" + "/"
        self.TestData = InitialData(first_user_num=first_user_num,last_user_num=last_user_num+1)
    def setUp(self):
        self.users_device_groups_arr = self.TestData.create_users_device_groups(1)
        for user in self.users_device_groups_arr:
            user_self = UsersForTest(num=int(user['mobile'][-2:]))
            user_self.login()
            for device_group in user['device_groups']:
                for index in range(0,self.index_max+1):
                    file = open(self.photo_path + 'test_1.jpg', 'rb')
                    r = user_self.device_group_upload_picture(groupid=device_group['groupid'],index=str(index),file={'file': ('test_1.jpg', file, 'image/jpeg')})
                    file.close()
                    print('upload picture:'+ str(r.status_code))
        return self.users_device_groups_arr
    def tearDown(self):
        self.TestData.delete_all_pictures_of_device_group()
        self.TestData.delete_all_users()

def delete_device_group_picture_test(url,login_user,groupid,index,login_or_not=1):
    '''上传设备分组的图片API接口用例'''
    base_url = url + groupid + '/images?index=' + index
    session = requests.Session()
    user = UsersForTest(num=int(login_user['mobile'][-2:]),session=session)
    if login_or_not == 1:
        user.login()
        r = session.delete(url=base_url)
    elif login_or_not == 0:
        r = requests.delete(url=base_url)
    else:
        user.login()
        user.logout()
        r = session.delete(url=base_url)
    return r.status_code

class DeviceGroupDeletePictureTest(unittest.TestCase):
    '''删除设备分组图片测试'''
    @classmethod
    def setUpClass(cls):
        global Initial,TestData
        Initial = InitialForDeviceGroupPicture(first_user_num=62,last_user_num=63,index_max=4)
        TestData = Initial.setUp()
    @classmethod
    def tearDownClass(cls):
        global Initial
        Initial.tearDown()
    def setUp(self):
        global TestData
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups/"
        self.TestData = TestData

    def tearDown(self):
        print(self.result)
    def test_device_group_picture_groupid_right_index_0(self):
        '''登录用户，传入该用户包含的一个groupid少一位字符，index=0'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0')
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_23_index_0(self):
        '''登录用户，传入该用户包含的一个groupid少一位字符，index=0'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'][:-1],index='0')
        self.assertEqual(self.result,403)
    def test_device_group_picture_groupid_of_other_user_index_0(self):
        '''登录用户，传入该用户包含的一个groupid少一位字符，index=0'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[1]['device_groups'][0]['groupid'],index='0')
        self.assertEqual(self.result,403)
    def test_device_group_picture_groupid_wrong_index_0(self):
        '''登录用户，传入该用户包含的一个groupid少一位字符，index=0'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid='0d1g2d3r4c5e6e7g8g9s0g1w',index='0')
        self.assertEqual(self.result,403)
    def test_device_group_picture_groupid_right_index_1(self):
        '''登录用户，传入该用户包含的一个groupid，index=1'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='1')
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_2(self):
        '''登录用户，传入该用户包含的一个groupid，index=2'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='2')
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_3(self):
        '''登录用户，传入该用户包含的一个groupid，index=3'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='3')
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_4(self):
        '''登录用户，传入该用户包含的一个groupid，index=4'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='4')
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_5(self):
        '''登录用户，传入该用户包含的一个groupid，index=5'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='5')
        self.assertEqual(self.result,404)
    def test_device_group_picture_groupid_right_index_6(self):
        '''登录用户，传入该用户包含的一个groupid，index=6'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='6')
        self.assertEqual(self.result,400)
    def test_device_group_picture_groupid_right_index_0_not_login(self):
        '''不登陆，传入该用户包含的一个groupid，index=0'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',login_or_not=0)
        self.assertEqual(self.result,401)
    def test_device_group_picture_groupid_right_index_0_logout(self):
        '''登录后退出，传入该用户包含的一个groupid'''
        self.result = delete_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',login_or_not=2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()
    # for n in range(384,388):
    #     user = UsersForTest(num=n,session=requests.Session())
    #     user.login()
    #     user.delete_users()