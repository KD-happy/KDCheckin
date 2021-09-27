# -*- coding: utf-8 -*-
"""
cron: 55 5 * * *
new Env('CCAVA');
"""

import requests, time, re, json, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class CCAVA:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def Sign_in(self):
        url = "https://pc.ccava.net/zb_users/plugin/mochu_us/cmd.php?act=qiandao"
        res = requests.get(url, headers={"Cookie": self.cookie})
        data = res.json()
        print(data)
        if '登录' in data['msg']:
            self.sio.write('Cookie失效\n')
        elif '今天' in data['msg']:
            self.sio.write(f'重复签到, 剩余{data["giod"]}月光币\n')
        else:
            self.sio.write(f'签到成功, 剩余{data["giod"]}月光币\n')

    def SignIn(self):
        print("【CCAVA 日志】")
        self.sio.write("【CCAVA】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.Sign_in()
            except BaseException as e:
                print(f"{cookie.get('name')}: 异常 {e}\n")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('CCAVA')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            ccava = CCAVA(Cookies['cookies'])
            sio = ccava.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('CCAVA', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 CCAVA 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 CCAVA')