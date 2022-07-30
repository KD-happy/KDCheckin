# -*- coding: utf-8 -*-
"""
cron: 55 7 * * *
new Env('油猴中文网');
"""

from signal import valid_signals
import requests, time, re, json, sys, traceback
from io import StringIO
from bs4 import BeautifulSoup
from KDconfig import getYmlConfig, send

class YHZWW:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def get_formhash(self):
        url = 'https://bbs.tampermonkey.net.cn/dsu_paulsign-sign.html'
        headers = {
            'cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        alert = soup.select("input[name=formhash][type=hidden]")
        value =  alert[0]['value']
        print(value)
        return value

    def Sign_in(self):
        url = "https://bbs.tampermonkey.net.cn/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1"
        data = {
            'formhash': self.get_formhash(),
            'qdxq': 'kx',
            'qdmode': 3,
            'todaysay': '',
            'fastreply': 0,
        }
        headers = {
            'cookie': self.cookie,
            'referer': 'https://bbs.tampermonkey.net.cn/plugin.php?id=dsu_paulsign:sign',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        res = requests.post(url=url, headers=headers, data=data)
        msg = re.findall('([\u4e00-\u9fa5！. 0-9!，]+)</div>', res.text)
        if len(msg) == 1:
            self.sio.write(msg[0] + '\n')
        else:
            self.sio.write("Cookie失效\n")
        print(res.text[:1000])

    def SignIn(self):
        print("【油猴中文网 日志】")
        self.sio.write("【油猴中文网】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.Sign_in()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('YHZWW')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            cloud = YHZWW(Cookies['cookies'])
            sio = cloud.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('油猴中文网', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 油猴中文网 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 油猴中文网')