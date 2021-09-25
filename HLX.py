"""
cron: 11 6 * * *
new Env('葫芦侠')
"""

import requests, json, sys, hashlib
from io import StringIO
from KDconfig import getYmlConfig, send
from bs4 import BeautifulSoup

class HLX:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.username = ''
        self.password = ''
        self.key = ''
        self.nick = ''
        self.userID = ''

    def md5(self):
        m = hashlib.md5()
        b = self.password.encode(encoding='utf-8')
        m.update(b)
        password_md5 = m.hexdigest()
        return password_md5


    def login(self):
        password_md5 = self.md5()
        url = 'http://floor.huluxia.com/account/login/ANDROID/4.0?device_code=1'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'account': self.username,
            'login_type': '2',
            'password': password_md5,
        }
        response = requests.post(url=url, data=data, headers=headers)
        self.key = json.loads(response.text)['_key']
        self.nick = json.loads(response.text)['user']['nick']
        self.userID = json.loads(response.text)['user']['userID']
        print('[+]用户：' + self.nick + ';userID:' + str(self.userID))

    def get_level(self):
        url = 'http://floor.huluxia.com/view/level?viewUserID={userID}&_key={key}'.format(
            userID=self.userID, key=self.key)
        response = requests.post(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')  #解析html页面
        level = soup.select('.lev_li_forth span')  #筛选经验值
        print('[+]当前经验值:' + level[0].string)
        print('[+]距离下一等级:' + level[1].string + '还需:' + level[2].string + '经验')


    def sign(self):
        url = 'https://floor.huluxia.com/category/list/ANDROID/2.0'
        response = requests.get(url=url)
        categories = json.loads(response.text)['categories']
        count = 0  #签到次数
        for list in categories:
            categoryID = list['categoryID']
            title = list['title']
            url = 'https://floor.huluxia.com/user/signin/ANDROID/4.0?_key={key}&cat_id={categoryID}'.format(
                key=self.key, categoryID=categoryID)
            response = requests.get(url=url)
            msg = json.loads(response.text)['msg']
            status = json.loads(response.text)['status']
            if status == 0:
                print('[+]' + msg)
            if status == 1:
                count += 1
                print('[+]板块' + str(count) + '：' + title + ' 签到成功')
        self.sio.write(': 共计签到' + str(count) + '个板块')
        print('[+]共计签到' + str(count) + '个板块')

    def SignIn(self):
        print("【葫芦侠 日志】")
        self.sio.write("【葫芦侠】")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            self.sio.write(f'\n{cookie["name"]}')
            try:
                self.username = cookie['username']
                self.password = cookie['password']
                self.login()
            except BaseException as e:
                print('[+]登录失败，请检测账号密码')
                continue
            self.get_level()
            print('---结束【登录，查询用户信息】---\n')

            print('---开始【签到】---')
            self.sign()
            print('---结束【签到】---')
            print('[+]选择不推送信息')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('HLX')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            hlx = HLX(Cookies['cookies'])
            sio = hlx.SignIn()
            print(sio.getvalue())
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('葫芦侠', sio.getvalue())
            else:
                print('\n推送失败: 关闭了推送 or send配置问题')
        else:
            print('\n配置文件 葫芦侠 没有 "cookies"')
            sys.exit()
    else:
        print('\n配置文件没有 葫芦侠')