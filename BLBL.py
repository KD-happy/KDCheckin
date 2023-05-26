# -*- coding: utf-8 -*-
"""
cron: 5 6 * * *
new Env('哔哩哔哩');
"""

import requests, time, json, sys, traceback
from io import StringIO

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
        self.mID = 0
        self.tx = True # 提醒过期礼物
        self.free = True # 送免费礼物
        self.lt = False # 免费辣条
        self.room_id = '0'
        self.watch_av = False
        self.share_av = False
        self.coins = 0 # 已经投币
        self.coin = 0 # 需要投币
        self.idError = True

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
        if data.get('code') != 0:
            self.sio.write(f'{self.name}: Cookie失效\n')
            print(f'{self.name}: Cookie失效')
            return False
        else:
            name = data.get('data', {}).get('uname')
            self.sio.write(f'账号信息: {name}\n')
        return True

    # 获得今日获得的经验
    def reward(self, pd):
        url = 'https://api.bilibili.com/x/member/web/exp/reward'
        headers = {
            "cookie": f'DedeUserID={self.mid}; '+self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        res = requests.get(url=url, headers=headers).json()
        print(res)
        if res.get('code') == 0:
            data = res.get('data', {})
            login = data.get("login")          # 登陆B站
            self.watch_av = data.get("watch")    # 看视频
            coins = data.get("coins", 0) # 投币 +10 显示的是获得的经验
            self.coins = coins//10
            self.share_av = data.get("share")    # 分享视频
            today_exp = len([one for one in [login, self.watch_av, self.share_av] if one]) * 5
            today_exp += coins
            msg = f'今日经验: {today_exp}'
        else:
            msg = '今日经验: 获得失败'
        print(msg)
        if pd:
            self.sio.write(msg+'\n')

    # *分享视频
    def share(self):
        aid_list = self.newlist()
        aid = aid_list[0].get("aid")
        title = aid_list[0].get("title")
        # 感觉 csrf=cookie.bili_jct 这个参数没用
        url = 'https://api.bilibili.com/x/web-interface/share/add'
        headers = {
            "cookie": self.cookie,
            "referer": "https://www.bilibili.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        data = {
            "aid": aid,
            "csrf": self.bili_jct
        }
        res = requests.post(url=url, headers=headers, data=data)
        print(res.text)
        if res.json().get('code') == 0:
            self.sio.write(f'分享任务: 分享《{title}》成功\n')
            print(f'分享任务: 分享《{title}》成功')
            return True
        else:
            self.sio.write(f'分享任务: {res.json().get("message")}\n')
            print(f'分享任务: {res.json().get("message")}')
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
            msg = f"观看视频: 观看《{title}》300秒"
        else:
            msg = "观看视频: 任务失败"
        print(msg)
        self.sio.write(msg+'\n')

    # 获取动态的视频
    def dynamic_new(self):
        # 视频动态的获取链接
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?type_list=8'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
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

    # 获取牌子亲密度等消息
    def get_list_in_room(self):
        url = 'https://api.live.bilibili.com/fans_medal/v1/FansMedal/get_list_in_room'
        headers = {
            "cookie": self.cookie,
            "origin": "https://live.bilibili.com",
            "referer": "https://live.bilibili.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        res = requests.get(url=url, headers=headers).json()
        if res.get('code') == 0:
            data_list = [
                {
                    "target_name": one.get("target_name"), # 主播名称
                    "target_id": one.get("target_id"), # 主播id
                    "medal_name": one.get("medal_name"), # 徽章名称
                    "room_id": one.get("room_id"), # 房间id
                    "today_intimacy": one.get("today_intimacy"), # 今日亲密度
                }
                for one in res.get("data", {})
            ]
        return data_list

    # 发送直播弹幕
    def send_danmu(self, medal):
        # medal: json 主播相关消息
        url = 'https://api.live.bilibili.com/msg/send'
        data = {
            "bubble": "0", # 不知道的模式
            "msg": "打卡", # 内容
            "color": "16777215", # 字体颜色 默认普通弹幕 16777215
            "mode": "1", # 不知道的模式
            "fontsize": "25", # 字体大小
            "rnd": str(int(time.time())), # 时间戳
            "roomid": str(medal.get('room_id')), # 房间号
            "csrf": self.bili_jct, # cookie 中的bili_jct
            "csrf_token": self.bili_jct,
        }
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        res = requests.post(url=url, data=data, headers=headers).json()
        print(res)
        if res.get('code') != 0:
            return False
        else:
            return True

    # 获得背包中礼物
    def bag_list(self):
        url = 'https://api.live.bilibili.com/xlive/web-room/v1/gift/bag_list'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        res = requests.get(url=url, headers=headers).json()
        data_list = []
        if res.get('code') == 0:
            if res.get('data', {}).get('list') == None:
                return data_list
            data_list = [
                {
                    "bag_id": one.get("bag_id"),           # 礼物再礼物栏中的id
                    "gift_id": one.get("gift_id"),         # 礼物的id
                    "gift_name": one.get("gift_name"),     # 礼物名称
                    "gift_num": one.get("gift_num"),       # 礼物数量
                    "corner_mark": one.get("corner_mark"), # 礼物下标, 显示到期时间 
                }
                for one in res.get("data", {}).get('list', [])
            ]
        return data_list

    # 送礼物
    def sendBag(self, bag, gift_num):
        # bag: json 礼物列表, gitf_num: int 礼物个数
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        # 获取主播的相关消息
        res = requests.get(url=f'https://api.bilibili.com/x/space/acc/info?mid={self.mID}', headers=headers).json()
        if res.get('code') != 0:
            if self.idError:
                self.sio.write('mid配置: 主播ID错误\n')
                print('mid配置: 主播ID错误')
            self.idError = False
            return False
        url = 'https://api.live.bilibili.com/xlive/revenue/v1/gift/sendBag'
        data = {
            "uid": str(self.mid), # 用户的id
            "gift_id": str(bag.get('gift_id')), # 礼物的id
            "ruid": str(self.mID), # 主播的id
            "send_ruid": "0", # 不知道
            "gift_num": str(gift_num), # 礼物数量
            "bag_id": str(bag.get('bag_id')), # 礼物再礼物栏中的id
            "platform": "pc", # 送礼端
            "biz_code": "Live", # 直播状态
            "biz_id": str(res.get('data', {}).get('live_room', {}).get('roomid')), # 主播直播间id
            "rnd": str(int(time.time()*1000)), # 时间戳 毫秒级
            "storm_beat_id": "0", # 不知道
            "metadata": "", # 不知道
            "price": "0", # 不知道
            "csrf_token": self.bili_jct, # cookie 中的bili_jct
            "csrf": self.bili_jct,
        }
        res = requests.post(url=url, data=data, headers=headers).json()
        if res.get('code') == 0:
            print(res.get('data', {}).get('send_tips'))
            return True
        else:
            print('赠送失败')
            return False

    # 直播签到
    def live_sign(self):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
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

    # 银瓜子兑硬币
    def silver2coin(self):
        url = "https://api.live.bilibili.com/xlive/revenue/v1/wallet/silver2coin"
        headers = {
            "cookie": self.cookie,
            "referer": "https://link.bilibili.com/p/center/index",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        data = {
            'csrf_token': self.bili_jct,
            'csrf': self.bili_jct
        }
        res = requests.post(url=url, headers=headers, data=data)
        self.sio.write(f"银瓜子兑硬币: {res.json()['message']}\n")
        print(res.text)

    def getStatus(self):
        url = "https://api.live.bilibili.com/xlive/revenue/v1/wallet/getStatus"
        headers = {
            "cookie": self.cookie,
            "referer": "https://www.bilibili.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        res = requests.get(url=url, headers=headers)
        silver = res.json()['data']['silver']
        coin = res.json()['data']['coin']
        return res.json()['data']['silver_2_coin_left'] == 0, silver, coin

    def Coin(self):
        if self.coins >= self.coin:
            self.sio.write(f"投币任务: {self.coin}/{self.coins}\n")
            print(f"投币任务: {self.coin}/{self.coins}")
            return
        for item in self.newlist():
            num = self.coin - self.coins
            if num > 2:
                num = 2
            elif num <= 0:
                self.sio.write(f"投币任务: {self.coin}/{self.coins}\n")
                print(f"投币任务: {self.coin}/{self.coins}")
                return
            url = "https://api.bilibili.com/x/web-interface/coin/add"
            data = {
                'aid': item['aid'],
                'multiply': num,
                'select_like': 1,
                'cross_domain': 'true',
                'csrf': self.bili_jct
            }
            headers = {
                "cookie": self.cookie,
                "referer": "https://www.bilibili.com",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            }
            res = requests.post(url=url, data=data, headers=headers)
            if res.json()['code'] == 0:
                print(f'{item["aid"]}: 投币成功')
                self.coins += num
            else:
                print(f'{item["aid"]}: 投币失败，{res.json()["message"]}')
        self.sio.write(f"投币任务: {self.coin}/{self.coins}\n")
        print(f"投币任务: {self.coin}/{self.coins}")

    def SignIn(self):
        print("【哔哩哔哩 日志】")
        self.sio.write("【哔哩哔哩】\n")
        for cookie in self.Cookies:
            self.idError = True
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.name = cookie.get('name')
            self.cookie = cookie.get('cookie')
            self.bili_jct = cookie.get('bili_jct')
            self.mID = cookie.get('mid', 0)
            self.coin = cookie.get('coin', 0)
            if self.coin > 5:
                self.coin = 5
            self.free = self.tx = True
            self.lt = self.watch_av = self.share_av = False
            try:
                if self.nav():
                    self.live_sign() # 直播签到
                    time.sleep(1)
                    self.manga_sign() # 漫画签到
                    time.sleep(1)
                    self.reward(False) # 获取今日任务
                    if not self.watch_av:
                        self.report() # 看视频
                        time.sleep(1)
                    else:
                        self.sio.write("观看视频: 今日已完成\n")
                        print("观看视频: 今日已完成")
                    if not self.share_av:
                        self.share() # 分享视频
                        time.sleep(1)
                    else:
                        self.sio.write("分享视频: 今日已完成\n")
                        print("分享视频: 今日已完成")
                    self.Coin() # 投币
                    time.sleep(1)
                    self.reward(True) # 获取今日获得经验
                    time.sleep(1)
                    if cookie.get('silver2coin', False):
                        pd, silver, coin = self.getStatus()
                        time.sleep(1)
                        if not pd:
                            self.silver2coin() # 银瓜子兑硬币
                            time.sleep(1)
                            pd, silver, coin = self.getStatus()
                            time.sleep(1)
                        else:
                            self.sio.write("银瓜子兑硬币: 今日已兑换\n")
                            print("银瓜子兑硬币: 今日已兑换")
                        self.sio.write(f"当前硬币和银币数: {coin}/{silver}\n")
                        print(f"当前硬币和银币数: {coin}/{silver}")
                    dataList = self.get_list_in_room() # 获得勋章列表

                    # 徽章列表直播间 发送弹幕
                    for one in dataList:
                        if one.get('today_intimacy') < 100:
                            if self.send_danmu(one):
                                msg = f"弹幕发送: 成功 {one.get('target_name')}"
                            else:
                                time.sleep(1)
                                if self.send_danmu(one):
                                    msg = f"弹幕发送: 成功 {one.get('target_name')}"
                                else:
                                    msg = f"弹幕发送: 失败 {one.get('target_name')}"
                            print(msg)
                            self.sio.write(msg+'\n')
                            time.sleep(1)
                    bagList = self.bag_list()

                    # 获取快过期的礼物 赠送免费礼物
                    for one in bagList:
                        if one.get('gift_name') == '辣条':
                            self.lt = True
                            time.sleep(1)
                            if self.sendBag(one, one.get('gift_num')):
                                if self.free:
                                    self.sio.write('免费礼物: 赠送成功\n')
                                    print('免费礼物: 赠送成功')
                                    self.free = False
                                time.sleep(1)
                                continue
                        if one.get('corner_mark') in ['1天', '2天'] and one.get('gift_name') != '辣条':
                            if self.tx:
                                self.sio.write('礼物提醒: 有快过期的礼物\n')
                                print('礼物提醒: 有快过期的礼物')
                                self.tx = False
                    else:
                        if self.free:
                            if self.lt:
                                print('免费礼物: 赠送失败')
                                self.sio.write('免费礼物: 赠送失败\n')
                            else:
                                print('免费礼物: 没有辣条')
                                self.sio.write('免费礼物: 没有辣条\n')
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
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