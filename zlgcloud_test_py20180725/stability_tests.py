# import time, sys
# sys.path.append('./interface')
# sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest
from db_fixture import test_data

# 指定测试用例为当前文件夹下的 interface 目录
# test_dir = './interface'
# discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')


# if __name__ == "__main__":
#     test_data.init_data() # 初始化接口测试数据
#
#     now = time.strftime("%Y-%m-%d %H_%M_%S")
#     filename = './report/' + now + '_result.html'
#     fp = open(filename, 'wb')
#     runner = HTMLTestRunner(stream=fp,
#                             verbosity=2,
#                             title='Guest Manage System Interface Test Report',
#                             description='Implementation Example with: ')
#     runner.run(discover)
#     fp.close()


import unittest
import time
from db_fixture import test_data
# test_dir = './interface'
# discover = unittest.defaultTestLoader.discover(test_dir,pattern='*_test.py')
init_time = time.time() #开始测试时间
days = 2 #运行天数
test_time = days*24*3600
def stability_test():
    test_dir = './interface'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')
    runner = unittest.TextTestRunner()
    runner.run(discover)
if __name__ == '__main__':
    while((time.time() - init_time) < test_time):
        test_data.init_data()
        stability_test()
    print('Test end.')
