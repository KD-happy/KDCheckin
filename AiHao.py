# -*- coding: utf-8 -*-
"""
cron: 23 8,13,18 * * *
new Env('爱好论坛');
"""

import requests, sys, datetime, traceback, re
from io import StringIO
from bs4 import BeautifulSoup
from KDconfig import getYmlConfig, send

class AiHao:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
        self.data = ''

    def daka(self):
        url = 'https://www.aihao.cc/plugin.php?id=daka'
        headers = {
            "referer": "https://www.aihao.cc/plugin.php?id=daka",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.post(url=url, headers=headers, data=self.data)
        if '未到打卡时间' in res.text:
            print('未到打卡时间')
        elif '打卡成功' in res.text:
            self.sio.write('打卡成功\n')
            print('打卡成功')
        elif '登录' in res.text:
            self.sio.write('Cookie失效\n')
            print('Cookie失效')
            return
        elif '重复' in res.text:
            self.sio.write('重复打卡\n')
            print('重复打卡')
        elif '已过打卡' in res.text:
            self.sio.write('已过打卡时间\n')
            print('已过打卡时间')
        else:
            self.sio.write('未知错误\n')
            print('未知错误')
        self.data = {'button4': ''}
        res = requests.post(url=url, headers=headers, data=self.data)
        soup = BeautifulSoup(res.text, "html.parser")
        alert = soup.select(".alert")
        print(alert[0].get_text()) if len(alert)>0 else print("获取失败")
        if '您本月还未打卡' in res.text or '无法获得全勤奖励' in res.text:
            print(re.findall('您本月打卡次数：\d+', res.text)[0])
            # print('月打卡次数不满足要求')
        elif '请勿重复领取' in res.text:
            print('本月全勤奖励已领取')
        else:
            print(res.text)

    def SignIn(self):
        print("【爱好论坛 日志】")
        self.sio.write("【爱好论坛】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            t = datetime.datetime.now()
            if t.hour == 8:
                self.data = {'button1': ''}
            elif t.hour == 13:
                self.data = {'button2': ''}
            elif t.hour == 18:
                self.data = {'button3': ''}
            else:
                self.sio.write('不在打卡时间\n')
                print('不在打卡时间')
                continue
            try:
                self.daka()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('AiHao')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            aihao = AiHao(Cookies['cookies'])
            sio = aihao.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('爱好论坛', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 爱好论坛 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 爱好论坛')