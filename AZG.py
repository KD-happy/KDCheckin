# -*- coding: utf-8 -*-
"""
cron: 3 0 * * *
new Env('爱助攻');
"""

import requests, sys, traceback
from io import StringIO
from bs4 import BeautifulSoup
from KDconfig import getYmlConfig, send

class AZG:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def get_formhash(self):
        url = 'https://www.aizhugong.com/plugin.php?id=k_misign:sign'
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        formhash = soup.select("input[name=formhash]")[0]['value']
        return formhash

    def k_misign(self):
        url = f'https://www.aizhugong.com/plugin.php?id=k_misign:sign&operation=qiandao&formhash={self.get_formhash()}'
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.get(url, headers=headers)
        print(res.text[:500])
        if '已签' in res.text:
            self.sio.write('重复签到\n')
        elif '立即注册' in res.text:
            self.sio.write('Cookie失效\n')
        else:
            self.sio.write('签到成功\n')

    def SignIn(self):
        print("【爱助攻 日志】")
        self.sio.write("【爱助攻】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.k_misign()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('AZG')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            azg = AZG(Cookies['cookies'])
            sio = azg.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('爱助攻', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 爱助攻 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 爱助攻')