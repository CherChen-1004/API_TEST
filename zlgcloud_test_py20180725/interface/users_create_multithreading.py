# coding=utf_8
# Author = CherChan
'''同时创建多个用户，采用多线程'''
import unittest
import requests
import json
import threading
from time import ctime, sleep
from db_fixture.test_data import UsersForTest
'''返回码如下：
            201 操作成功
            400 无效参数
            500 服务器内部错误'''

# 创建测试数据二维数组
test_data_file_name = 'test_data_99999.txt'  # 存放测试数据的txt文件   备注：需要将文件放在同一目录下
test_data_1D_arr_99999 = []
test_data_arr_99999 = []
n = 0
for line in open(test_data_file_name):
    test_data_1D_arr_99999.append(str(line)[0:-1])
    test_data_arr_99999.append(test_data_1D_arr_99999[n].split('\t'))
    n += 1

class GetSmscode(object):
    '''创建获取验证码函数'''
    def __init__(self, mobile, session):
        self.session = session
        self.mobile = mobile
    def get_smscode(self):
        r = self.session.get('https://zlab.zlgcloud.com:443/v1/auth/smscode?mobile=' + self.mobile)
        self.smscode = r.json()['message']
        return self.smscode

def create_users(num):
    session = requests.Session()
    base_url = 'https://zlab.zlgcloud.com:443/v1/users'
    mobile = test_data_arr_99999[num][0]
    username = test_data_arr_99999[num][1]
    password = test_data_arr_99999[num][2]
    smscode = GetSmscode(mobile, session).get_smscode()
    payload = {"username": username, "password": password, "mobile": mobile, "smscode": smscode}
    r = session.post(base_url, json=payload)
    # print(r.status_code)
    print('\n %d user created? %d' % (num,r.status_code))
    if r.status_code != 201:
        print('\n************ %d user created failed*********' % num)
    r2 = session.delete('https://zlab.zlgcloud.com:443/v1/users/' + username)
    print('\n %d user delete? %d' % (num,r2.status_code))

threads = []
for n in range(1000):
    num = n
    t = threading.Thread(target=create_users, args=(num,))
    threads.append(t)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print('All over ')