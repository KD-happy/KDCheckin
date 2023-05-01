# -*- coding: utf-8 -*-
"""
cron: 55 7 * * *
new Env('恩山论坛');
"""

import requests, re, traceback, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class EnShan:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def sign(self):
        url = "https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1"
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Cookie': self.cookie
        }
        res = requests.get(url, headers=headers)
        if '您需要先登录才能继续本操作' in res.text:
            print("Cookie失效")
            self.sio.write("Cookie失效\n")
        else:
            coin = re.findall("恩山币: </em>(.*?)nb &nbsp;", res.text)[0]
            print(f"签到成功, 剩余{coin}nb")
            self.sio.write(f"签到成功, 剩余{coin}nb\n")

    def SignIn(self):
        print("【恩山论坛 日志】")
        self.sio.write("【恩山论坛】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.sign()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('EnShan')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            enshan = EnShan(Cookies['cookies'])
            sio = enshan.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('恩山论坛', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 恩山论坛 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 恩山论坛')