# -*- coding: utf-8 -*-
"""
cron: 55 7 * * *
new Env('CSDN');
"""

import requests, time, re, json, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class CSDN:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def signIn(self):
        url = 'https://me.csdn.net/api/LuckyDraw_v2/signIn'
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.get(url, headers=header)
        data = res.json()
        print(data)
        if data['code'] == 200:
            if '已签到' in data['data']['msg']:
                self.sio.write('重复签到')
            else:
                self.sio.write('签到成功')
            self.goodluck()
        else:
            self.sio.write('Cookie失效\n')
    
    def goodluck(self):
        url = 'https://me.csdn.net/api/LuckyDraw_v2/goodluck'
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.get(url, headers=header)
        data = res.json()
        print(data)
        if data['code'] == 200:
            if data.get('data').get('prize_title') != None:
                self.sio.write(f", {data.get('data').get('prize_title')}\n")
                print(f"{data.get('data').get('prize_title')}")
            else:
                self.sio.write(f", {data.get('data').get('msg')}\n")
                print(f"{data.get('data').get('msg')}")
        else:
            self.sio.write('抽奖失败\n')


    def SignIn(self):
        print("【CSDN 日志】")
        self.sio.write("【CSDN】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.signIn()
            except BaseException as e:
                print(f"{cookie.get('name')}: 异常 {e}\n")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('CSDN')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            csdn = CSDN(Cookies['cookies'])
            sio = csdn.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('CSDN', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 CSDN 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 CSDN')