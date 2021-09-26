"""
cron: 0 6 * * *
new Env('AcFun');
"""

import requests, sys
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
        response = self.session.post(
            url=url, data=data, headers=headers, verify=False)
        self.contentid = response.json().get("rankList")[0].get("contentId")
        return self.contentid

    def sign(self, cookies):
        url = "https://www.acfun.cn/rest/pc-direct/user/signIn"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = self.session.post(
            url=url, cookies=cookies, headers=headers, verify=False)
        return response.json().get("msg")

    def danmu(self, cookies):
        url = "https://www.acfun.cn/rest/pc-direct/new-danmaku/add"
        body = "body=sitoi&color=16777215&id=27259341&mode=1&position=5019&size=25&subChannelId=84&subChannelName=%E4%B8%BB%E6%9C%BA%E5%8D%95%E6%9C%BA&type=douga&videoId=22898696"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = self.session.post(url=url, cookies=cookies,
                                data=body, headers=headers, verify=False)
        if response.json().get("result") == 0:
            msg = "弹幕成功"
        else:
            msg = "弹幕失败"
        return msg

    def throwbanana(self, cookies):
        url = "https://www.acfun.cn/rest/pc-direct/banana/throwBanana"
        body = f"count=1&resourceId={self.contentid}&resourceType=2"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70"
        }
        response = self.session.post(url=url, cookies=cookies,
                                data=body, headers=headers, verify=False)
        if response.json().get("result") == 0:
            msg = "香蕉成功"
        else:
            msg = "香蕉失败"
        return msg

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

    def share(self, cookies):
        url = "https://api-ipv6.acfunchina.com/rest/app/task/reportTaskAction?taskType=1&market=tencent&product=ACFUN_APP&appMode=0"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.session.get(
            url=url, cookies=cookies, headers=headers, verify=False)
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

                sign_msg = self.sign(cookies)
                print(sign_msg)
                like_msg = self.like(token)
                print(like_msg)
                share_msg = self.share(cookies)
                print(share_msg)
                danmu_msg = self.danmu(cookies)
                print(danmu_msg)
                throwbanana_msg = self.throwbanana(cookies)
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
            except BaseException as e:
                print(f"{self.name}: 异常 {e}\n")
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