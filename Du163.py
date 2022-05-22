# -*- coding: utf-8 -*-
"""
cron: 20 6 * * *
new Env('网易读书');
"""

import requests, sys, traceback
from io import StringIO

from requests.api import get
from KDconfig import getYmlConfig, send

class Du163:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
        self.xsrf = ''

    def Sign_in(self):
        url = 'https://du.163.com/activity/201907/activityCenter/sign.json'
        headers = {
            'cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PCAM00 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.36 NeteaseSnailReader/1.9.14 NetType/3G+ (bnvsbaljndplmzo5zjpmntphmtowzglimtcxy2uzntrmmjrjntmycwq1mdcwmjmymgvlnjniogi%3d;oppo) NEJSBridge/2.0.0'
        }
        data = {'csrfToken': self.xsrf}
        res = requests.post(url, headers=headers, data=data)
        print(res.text)
        msg = 'Cookie失效'
        if '已经签过' in res.text:
            msg = '重复签到'
        elif res.json().get('code') == 0:
            data = res.json()
            message = data.get('message')
            day = data.get('continuousSignedDays')
            msg = f'{message}, 连续签到{day}天'
        print(msg)
        self.sio.write(msg + '\n')

    def SignIn(self):
        print("【网易读书 日志】")
        self.sio.write("【网易读书】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            du163_cookie = {item.split("=")[0]: item.split("=")[1] for item in self.cookie.split("; ")}
            self.xsrf = du163_cookie.get('_xsrf')
            try:
                self.Sign_in()
            except:
                self.sio.write(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Du163')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            du163 = Du163(Cookies['cookies'])
            sio = du163.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('网易读书', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 网易读书 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 网易读书')