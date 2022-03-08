"""
cron: 11 6 * * *
new Env('葫芦侠')
"""

import requests, json, sys, hashlib, traceback, time
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
        url = 'http://floor.huluxia.com/account/login/IOS/4.0?device_code=1'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'okhttp/3.8.1',
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
        url = "https://floor.huluxia.com/category/forum/list/IOS/1.0"
        ura = "https://floor.huluxia.com/category/forum/list/all/IOS/1.0"
        urs = "https://floor.huluxia.com/user/signin/IOS/1.1"
        categoryforum = requests.post(url).json()["categoryforum"]
        count = 0
        for i in categoryforum:
            categories = requests.post(url=ura, data={"fum_id": i["id"]}).json()[
                "categories"
            ]
            for cat in categories:
                headers = {
                    "Host": "floor.huluxia.com",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "Floor/1.3.0 (iPhone; iOS 15.3; Scale/3.00)",
                    "Accept-Language": "zh-Hans-CN;q=1",
                    "Content-Length": "304",
                    "Accept-Encoding": "gzip, deflate, br",
                }
                res = requests.post(
                    url=urs,
                    data={"_key": self.key, "cat_id": cat["categoryID"]},
                    headers=headers,
                ).json()
                msg = res["msg"]
                status = res["status"]
                if status == 0:
                    print("[+]" + cat["title"] + " 签到失败 错误原因：" + msg)
                elif status == 1:
                    count += 1
                    print("[+]" + cat["title"]+ " 签到成功 获得经验：" + str(res["experienceVal"]))
        self.sio.write(': 共计签到' + str(count) + '个板块\n')
        print('[+]共计签到' + str(count) + '个板块\n')

    def SignIn(self):
        print("【葫芦侠 日志】")
        self.sio.write("【葫芦侠】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            self.sio.write(f'{cookie["name"]}')
            try:
                self.username = cookie['username']
                self.password = cookie['password']
                self.login()
            except:
                print('[+]登录失败，请检测账号密码')
                self.sio.write(': 登录失败，请检测账号密码\n')
                print('异常: ' + traceback.format_exc())
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
                continue
            self.get_level()
            print('---结束【登录，查询用户信息】---')
            print('---开始【签到】---')
            self.sign()
            print('---结束【签到】---')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('HLX')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            hlx = HLX(Cookies['cookies'])
            sio = hlx.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('葫芦侠', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 葫芦侠 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 葫芦侠')