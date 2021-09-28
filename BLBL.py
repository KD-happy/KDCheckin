# -*- coding: utf-8 -*-
"""
cron: 5 6 * * *
new Env('哔哩哔哩');
"""

"""
后续会弄: 投币, 直播弹幕, 直播礼物, 分区的使用
"""

from datetime import date
import requests, time, re, json, sys, traceback
from io import StringIO
from requests.api import head

from requests.models import cookiejar_from_dict
from KDconfig import getYmlConfig, send

class BLBL:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
        self.bili_jct = ''
        self.title = ''
        self.bvid = ''
        self.money0 = 0
        self.money1 = 0
        self.current_exp0 = 0
        self.current_exp1 = 0

    # 获取基本信息
    def nav(self):
        # uname：名字
        # mid：用户id
        # isLogin：判断是否登录
        # money：硬币
        # vipType：会员类型
        # current_exp：经验
        # bcoin_balance：B币
        url = 'https://api.bilibili.com/x/web-interface/nav'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        res = requests.get(url=url, headers=headers)
        data = res.json()
        print(data)
        if data.get('code') != 0:
            self.sio.write(f'{self.name}: Cookie失效\n')
            print(f'{self.name}: Cookie失效')
            return False
        elif '账号信息' not in self.sio.getvalue():
            name = data.get('data', {}).get('uname')
            self.sio.write(f'账号信息: {name}\n')
            self.money0 = data.get('data', {}).get('money')
            self.current_exp0 = data.get('data', {}).get('level_info', {}).get('current_exp')
        else:
            self.money1 = data.get('data', {}).get('money')
            self.current_exp1 = data.get('data', {}).get('level_info', {}).get('current_exp')
            print(f'硬币比: {self.money0}/{self.money1}')
            self.sio.write(f'硬币比: {self.money0}/{self.money1}\n')
            print(f'经验比: {self.current_exp0}/{self.current_exp1}')
            self.sio.write(f'经验比: {self.current_exp0}/{self.current_exp1}\n')
        return True

    # *分享视频
    def share(self):
        # 感觉 csrf=cookie.bili_jct 这个参数没用
        url = 'https://api.bilibili.com/x/web-interface/share/add'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        data = {
            "bvid": self.bvid,
            "csrf": self.bili_jct
        }
        res = requests.post(url=url, headers=headers, data=data)
        print(res.text)
        if res.json().get('code') == 0:
            self.sio.write(f'分享任务: 分享《{self.title}》成功\n')
            print(f'分享任务: 分享《{self.title}》成功')
            return True
        return False

    # 获取分区视频的相关消息
    def newlist(self):
        # ps: 一页显示的视频数, rid: 分区号, 
        url = 'https://api.bilibili.com/x/web-interface/newlist?rid=20&type=0&pn=3&ps=20'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
    
    # 获取动态的视频
    def dynamic_new(self):
        # 视频动态的获取链接
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?type_list=8'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36    ",
        }
        res = requests.get(url=url, headers=headers)
        data = res.json()
        for da in data.get('data', {}).get('cards', []):
            self.bvid = da.get('desc', {}).get('bvid', '')
            if self.bvid != '':
                self.title = json.loads(da.get('card')).get('title', '标题获取失败')[:10]
                if self.share():
                    break
        print(self.bvid, self.title)

    # 直播签到
    def live_sign(self):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36    ",
        }
        res = requests.get(url=url, headers=headers)
        data = res.json()
        print(data)
        if data.get('code') == 0:
            self.sio.write(f'直播签到: 获得 {data.get("data", {}).get("text")}\n')
            print(f'直播签到: 获得 {data.get("data", {}).get("text")}')
        else:
            if '重复签到' in data.get('message'):
                self.sio.write('直播签到: 重复签到\n')
                print('直播签到: 重复签到')
            else:
                self.sio.write('直播签到: Cookie失效\n')
                print('直播签到: Cookie失效')
    
    # 漫画签到
    def manga_sign(self):
        url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
        data = {"platform": "android"}
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36    ",
        }
        res = requests.post(url=url, headers=headers, data=data)
        data = res.json()
        print(data)
        if data["code"] == 0:
                msg = "签到成功"
        elif data["msg"] == "clockin clockin is duplicate":
            msg = "重复签到"
        else:
            msg = 'Cookie失效'
        print(f'漫画签到: {msg}')
        self.sio.write(f'漫画签到: {msg}\n')

    def SignIn(self):
        print("【哔哩哔哩 日志】")
        self.sio.write("【哔哩哔哩】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.name = cookie.get('name')
            self.cookie = cookie.get('cookie')
            self.bili_jct = cookie.get('bili_jct')   
            try:
                if self.nav():
                    self.live_sign()
                    time.sleep(1)
                    self.manga_sign()
                    time.sleep(1)
                    self.dynamic_new()
                    time.sleep(1)
                    self.nav()
            except:
                self.sio.write(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('BLBL')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            bibi = BLBL(Cookies['cookies'])
            sio = bibi.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('哔哩哔哩', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 哔哩哔哩 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 哔哩哔哩')