# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('每日新闻');
"""

import requests, time, re, json, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send

class News:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie

    def SignIn(self):
        print("【每日新闻 日志】")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"每日新闻 开始爬取中...")
            # self.sio.write(f"{cookie.get('name')}: ")
            try:
                res = requests.get(url = f'https://news.topurl.cn/api?ip={cookie.get("cookie")}').json()
                if res.get('code') == 200:
                    print(res)
                    data = res.get('data', {})
                    if data.get('newsList') != []:
                        self.sio.write("【每日新闻】\n")
                        no = 1
                        for news in data.get('newsList', []):
                            self.sio.write(f'{str(no).zfill(2)}: {news.get("title", "")}\n')
                            no += 1
                        self.sio.write('\n')
                    if data.get('historyList') != []:
                        self.sio.write('【历史上的今天】\n')
                        for history in data.get('historyList', []):
                            self.sio.write(f'{history.get("event", "")}\n')
            except:
                self.sio.write(f"每日新闻: 异常 {traceback.format_exc()}")
                if '存在异常, 请自行查看日志' not in self.sio.getvalue():
                    self.sio.write('存在异常, 请自行查看日志\n')
            break
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('News')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            cloud = News(Cookies['cookies'])
            sio = cloud.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('每日新闻', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 每日新闻 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 每日新闻')