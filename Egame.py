# -*- coding: utf-8 -*-
"""
cron: 11 5 * * *
new Env('企鹅电竞');
"""

"""
后续会添加的
1. 疯狂打卡
2. 午间/晚间 登录
3. 关注/取关主播 尽量
"""

import requests, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class Egame:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def signin(self):
        url = 'https://game.egame.qq.com/cgi-bin/pgg_async_fcgi?param={"key":{"module":"pgg.user_task_srf_svr.CPGGUserTaskSrfSvrObj","method":"OldUserCheckin","param":{}}}'
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.get(url, headers=header)
        print(res.text)
        data = res.json()
        if data.get('uid') == 0:
            print('Cookie失效')
            self.sio.write('Cookie失效\n')
        elif data['data']['key']['retMsg'] == '成功':
            print(f"签到成功, 获得{data['data']['key']['retBody']['data']['award']['description']}")
            self.sio.write(f"签到成功, 获得{data['data']['key']['retBody']['data']['award']['description']}\n")
        else:
            print(data['data']['key']['retMsg'])
            self.sio.write(f"{data['data']['key']['retMsg']}\n")    

    def SignIn(self):
        print("【企鹅电竞 日志】")
        self.sio.write("【企鹅电竞】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.signin()
            except BaseException as e:
                print(f"{cookie.get('name')}: 异常 {e}\n")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Egame')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            egame = Egame(Cookies['cookies'])
            sio = egame.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('企鹅电竞', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 企鹅电竞 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 企鹅电竞')