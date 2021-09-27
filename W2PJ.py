# -*- coding: utf-8 -*-
"""
cron: 21 6 * * *
new Env('吾爱破解');
"""

import requests, sys, re
from io import StringIO
from KDconfig import getYmlConfig, send

class W2PJ:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    # 签到
    def task(self):
        url = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
        header = {
            "Referer": "https://www.52pojie.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Cookie": self.cookie
        }
        res = requests.get(url, headers=header)
        print(res.text)
        if '恭喜' in res.text:
            self.sio.write('签到成功')
            self.getCB()
        elif '已申请过此任务' in res.text:
            self.sio.write('重复签到')
            self.getCB()
        else:
            self.sio.write('Cookie失效\n')

    # 获取 CB
    def getCB(self):
        url = 'https://www.52pojie.cn/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu'
        header = {
            "Referer": "https://www.52pojie.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Cookie": self.cookie
        }
        res = requests.get(url, headers=header)
        cb = re.findall('吾爱币: <span id="hcredit_2">(.*)</span></li><li> 贡献值', res.text)[0]
        print(f'剩余{cb}')
        self.sio.write(f', 剩余{cb}\n')

    def SignIn(self):
        print("【吾爱破解 日志】")
        self.sio.write("【吾爱破解】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            self.cookie = cookie.get("cookie")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            try:
                self.task()
            except BaseException as e:
                print(f"{cookie.get('name')}: 异常 {e}\n")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('W2PJ')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            w2pj = W2PJ(Cookies['cookies'])
            sio = w2pj.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('吾爱破解', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 吾爱破解 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 吾爱破解')