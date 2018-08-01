# coding=utf_8
# Author = Cher Chan

import requests
import os

'''管理员账号：admin/admin123'''

# 创建已注册普通用户
test_data_path = "E:\\git\\zlgcloud\\zlgcloud_test_py20180725\\zlgcloud_test_py20180725\\db_fixture"
# 创建测试数据二维数组
def create_test_data(test_data_file_name):
    # test_data_file_name = 'test_data.txt' #存放测试数据的txt文件   备注：需要将文件放在同一目录下
    test_data_1D_arr = []
    test_data_arr = []
    n = 0
    f = open(test_data_path+'/'+ test_data_file_name)
    for line in f:
        test_data_1D_arr.append(str(line)[0:-1])
        test_data_arr.append(test_data_1D_arr[n].split('\t'))
        n += 1
    f.close()
    return test_data_arr

# a = create_test_data("test_data.txt")
test_data_arr = create_test_data('test_data.txt')
device_event_test_data_arr = create_test_data('device_event_test_data.txt')
models_list = ["demo01","demo02", "demo03","demo04","CANDTU-200UWGR","WM6232PU","temp01","temp02","temp03"]
device_data_arr = ["total_energy", "today_energy", "temperature", "gfci", "bus_volt", "power", "q_power", "pf",
                   "pv1_volt", "pv1_curr", "pv2_volt", "pv2_curr", "pv3_volt", "pv3_curr", "l1_volt", "l1_curr",
                   "l1_freq", "l1_dci", "l1_power", "l1_pf"]

class UsersForTest:
    '''creating users for testing'''
    def __init__(self, num=0,session=requests.Session()):
        self.num = num
        self.session = session
        self.data_arr = test_data_arr
        self.mobile = str(12312341200 + self.num)
        self.username = 'u'+ self.mobile
        self.password = 'p' + self.mobile
        self.email = 'test12345'+ str(600 + self.num) + '@zlg.cn'
    def get_smscode(self,mobile):
        '''获取注册短信验证码'''
        base_url = "https://zlab.zlgcloud.com/v1/auth/smscode?mobile=" + mobile
        r = self.session.get(base_url)
        return r
    def create_users(self,isagent=False):
        '''创建用户,isagent=False:创建普通用户，isagent=True:创建代理商'''
        session = requests.Session()
        r1 = session.get('https://zlab.zlgcloud.com/v1/auth/smscode?mobile=' + self.mobile)
        smscode = r1.json()['message']
        payload = {"username": self.username, "password": self.password, "mobile": self.mobile, "smscode": smscode, "email": self.email, "isagent": isagent}
        r2 = session.post("https://zlab.zlgcloud.com/v1/users", json=payload)
        return r2
    def get_users(self,filter="",skip="",limit="",aggregation=""):
        ''''查询符合条件的用户'''
        if (filter == '' and skip == '' and limit == '' and aggregation == '') == True:
            base_url = "https://zlab.zlgcloud.com/v1/users"
        else:
            base_url = "https://zlab.zlgcloud.com/v1/users" + '?' + filter + skip + limit + aggregation
        r = self.session.get(base_url)
        return r
    def get_user_info(self,username):
        '''获取用户信息'''
        base_url = "https://zlab.zlgcloud.com/v1/users/" + username
        r = self.session.get(base_url)
        return r
    def update_user_message(self,username="",code="",payload={}):
        '''更新用户信息'''
        if code == "":
            base_url = "https://zlab.zlgcloud.com/v1/users/" + username
        else:
            base_url = "https://zlab.zlgcloud.com/v1/users/" + username +'?code=' + code
        r = self.session.put(base_url,json=payload)
        return r
    def get_changing_email_code(self,email):
        '''获取修改邮箱的验证码'''
        base_url = "https://zlab.zlgcloud.com/v1/auth/change_email_verify_code?email=" + email
        r = self.session.get(base_url)
        return r
    def get_changing_mobile_code(self,mobile):
        '''获取修改手机的验证码'''
        base_url = "https://zlab.zlgcloud.com/v1/auth/change_mobile_verify_code?mobile=" + mobile
        r = self.session.get(base_url)
        return r
    def recover_password(self,username,type):
        '''恢复用户密码，获取验证码'''
        base_url = "https://zlab.zlgcloud.com/v1/auth/recover_password?username=" + username + "&type=" + type
        r = self.session.get(base_url)
        return r
    def reset_password(self,code,username,password):
        '''重置用户密码'''
        payload = { "code": code,"username": username,"password": password}
        base_url = "https://zlab.zlgcloud.com/v1/auth/reset_password"
        r = self.session.post(base_url,json=payload)
        return r
    def change_password(self,old_password,new_password):
        '''修改用户密码，需要提供旧密码'''
        payload = {"oldpassword": old_password,"password": new_password}
        base_url = "https://zlab.zlgcloud.com/v1/auth/change_password"
        r = self.session.post(base_url,json=payload)
        return r
    def login(self):
        '''登录'''
        base_url = 'https://zlab.zlgcloud.com/v1/auth/login'
        payload = {"username": self.username, "password": self.password}
        r = self.session.post(base_url, json=payload)
        return r
    def logout(self):
        '''退出登录'''
        base_url = 'https://zlab.zlgcloud.com/v1/auth/logout'
        r = self.session.get(base_url)
        return r
    def user_exist(self,username):
        base_url = 'https://zlab.zlgcloud.com/v1/auth/user_exist?username='
        r = self.session.get(url=base_url + username)
        return r
    def email_exist(self,email):
        base_url = 'https://zlab.zlgcloud.com/v1/auth/email_exist?email='
        r = self.session.get(url=base_url+email)
        return r
    def mobile_exist(self,mobile):
        base_url = 'https://zlab.zlgcloud.com/v1/auth/mobile_exist?mobile='
        r = self.session.get(url=base_url+mobile)
        return r
    def create_orgnization(self,orgnizationname='',desc='',address=''):
        '''创建组织'''
        base_url = "https://zlab.zlgcloud.com/v1/orgnizations"
        payload = {"orgnizationname":orgnizationname,"desc": desc,"address": address}
        r = self.session.post(base_url,json=payload)
        return r
    def delete_orgnization(self, orgnizationid):
        '''删除指定的组织'''
        base_url = "https://zlab.zlgcloud.com/v1/orgnizations/" + orgnizationid
        r = self.session.delete(base_url)
        return r
    def get_orgnizations(self,filter="",skip="",limit="",aggregation=""):
        '''查询满足条件的组织'''
        if (filter == '' and skip == '' and limit == '' and aggregation == '') == True:
            base_url = "https://zlab.zlgcloud.com/v1/orgnizations"
        else:
            base_url = "https://zlab.zlgcloud.com/v1/orgnizations" + '?' + filter + skip + limit + aggregation
        r = self.session.get(base_url)
        return r
    def get_all_orgnizations(self):
        '''查询满足条件的组织 接口，主要用于查询所有存在的orgnization'''
        base_url = "https://zlab.zlgcloud.com/v1/orgnizations"
        r = self.session.get(base_url)
        return r
    def login_get_delete_orgnization_and_agent(self):
        '''登录代理商查询组织id，然后逐个删除'''
        r1 = self.create_users(True)
        r2 = self.login()
        r3 = self.get_orgnizations()
        if r3.status_code == 200:
            orgnizations_arr = r3.json()['data']
            for orgnization in orgnizations_arr:
                r4 = self.delete_orgnization(orgnization['orgnizationid'])
        self.delete_users()
    def get_orgnization_message(self,orgnizationid):
        '''返回指定组织信息'''
        base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/'
        r = self.session.get(base_url+orgnizationid)
        return r
    def add_users_to_orgnization(self,orgnizationid,username,role = 0):
        '''添加用户到组织'''
        base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/' + orgnizationid +"/members"
        payload = {"username":username,"role":role}
        r = self.session.post(base_url,json=payload)
        return r
    def update_orgnization_info(self,orgnizationid,payload):
        '''更新组织信息'''
        base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/' + orgnizationid
        r = self.session.put(base_url,json=payload)
        return r
    def remove_user_from_orgnization(self,orgnizationid,username):
        '''从组织中移除用户'''
        base_url = 'https://zlab.zlgcloud.com/v1/orgnizations/' + orgnizationid + '/' + username
        r = self.session.delete(base_url)
        return r
    def create_device_group(self,payload):
        '''创建设备分组'''
        base_url = "https://zlab.zlgcloud.com/v1/device_groups"
        r = self.session.post(base_url,json=payload)
        return r
    def add_device(self,groupid,payload):
        '''添加设备到设备分组'''
        base_url = 'https://zlab.zlgcloud.com/v1/device_groups/'+groupid
        r = self.session.post(base_url,json=payload)
        return r
    def get_device_groups(self,filter="",skip="",limit="",aggregation=""):
        '''查询设备分组'''
        if (filter == "" and skip == "" and limit == "" and aggregation == "") == True:
            base_url = "https://zlab.zlgcloud.com/v1/device_groups"
        else:
            base_url = "https://zlab.zlgcloud.com/v1/device_groups?"+filter+skip+limit+aggregation
        r = self.session.get(base_url)
        return r
    def get_device_group_info(self,groupid):
        '''获取设备分组信息'''
        base_url = "https://zlab.zlgcloud.com/v1/device_groups/" + groupid
        r = self.session.get(base_url)
        return r
    def delete_device_group_picture(self,groupid,index):
        '''删除设备分组的图片'''
        base_url = 'https://zlab.zlgcloud.com/v1/device_groups/' + groupid + '/images?index=' + index
        r = self.session.delete(url=base_url)
        return r
    def device_group_upload_picture(self,groupid,index,file):
        base_url = 'https://zlab.zlgcloud.com/v1/device_groups/' + groupid + '/images?index=' + index
        r = self.session.post(url=base_url,files=file)
        return r
    def get_device_list(self,filter="",devtype="",skip="",limit="",aggregation=""):
        '''查询设备列表'''
        if (filter == "" and devtype == "" and skip == "" and aggregation == "") == True:
            base_url = "https://zlab.zlgcloud.com/v1/devices"
        else:
            base_url = "https://zlab.zlgcloud.com/v1/devices?" + filter + devtype + skip + limit + aggregation
        r = self.session.get(base_url)
        return r
    def add_device_data(self,devtype,devid,data):
        '''添加一条设备数据'''
        base_url = "https://zlab.zlgcloud.com/v1/devices/" + devid + '/data?devtype=' + devtype
        r = self.session.post(base_url,json=data)
        return r
    def device_data_inquery(self,devtype="",devid="",filter="",descend="",skip="",limit="",aggregation=""):
        '''查询满足条件的设备数据'''
        base_url = 'https://zlab.zlgcloud.com/v1/devices/'+ devid + '/data?devtype=' + devtype + filter + descend + skip + limit + aggregation
        r = self.session.get(base_url)
        return r
    def get_device_info(self,device):
        '''返回指定设备的信息'''
        base_url = 'https://zlab.zlgcloud.com/v1/devices/' + device['devid'] + '?devtype=' + device['devtype']
        r = self.session.get(url=base_url)
        return r
    def update_device_info(self,device):
        '''更新指定设备的信息'''
        base_url = 'https://zlab.zlgcloud.com/v1/devices/' + device['devid'] + '?devtype=' + device['devtype']
        r = self.session.put(url=base_url)
        return r
    def add_device_event(self,payload):
        '''添加一条设备事件'''
        base_url = "https://zlab.zlgcloud.com/v1/events"
        r = self.session.post(base_url,json=payload)
        return r
    def get_device_event(self,filter="",descend="",skip="",limit="",aggregation=""):
        '''查询满足条件的设备事件'''
        if (filter == "" and descend == "" and skip == "" and limit == "" and aggregation == "") == True:
            base_url = "https://zlab.zlgcloud.com/v1/events"
        else:
            base_url = "https://zlab.zlgcloud.com/v1/events?" + filter + descend + skip + limit + aggregation
        r = self.session.get(base_url)
        return r
    def get_device_commands(self,devtype,devid):
        '''查询设备支持的命令'''
        base_url = "https://zlab.zlgcloud.com/v1/devices/" + devid + "/commands?devtype=" + devtype
        r = self.session.get(base_url)
        return r
    def upload_firmware(self,model,version,file,file_path):
        '''上传固件'''
        base_url = "https://zlab.zlgcloud.com/v1/firmware/" + model + '/' + version
        payload = {'file': (file, open(file_path + file, 'rb'))}
        r = self.session.post(base_url,files=payload)
        return r
    def download_firmware(self,model,version):
        '''下载固件'''
        base_url = "https://zlab.zlgcloud.com/v1/public/firmware/" + model + '/' + version
        r = self.session.get(base_url)
        return r
    def get_firmware_list(self,model):
        '''列出固件列表'''
        base_url = "https://zlab.zlgcloud.com/v1/firmware/" + model
        r = self.session.get(base_url)
        return r
    def delete_firmware(self,model,version):
        '''删除固件'''
        base_url = "https://zlab.zlgcloud.com/v1/firmware/" + model + '/' + version
        r = self.session.delete(base_url)
        return r

    def delete_single_device(self,groupid,devtype,devid):
        '''删除单个设备'''
        base_url = "https://zlab.zlgcloud.com/v1/device_groups/" + groupid + '/' + devid + '?devtype=' + devtype
        r = self.session.delete(base_url)
        return r
    def delete_device_data(self,devtype,devid,filter=""):
        '''删除单个设备的数据'''
        base_url = "https://zlab.zlgcloud.com/v1/devices/"+devid+"/data?devtype="+devtype+filter
        r = self.session.delete(base_url)
        return r
    def delete_device_event(self,filter=""):
        '''删除满足条件的设备事件'''
        if filter == "":
            base_url = "https://zlab.zlgcloud.com/v1/events"
        else:
            base_url = "https://zlab.zlgcloud.com/v1/events?" + filter
        r = self.session.delete(base_url)
        return r
    def delete_data_and_devices_from_device_group(self):
        '''登录普通用户，查询device，然后逐个删除设备与设备数据'''
        r2 = self.login()
        # print('login?',r2.status_code)
        r1 = self.get_device_groups()
        device_groups_arr = r1.json()['data']
        for device_groups in device_groups_arr:
            for device in device_groups['devices']:
                r3 = self.delete_device_data(device['devtype'],device['devid'])
                # print("device data delete?",r3.json())
                r4 = self.delete_single_device(device_groups['groupid'],device['devtype'],device['devid'])
                # print("device delete?",r4.status_code)
    def delete_device_groups(self,groupid):
        '''删除已创建的设备分组'''
        base_url = 'https://zlab.zlgcloud.com/v1/device_groups/'
        r = self.session.delete(base_url+groupid)
        return r
    def delete_all_device_events(self,filter=""):
        '''删除所有的设备事件'''
        base_url = "https://zlab.zlgcloud.com/v1/events"+filter
        r = self.session.delete(base_url)
        return r
    def delete_users(self):
        '''删除已创建的用户'''
        base_url = 'https://zlab.zlgcloud.com/v1/users/'
        r = self.session.delete(base_url + self.username)
        return r
    def get_user_schema(self):
        '''获取辅助开发接口的users_schema'''
        base_url = 'https://zlab.zlgcloud.com/v1/dev/user_schema'
        r = requests.get(url=base_url)
        return r
    def get_device_schema(self):
        '''获取辅助开发接口的device_schema'''
        base_url = 'https://zlab.zlgcloud.com/v1/dev/device_schema'
        r = requests.get(url=base_url)
        return r
    def get_orgnization_schema(self):
        '''获取辅助开发接口的organization_schema'''
        base_url = 'https://zlab.zlgcloud.com/v1/dev/orgnization_schema'
        r = requests.get(url=base_url)
        return r
    def get_device_group_schema(self):
        '''获取辅助开发接口的device_group_schema'''
        base_url = 'https://zlab.zlgcloud.com/v1/dev/device_group_schema'
        r = requests.get(url=base_url)
        return r
class InitialData(object):
    '''进行数据初始化'''
    def __init__(self,first_agent_num=0,last_agent_num=0,first_user_num=0,last_user_num=0):
        self.first_agent_num = first_agent_num
        self.last_agent_num = last_agent_num
        self.first_user_num = first_user_num
        self.last_user_num = last_user_num
    def create_users(self):
        '''创建一组普通用户'''
        users_arr = []
        for n in range(self.first_user_num, self.last_user_num):
            session = requests.Session()
            user = UsersForTest(n, session)
            r1 = user.create_users()
            if r1.status_code == 201:
                user_data = r1.json()['data']
                del user_data['last_login_time']
                del user_data['password']
                # del user["last_login_time"]
                del user_data['password_changed_time']
                del user_data["last_login_ip"]
                users_arr.append(user_data)
            else:
                print('create user failed!!')
        return users_arr
    def create_agents(self):
        '''创建一组代理商'''
        agents_arr = []
        for n in range(self.first_agent_num, self.last_agent_num):
            session = requests.Session()
            user = UsersForTest(n, session)
            r1 = user.create_users(True)
            if r1.status_code == 201:
                agent_data = r1.json()['data']
                del agent_data['last_login_time']
                agents_arr.append(agent_data)
            else:
                print('create agent failed!!')
        return agents_arr
    def create_staff(self):
        '''创建一组员工'''
        agents_arr = []
        for n in range(self.first_user_num, self.last_user_num):
            session = requests.Session()
            user = UsersForTest(n, session)
            r1 = user.create_users(True)
            if r1.status_code == 201:
                agent_data = r1.json()['data']
                del agent_data['last_login_time']
                agents_arr.append(agent_data)
            else:
                print('create staff failed!!')
        return agents_arr
    def get_orgnizationid(self):
        '''创建代理商用户，并创建对应orgnization，获得代理商和orgnization的数组'''
        orgnization_test_data = create_test_data('orgnization_test_data.txt')
        agents_arr = self.create_agents()
        or_num = 0
        orgnizations_arr = []
        for agent in agents_arr:
            session = requests.Session()
            agent_self = UsersForTest(int(agent['mobile'][-3:]),session)
            agent_self.login()
            r1 = agent_self.create_orgnization(orgnization_test_data[or_num][0], orgnization_test_data[or_num][1],orgnization_test_data[or_num][2])
            agent['orgnizationid'] = r1.json()['data']['orgnizationid']
            agent['orgnizationname'] = orgnization_test_data[or_num][0]
            agent['desc'] = orgnization_test_data[or_num][1]
            agent['address'] = orgnization_test_data[or_num][2]
            orgnizations_arr.append(agent)
            or_num +=1
        return orgnizations_arr

    def add_users_to_orgnization(self):
        '''创建代理商，并创建组织，给每个组织添加用户'''
        orgnization_arr = self.get_orgnizationid()
        users_arr = self.create_users()
        m = 0
        for n in range(self.first_agent_num,self.last_agent_num):
            session = requests.Session()
            agent = UsersForTest(n,session)
            agent.login()
            agent.add_users_to_orgnization(orgnization_arr[m]['orgnizationid'],users_arr[m]['username'])
            orgnization_arr[m]['member'] = users_arr[m]['username']
            m +=1
        return orgnization_arr
    def add_several_users_to_orgnization(self,users_n):
        '''创建代理商，并创建组织，给每个组织添加多个用户'''
        orgnization_arr = self.get_orgnizationid()
        users_arr = self.create_users()
        m = 0
        j = 0
        for n in range(self.first_agent_num,self.last_agent_num):
            session = requests.Session()
            agent = UsersForTest(n,session)
            agent.login()
            orgnization_arr[m]['member'] = []
            for i in range(users_n):
                agent.add_users_to_orgnization(orgnization_arr[m]['orgnizationid'],users_arr[j]['username'])
                orgnization_arr[m]['member'].append(users_arr[j]['username'])
                j +=1
            m +=1
        return orgnization_arr
    def several_orgnizations_for_each_agent(self,orgnization_num):
        '''创建代理商，每个代理商创建多个组织，返回代理商及所包含组织的数组'''
        orgnization_test_data = create_test_data('orgnization_test_data.txt')
        agents_arr = self.create_agents()
        org_num = 0
        for agent in agents_arr:
            session = requests.Session()
            agent_self = UsersForTest(int(agent['mobile'][-2:]),session)
            agent_self.login()
            for n in range(orgnization_num):
                r1 = agent_self.create_orgnization(orgnization_test_data[org_num][0],orgnization_test_data[org_num][1],orgnization_test_data[org_num][2])
                org_num +=1
            agent['orgnization_arr'] = agent_self.get_orgnizations().json()['data']
        agents_orgnizations_arr = agents_arr
        agents_orgnizations_arr.sort(key=str)
        return agents_orgnizations_arr

    def create_agents_orgnizations_staff(self,orgnization_num,user_num):
        '''返回一组代理商，代理商包含多个组织，每个组织包含多个用户'''
        staff_arr = self.create_staff()
        agents_orgnizations_arr = self.several_orgnizations_for_each_agent(orgnization_num)
        m = 0
        for agent in agents_orgnizations_arr:
            session = requests.Session()
            agent_self = UsersForTest(int(agent['mobile'][-2:]),session)
            agent_self.login()
            for orgnization in agent['orgnization_arr']:
                # print(orgnization)
                orgnization['members'] = []
                for n in range(user_num):
                    r1 = agent_self.add_users_to_orgnization(orgnization['orgnizationid'],staff_arr[m]['username'])
                    # print('add staff?',r1.json())
                    orgnization['members'].append(staff_arr[m])
                    m +=1
        agents_orgnizations_users = agents_orgnizations_arr
        return agents_orgnizations_users
    def create_several_device_groups_for_each_user(self,orgnization_num,user_num,device_group_num):
        '''创建一组代理商，创建一组普通用户，登录每个代理商，创建一组orgnization，给每个orgnization添加一组普通用户，
        登录普通用户，依次添加多个设备分组'''
        device_groups_test_data_arr = create_test_data('device_groups_test_data.txt')
        agents_orgnizations_users_arr = self.create_agents_orgnizations_staff(orgnization_num,user_num)
        m = 0
        for agent in agents_orgnizations_users_arr:
            for orgnization in agent['orgnization_arr']:
                for user in orgnization['members']:
                    session = requests.Session()
                    user_self = UsersForTest(int(user['mobile'][-3:]),session)
                    user_self.login()
                    user['device_groups']=[]
                    for n in range(device_group_num):
                        r = user_self.create_device_group({"groupname":device_groups_test_data_arr[m][0],"desc":device_groups_test_data_arr[m][1]})
                        if r.status_code == 201:
                            user['device_groups'].append(r.json()['data'])
                        else:
                            print('created device_groups failed!')
                        m += 1
                    user['device_groups'].sort(key=str)
        agents_orgnizations_users_device_groups = agents_orgnizations_users_arr
        return agents_orgnizations_users_device_groups
    def create_users_device_groups(self,device_group_num):
        '''创建一组普通用户，给每个用户创建多个设备分组'''
        device_groups_test_data_arr = create_test_data('device_groups_test_data.txt')
        users_arr = self.create_users()
        m = 0
        for user in users_arr:
            session = requests.Session()
            user_self = UsersForTest(int(user['mobile'][-2:]), session)
            user_self.login()
            user['device_groups'] = []
            for n in range(device_group_num):
                r = user_self.create_device_group(
                    {"groupname": device_groups_test_data_arr[m][0], "desc": device_groups_test_data_arr[m][1]})
                if r.status_code == 201:
                    user['device_groups'].append(r.json()['data'])
                else:
                    print('created device_groups failed!')
                m += 1
            user['device_groups'].sort(key=str)
        users_device_groups = users_arr
        return users_device_groups

    def users_device_groups_devices(self,device_group_num,device_num):
        '''创建一组普通用户，给每个用户创建多个设备分组，每个设备分组添加多个设备'''
        device_test_data = create_test_data('device_test_data.txt')
        users_device_groups_arr = self.create_users_device_groups(device_group_num)
        j = 0
        for user in users_device_groups_arr:
            session = requests.Session()
            user_self = UsersForTest(int(user['mobile'][-2:]),session)
            user_self.login()
            for device_group in user['device_groups']:
                device_group['devices'] = []
                for n in range(device_num):
                    payload = {'devid':device_test_data[j][0],'devtype':device_test_data[j][1]}
                    r = user_self.add_device(device_group['groupid'],payload)
                    # print(r.json())
                    j +=1
                r1 = user_self.get_device_group_info(device_group['groupid'])
                if r1.status_code == 200:
                    device_group['devices'] = r1.json()["devices"]
                    for device in device_group['devices']:
                        del device['time']
                        del device['offlinetime']
                        del device['registertime']
                        del device['newfm']
                        del device['onlinetime']
                        del device['resources']
                        del device['uri']
                else:
                    print('get device list failed!')
        users_device_groups_devices_arr = users_device_groups_arr
        # users_device_groups_devices_arr.sort(key=str)
        return users_device_groups_devices_arr
    def users_device_groups_devices_datas(self,device_group_num,device_num,data_num):
        '''创建一组普通用户，给每个用户创建多个设备分组，每个设备分组添加多个设备,每个设备添加多个数据'''
        # device_data_arr = ["total_energy","today_energy","temperature","gfci","bus_volt","power","q_power","pf","pv1_volt","pv1_curr","pv2_volt","pv2_curr","pv3_volt","pv3_curr","l1_volt","l1_curr","l1_freq","l1_dci","l1_power","l1_pf"]
        users_device_groups_devices_arr = self.users_device_groups_devices(device_group_num,device_num)
        j = 0
        t = 10000
        for user in users_device_groups_devices_arr:
            session = requests.Session()
            user_self = UsersForTest(int(user['mobile'][-2:]), session)
            user_self.login()
            for device_group in user['device_groups']:
                for device in device_group['devices']:
                    device['data'] = []
                    for n in range(data_num):
                        if j == len(device_data_arr)-1:
                            j = 0
                        data = {device_data_arr[j]: 0,device_data_arr[j+1]:0,"time":t}
                        r = user_self.add_device_data(device['devtype'], device['devid'], data)
                        if r.status_code == 200:
                            data['devid'] = device['devid']
                            device['data'].append(data)
                        else:
                            print('Add data failed!!')
                        j += 1
                        t += 1
                    # print(device['data'])
                    # r1 = user_self.device_data_inquery(device['devtype'], device['devid'])
                    # if r1.status_code == 200:
                        # device['data'] = r1.json()['data']
        users_device_groups_devices_datas_arr = users_device_groups_devices_arr
        return users_device_groups_devices_datas_arr

    def users_device_events(self,device_events_num):
        '''创建一组用户，给这组用户添加多条设备事件'''
        users_arr = self.create_users()
        i = 0
        for user in users_arr:
            user['device_events'] = []
            session = requests.Session()
            user_self = UsersForTest(int(user['mobile'][-2:]),session)
            user_self.login()
            for n in range(device_events_num):
                payload = {"name": device_event_test_data_arr[i][0],"time": int(device_event_test_data_arr[i][1]), "eventtype": device_event_test_data_arr[i][2], "devtype": device_event_test_data_arr[i][3], "devid": device_event_test_data_arr[i][4]}
                r = user_self.add_device_event(payload)
                i +=1
                if r.status_code == 200:
                    user['device_events'].append(r.json()['data'])
                else:
                    print('Add device event failed!')
            # user['device_events'].sort(key=str)
        return users_arr
    def users_for_firmware_test(self,firmware_admin_num):
        '''更改普通用户角色为固件管理员，返回普通用户和固件管理员的数组'''
        users_arr = self.create_users()
        session = requests.Session()
        admin = UsersForTest(0,session)
        admin.username = 'admin'
        admin.password = 'admin123'
        admin.login()
        i = 0
        for n in range(firmware_admin_num):
            r1 = admin.update_user_message(users_arr[i]['username'],"",{"role":2})
            if r1.status_code == 200:
                users_arr[i]['role'] = 2
            else:
                print('update message failed!!')
            i +=1
        return users_arr
    def upload_firmwares(self,firmware_num):
        '''上传多个固件'''
        session = requests.Session()
        user = UsersForTest(87,session)
        user.create_users()
        admin = UsersForTest(0,session)
        admin.username = 'admin'
        admin.password = 'admin123'
        admin.login()
        r1 = admin.update_user_message(user.username,"",{'role':2})
        user.login()
        f = 0
        firmware_arr = []
        for model in models_list:
            v = 1.01
            model_self = {'model':model}
            model_self['versions'] = []
            for n in range(firmware_num):
                r = user.upload_firmware(model=model,version=str(v),file="firmware_test_file_"+str(f)+".zip",file_path=test_data_path+"\\test_firmware\\firware_test_initial/")
                if r.status_code ==200:
                    model_self['versions'].append(str(v))
                else:
                    print('upload firmware failed!')
                v +=0.01
                f +=1
            firmware_arr.append(model_self)
        user.login()
        r4 = user.delete_users()
        if r4.status_code != 200:
            print('delete user failed!!')
        return firmware_arr


    # def users_device_groups_devices_datas(self,device_group_num,device_num,device_data_num):
    #     '''创建一组用户，给这组用户添加多个设备分组，给每个设备分组添加多个设备，给每个设备添加一组数据'''
        # user_device_groups_devices_arr = self.users_device_groups_devices(device_group_num,device_num)
        # device_data_arr = ["total_energy","today_energy","temperature","gfci","bus_volt","power","q_power","pf","pv1_volt","pv1_curr","pv2_volt","pv2_curr","pv3_volt","pv3_curr","l1_volt","l1_curr","l1_freq","l1_dci","l1_power","l1_pf"]
        # for user in user_device_groups_devices_arr:
        #     session = requests.Session()
        #     user_self = UsersForTest(int(user['mobile'][-3:]),session)
        #     for device_group in user['device_groups']:
        #         for device in device_group['devices']:
        #             for n in range(device_num):
        #                 data = {device_data_arr[i]:0}
        #                 r = user_self.add_device_data(device['devtype'],device['devid'],data)

    def delete_all_users(self,):
        '''清除测试数据，还原环境'''
        for n in range(self.first_user_num,self.last_user_num):
            session = requests.Session()
            user = UsersForTest(n, session)
            user.login()
            r1 = user.delete_users()
            # print('%d delete' %n)
            # print(r1.status_code)
        for m in range(self.first_agent_num,self.last_agent_num):
            session = requests.Session()
            agent = UsersForTest(m,session)
            agent.login()
            r1 = agent.delete_users()
            # print('%d delete' %m)
            # print(r1.status_code)

    def delete_all_agents_and_orgnizations(self):
        '''删除所有的代理商和其组织'''
        for n in range(self.first_agent_num,self.last_agent_num):
            session = requests.session()
            agent = UsersForTest(n,session)
            agent.create_users(True)
            agent.login_get_delete_orgnization_and_agent()

    def delete_all_devices_and_data(self):
        '''删除所有用户的所属设备和数据'''
        for n in range(self.first_user_num,self.last_user_num):
            session = requests.Session()
            user = UsersForTest(n,session)
            r1 = user.login()
            # print('user login?',r1.status_code)
            r2 = user.get_device_list(devtype='devtype=inverter')
            # print('get device list?',r2.json())
            if r2.status_code == 200:
                for device in r2.json()['data']:
                    r3 = user.delete_device_data(device['devtype'],device['devid'],"")
                    # print(r3.json())
                    if r3.status_code != 200:
                        print('delete data failed!')
    def delete_all_pictures_of_device_group(self):
        for n in range(self.first_user_num,self.last_user_num):
            session = requests.Session()
            user = UsersForTest(num=n,session=session)
            user.login()
            r1 = user.get_device_groups()
            if r1.status_code == 200:
                device_groups = r1.json()['data']
                for device_group in device_groups:
                    for index in range(6):
                        r2 = user.delete_device_group_picture(groupid=device_group['groupid'],index=str(index))
                        print(r2.status_code)
            else:
                print('Get device groups failed!!!')
    def delete_all_device_events(self):
        '''删除所有用户的所属设备事件'''
        for n in range(self.first_user_num,self.last_user_num):
            session = requests.Session()
            user = UsersForTest(n,session)
            r1 = user.create_users()
            # print('user created?',r1.status_code)
            r2 = user.login()
            # print('user login?',r2.status_code)
            r = user.delete_device_event()
            # print(r.json())
    def delete_all_firmware(self,user_num=0):
        '''删除所有固件'''
        session = requests.Session()
        firmware_admin = UsersForTest(num=user_num,session=session)
        firmware_admin.create_users()
        admin = UsersForTest(num=0,session=requests.Session())
        admin.username = 'admin'
        admin.password = 'admin123'
        admin.login()
        r1 = admin.update_user_message(username=firmware_admin.username,code="",payload={'role':2})
        print(r1.json())
        print('set firmware_admin',r1.status_code)
        firmware_admin.login()
        for model in models_list:
            r2 = firmware_admin.get_firmware_list(model)
            if r2.status_code == 200:
                firmware_arr = r2.json()
                print(firmware_arr)
                for firmware in firmware_arr:
                    r3 = firmware_admin.delete_firmware(model,firmware['name'])
                    # print('delete firmware?',r3.status_code)
            else:
                print('get firmware list failed!!')
        firmware_admin.login()
        r4 = firmware_admin.delete_users()
        if r4.status_code != 200:
            print('delete user failed!!')

def init_data():
    for n in range(0,100):
        session = requests.Session()
        user = UsersForTest(n,session)
        r1 = user.login()
        r2 = user.delete_users()
        print(n,'login? %d',r1.status_code)
        print(n,"delete?",r2.status_code)
    # orgnization_list = requests.get(url='http://zlab.zlgcloud.com:8280/v1/orgnizations').json()['data']
    # print(orgnization_list)
    # #删除所有的组织
    # for orgnization in orgnization_list:
    #     r3 = requests.delete(url="http://zlab.zlgcloud.com:8280/v1/orgnizations/"+orgnization["orgnizationid"]+'?owner=' + orgnization["owner"])
    #     print(orgnization['orgnizationid'], ':delete?',r3.status_code)

if __name__ == '__main__':
    for n in range(100):
        user = UsersForTest()
        r = user.mobile_exist(mobile=str(12312341200+n))
        print(n,r.status_code)

