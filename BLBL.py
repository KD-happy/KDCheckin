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
        self.aid = ''
        self.mid = 0

    # 获取基本信息
    def nav(self):
        # uname: 名字
        # mid: 用户id
        # isLogin: 判断是否登录
        # money: 硬币
        # vipType: 会员类型
        # current_exp: 经验
        # bcoin_balance: B币
        url = 'https://api.bilibili.com/x/web-interface/nav'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        res = requests.get(url=url, headers=headers)
        data = res.json()
        self.mid = data.get('mid')
        print(str(data)[:500])
        if data.get('code') != 0:
            self.sio.write(f'{self.name}: Cookie失效\n')
            print(f'{self.name}: Cookie失效')
            return False
        else:
            name = data.get('data', {}).get('uname')
            self.sio.write(f'账号信息: {name}\n')
        return True

    # 获得今日获得的经验
    def reward(self):
        url = 'https://account.bilibili.com/home/reward'
        headers = {
            "cookie": f'DedeUserID={self.mid}; '+self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        res = requests.get(url=url, headers=headers).json()
        print(res)
        if res.get('code') == 0:
            data = res.get('data', {})
            login = data.get("login") # 登陆B站
            watch_av = data.get("watch_av") # 看视频
            coins_av = data.get("coins_av", 0) # 投币 +10 显示的是获得的经验
            share_av = data.get("share_av") # 分享视频
            today_exp = len([one for one in [login, watch_av, share_av] if one]) * 5
            today_exp += coins_av
            mes = f'今日经验: {today_exp}'
        else:
            mes = '今日经验: 获得失败'
        print(mes)
        self.sio.write(mes+'\n')
        

    # *分享视频
    def share(self):
        # 感觉 csrf=cookie.bili_jct 这个参数没用
        url = 'https://api.bilibili.com/x/web-interface/share/add'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        data = {
            "aid": self.aid,
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
        num = 6 # 获取视频数量
        rid = 1 # 分区号
        url = "https://api.bilibili.com/x/web-interface/dynamic/region?ps=" + str(num) + "&rid=" + str(rid)
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        res = requests.get(url=url, headers=headers).json()
        data_list = [
            {
                "aid": one.get("aid"),
                "cid": one.get("cid"),
                "title": one.get("title"),
                "owner": one.get("owner", {}).get("name"),
            }
            for one in res.get("data", {}).get("archives", [])
        ]
        return data_list
    
    # 看视频
    def report(self):
        url = "http://api.bilibili.com/x/v2/history/report"
        aid_list = self.newlist()
        aid = aid_list[0].get("aid")
        cid = aid_list[0].get("cid")
        title = aid_list[0].get("title")
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        post_data = {"aid": aid, "cid": cid, "progres": 300, "csrf": self.bili_jct}
        report_ret = requests.post(url=url, headers=headers, data=post_data).json()
        self.aid, self.title = aid, title
        print(report_ret)
        if report_ret.get("code") == 0:
            mes = f"观看视频: 观看《{title}》300秒"
        else:
            mes = "观看视频: 任务失败"
        print(mes)
        self.sio.write(mes+'\n')

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
            # self.sio.write(f"{cookie.get('name')}: ")
            self.name = cookie.get('name')
            self.cookie = cookie.get('cookie')
            self.bili_jct = cookie.get('bili_jct')
            try:
                if self.nav():
                    self.live_sign() # 直播签到
                    time.sleep(1)
                    self.manga_sign() # 漫画签到
                    time.sleep(1)
                    self.report() # 看视频
                    time.sleep(1)
                    self.share() # 分享视频
                    time.sleep(1)
                    self.reward() # 获取今日获得经验
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