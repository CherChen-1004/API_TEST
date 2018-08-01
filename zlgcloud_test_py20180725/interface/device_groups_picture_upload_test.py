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
    def __init__(self,first_user_num,last_user_num):
        self.first_user_num = first_user_num
        self.last_user_num = last_user_num
        self.TestData = InitialData(first_user_num=first_user_num,last_user_num=last_user_num+1)
    def setUp(self):
        self.users_device_groups_arr = self.TestData.create_users_device_groups(1)
        return self.users_device_groups_arr
    def tearDown(self):
        self.TestData.delete_all_pictures_of_device_group()
        self.TestData.delete_all_users()

def upload_device_group_picture_test(url,login_user,groupid,index,payload,login_or_not=1):
    '''上传设备分组的图片API接口用例'''
    base_url = url + groupid + '/images?index=' + index
    session = requests.Session()
    user = UsersForTest(num=int(login_user['mobile'][-2:]),session=session)
    if login_or_not == 1:
        user.login()
        r = session.post(url=base_url,files = payload)
    elif login_or_not == 0:
        r = requests.post(url=base_url,files= payload)
    else:
        user.login()
        user.logout()
        r = session.post(url=base_url,files = payload)
    return r.status_code

class DeviceGroupPictureTest(unittest.TestCase):
    '''上传设备分组图片测试'''
    @classmethod
    def setUpClass(cls):
        global Initial,TestData
        Initial = InitialForDeviceGroupPicture(first_user_num=63,last_user_num=64)
        TestData = Initial.setUp()
    @classmethod
    def tearDownClass(cls):
        global Initial
        Initial.tearDown()
    def setUp(self):
        global TestData
        self.base_url = "https://zlab.zlgcloud.com:443/v1/device_groups/"
        self.photo_path = test_data.test_data_path + "\\test_photos" + "/"
        self.TestData = TestData

    def tearDown(self):
        print(self.result)
    def test_device_group_picture_groupid_right_index_0_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=0，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_0_file_png_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=0，file=*.png，大小不超过200k'''
        payload = {'file': ('test_2.png', open(self.photo_path + 'test_2.png', 'rb'), 'image/png')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_0_file_PNG_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=0，file=*.PNG，大小不超过200k'''
        payload = {'file': ('test_3.PNG', open(self.photo_path + 'test_3.PNG', 'rb'), 'image/PNG')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_0_file_txt_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=0，file=*.PNG，大小不超过200k'''
        payload = {'file': open(self.photo_path + 'test.txt', 'rb')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',payload = payload)
        self.assertEqual(self.result,400)
    def test_device_group_picture_groupid_right_index_0_file_jpg_bigger_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=0，file=*.jpg，大小超过200k'''
        payload = {'file': ('test_4.jpg', open(self.photo_path + 'test_4.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',payload = payload)
        self.assertEqual(self.result,400)
    def test_device_group_picture_groupid_23_index_0_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid少一位字符，index=0，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'][:-1],index='0',payload = payload)
        self.assertEqual(self.result,403)
    def test_device_group_picture_groupid_of_other_user_index_0_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid少一位字符，index=0，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[1]['device_groups'][0]['groupid'],index='0',payload = payload)
        self.assertEqual(self.result,403)
    def test_device_group_picture_groupid_wrong_index_0_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid少一位字符，index=0，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid='0d1g2d3r4c5e6e7g8g9s0g1w',index='0',payload = payload)
        self.assertEqual(self.result,403)
    def test_device_group_picture_groupid_right_index_1_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=1，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='1',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_2_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=2，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='2',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_3_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=3，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='3',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_4_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=4，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='4',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_5_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=5，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='5',payload = payload)
        self.assertEqual(self.result,200)
    def test_device_group_picture_groupid_right_index_6_file_jpg_less_200(self):
        '''登录用户，传入该用户包含的一个groupid，index=6，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='6',payload = payload)
        self.assertEqual(self.result,400)
    def test_device_group_picture_groupid_right_index_0_file_jpg_200_not_login(self):
        '''不登陆，传入该用户包含的一个groupid，index=0，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',payload = payload,login_or_not=0)
        self.assertEqual(self.result,401)
    def test_device_group_picture_groupid_right_index_0_file_jpg_200_logout(self):
        '''登录后退出，传入该用户包含的一个groupid，index=0，file=*.jpg，大小不超过200k'''
        payload = {'file': ('test_1.jpg', open(self.photo_path + 'test_1.jpg', 'rb'), 'image/jpeg')}
        self.result = upload_device_group_picture_test(url=self.base_url,login_user=self.TestData[0],groupid=self.TestData[0]['device_groups'][0]['groupid'],index='0',payload = payload,login_or_not=2)
        self.assertEqual(self.result,401)
if __name__ == '__main__':
    unittest.main()
    # for n in range(383,385):
    #     user = UsersForTest(num=n,session=requests.Session())
    #     user.login()
    #     user.delete_users()