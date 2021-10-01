"""
cron: 0 6 * * *
new Env('AcFun');
"""

import requests, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send
import urllib3
urllib3.disable_warnings()

class AcFun:
    def __init__(self, cookie):
        self.Cookies = cookie
        self.check_items = cookie
        self.contentid = "27259341"
        self.cookies = ''
        self.sio = StringIO()
        self.session = requests.session()

    def get_cookies(session, phone, password):
        url = "https://id.app.acfun.cn/rest/app/login/signin"
        headers = {
            "Host": "id.app.acfun.cn",
            "user-agent": "AcFun/6.39.0 (iPhone; iOS 14.3; Scale/2.00)",
            "devicetype": "0",
            "accept-language": "zh-Hans-CN;q=1, en-CN;q=0.9, ja-CN;q=0.8, zh-Hant-HK;q=0.7, io-Latn-CN;q=0.6",
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }
        data = f"password={password}&username={phone}"
        response = session.post(
            url=url, data=data, headers=headers, verify=False)
        acpasstoken = response.json().get("acPassToken")
        auth_key = str(response.json().get("auth_key"))
        if acpasstoken and auth_key:
            cookies = {"acPasstoken": acpasstoken, "auth_key": auth_key}
            return cookies
        else:
            return False

    def get_token(self, cookies):
        url = "https://id.app.acfun.cn/rest/web/token/get"
        data = "sid=acfun.midground.api"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.session.post(url=url, cookies=cookies,
                                data=data, headers=headers, verify=False)
        return response.json().get("acfun.midground.api_st")

    def get_video(self):
        url = "https://www.acfun.cn/rest/pc-direct/rank/channel"
        data = "channelId=0&rankPeriod=DAY"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = self.session.post(url=url, data=data, headers=headers, verify=False)
        with open('ww.json', encoding='utf-8', mode='w') as file:
            file.write(response.text)
        self.contentid = response.json().get("rankList")[0].get("contentId")
        return self.contentid

    # 签到
    def sign(self, cookies):
        url = "https://www.acfun.cn/rest/pc-direct/user/signIn"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = self.session.post(
            url=url, cookies=cookies, headers=headers, verify=False)
        return response.json().get("msg")

    # 弹幕 修改版
    def danmu(self):
        url = "https://www.acfun.cn/rest/pc-direct/new-danmaku/add"
        body = "body=sitoi&color=16777215&id=27259341&mode=1&position=5019&size=25&subChannelId=84&subChannelName=%E4%B8%BB%E6%9C%BA%E5%8D%95%E6%9C%BA&type=douga&videoId=22898696"
        data = {
            'mode': '1',
            'color': '16777215',
            'size': '25',
            'body': '123321',
            'videoId': '26113662',
            'position': '2719',
            'type': 'douga',
            'id': '31224739',
            'subChannelId': '1',
            'subChannelName': '动画',
        }
        headers = {
            "cookie": self.cookie,
            'referer': 'https://www.acfun.cn/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        response = requests.post(url=url, data=data, headers=headers, verify=False)
        if response.json().get("result") == 0:
            msg = "弹幕成功"
        else:
            msg = "弹幕失败"
        return msg

    # 投蕉 修复版
    def throwbanana(self):
        url = "https://www.acfun.cn/rest/pc-direct/banana/throwBanana"
        data = {
            "resourceId": self.contentid,
            "count": "1",
            "resourceType": "2"
        }
        headers = {
            "cookie": self.cookie,
            'referer': 'https://www.acfun.cn/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        response = self.session.post(url=url, data=data, headers=headers, verify=False)
        print(self.contentid)
        print(response.text)
        if response.json().get("result") == 0:
            msg = "香蕉成功"
        else:
            msg = "香蕉失败"
        return msg

    # 点赞
    def like(self, token):
        like_url = "https://api.kuaishouzt.com/rest/zt/interact/add"
        unlike_url = "https://api.kuaishouzt.com/rest/zt/interact/delete"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        cookies = {"acfun.midground.api_st": token, "kpn": "ACFUN_APP"}
        body = f"interactType=1&objectId={self.contentid}&objectType=2&subBiz=mainApp"
        response = self.session.post(url=like_url, cookies=cookies,
                                data=body, headers=headers, verify=False)
        self.session.post(url=unlike_url, cookies=cookies,
                     data=body, headers=headers, verify=False)
        if response.json().get("result") == 1:
            msg = "点赞成功"
        else:
            msg = "点赞失败"
        return msg

    # 分享
    def share(self):
        url = "https://api-ipv6.app.acfun.cn/rest/app/task/reportTaskAction?taskType=1&market=tencent&product=ACFUN_APP&sys_version=8.0.0&app_version=6.42.0.1119&ftt=K-F-T&boardPlatform=hi3650&sys_name=android&socName=%3A%20HiSilicon%20Kirin%20950&ks_ipv6_cellular=2408%3A8470%3A8a03%3A526d%3A8017%3Acdeb%3A414%3Acbec&appMode=0"
        headers = {
            'cookie': self.cookie,
            'referer': 'https://www.acfun.cn/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        response = requests.get(url=url, headers=headers, verify=False)
        if response.json().get("result") == 0:
            msg = "分享成功"
        else:
            msg = "分享失败"
        return msg

    def SignIn(self):
        print("【AcFun 日志】")
        self.sio.write("【AcFun】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            try:
                self.name = cookie.get('name')
                self.cookie = cookie.get('cookie')
                cookies = {
                    item.split("=")[0]: item.split("=")[1]
                    for item in self.cookie.split("; ")
                }
                self.session = requests.session()

                self.get_video()
                token = self.get_token(cookies)

                sign_msg = self.sign(cookies) # 签到
                print(sign_msg)
                like_msg = self.like(token) # 点赞
                print(like_msg)
                share_msg = self.share() # 分享 失效
                print(share_msg)
                danmu_msg = self.danmu() # 弹幕
                print(danmu_msg)
                throwbanana_msg = self.throwbanana() # 投香蕉
                print(throwbanana_msg)

                msg = (
                    f"帐号信息: {self.name}\n"
                    f"签到状态: {sign_msg}\n"
                    f"点赞任务: {like_msg}\n"
                    f"弹幕任务: {danmu_msg}\n"
                    f"香蕉任务: {throwbanana_msg}\n"
                    f"分享任务: {share_msg}\n"
                )
                self.sio.write(msg)
            except:
                print(f"{self.name}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('AcFun')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            acfun = AcFun(Cookies['cookies'])
            sio = acfun.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('AcFun', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 AcFun 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 AcFun')