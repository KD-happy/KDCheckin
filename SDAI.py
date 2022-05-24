# -*- coding: utf-8 -*-
"""
cron: 3 8 * * *
new Env('神代汉化组');
"""

import requests, time, re, json, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send

class SDAI:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
        self.url = "https://www.sdai.me/wp-admin/admin-ajax.php"
        self.headers = {
            'cookie': self.cookie,
            'referer': 'https://www.sdai.me/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        self._nonce = ''
        self.point = 0

    def user_info(self):
        self._nonce = ""
        self.headers['cookie'] = self.cookie
        res = requests.get(url=self.url, headers=self.headers, params={
                'action': '05cb72cbd26af33ef26d5525c0097651',
                'dbf5b3985f794fa68fae27b6cfae8755[type]': 'checkSigned',
                '9cf2f21d615fc9c18397da44e9363725[type]': 'checkUnread',
                '7552d1b6008879534d6d573f3bdad742[type]': 'getUnreadCount'
            })
        myjson = res.json()
        print(myjson)
        if myjson['user']['id'] == 0:
            print("Cookie失效")
        else:
            signed = "已签" if myjson['customPointSignDaily']['signed'] else "未签"
            print(f"用户名: {myjson['user']['name']}, 用户ID: {myjson['user']['id']}, 今日签到: {signed}, 神币数: {myjson['customPoint']['point']}")
            self.point = myjson['customPoint']['point']
            self._nonce = myjson['_nonce']

    def sign_in(self):
        self.headers['cookie'] = self.cookie
        res = requests.get(url=self.url, headers=self.headers, params={
                '_nonce': self._nonce,
                'action': "dbf5b3985f794fa68fae27b6cfae8755",
                'type': "goSign"
            })
        print(res.text)
        if res.json()['code'] == 0:
            self.sio.write("签到成功")
        else:
            self.sio.write("签到失败")

    def like(self):
        self.headers['cookie'] = self.cookie
        data = {
            'postId': 14430
        }
        for i in range(4):
            res = requests.post(url=self.url, headers=self.headers, data=data, params={
                    '_nonce': self._nonce,
                    'action': 'd6f717f7852f1f69b9818230bed4b07c',
                    'type': 'add'
                })
            print(res.text)
            time.sleep(1)
        self.sio.write(" 点赞成功")

    def SignIn(self):
        print("【神代汉化组 日志】")
        self.sio.write("【神代汉化组】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.user_info()
                if self._nonce == "":
                    self.sio.write("Cookie失效\n")
                else:
                    self.sign_in()
                    time.sleep(2)
                    self.like()
                    time.sleep(2)
                    self.user_info()
                    self.sio.write(f' 神币数: {self.point}\n')
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('SDAI')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            cloud = SDAI(Cookies['cookies'])
            sio = cloud.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('神代汉化组', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 神代汉化组 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 神代汉化组')