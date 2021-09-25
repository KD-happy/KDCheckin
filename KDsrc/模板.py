# -*- coding: utf-8 -*-
"""
cron: 55 7 * * *
new Env('天翼云盘');
"""

import requests, time, re, json, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class Cloud:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie

    def SignIn(self):
        print("【天翼云盘 日志】")
        self.sio.write("【天翼云盘】")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            try:
                self.Sign_in(cookie.get('name'), cookie.get('cookie'))
            except BaseException as e:
                print(f"\n{cookie.get('name')}: {e}")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('{签到的key}')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            cloud = Cloud(Cookies['cookies'])
            sio = cloud.SignIn()
            print(sio.getvalue())
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('{签到的标题}', sio.getvalue())
            else:
                print('\n推送失败: 关闭了推送 or send配置问题')
        else:
            print('\n配置文件 {签到的标题} 没有 "cookies"')
            sys.exit()
    else:
        print('\n配置文件没有 {签到的标题}')