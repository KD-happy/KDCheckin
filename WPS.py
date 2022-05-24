# -*- coding: utf-8 -*-
"""
cron: 12 6 * * *
new Env('WPS签到');
"""

import requests, time, random, json, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send

class WPS:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    # 判断Cookie是否失效 和 今日是否签到
    def is_sign(self):
        url0 = 'https://vip.wps.cn/sign/mobile/v3/get_data'
        headers = {
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586"
        }
        res = requests.get(url=url0, headers=headers)
        if '会员登录' in res.text:
            print('Cookie失效')
            self.sio.write('Cookie失效\n')
            return False
        is_sign = res.json().get('data', {}).get('is_sign')
        if is_sign:
            print('今日已签到')
            self.sio.write('今日已签到\n')
            return False
        else:
            return True

    def Sign_in(self):
        url = "https://vip.wps.cn/sign/v2"
        yz_url = "https://vip.wps.cn/checkcode/signin/captcha.png?platform=8&encode=0&img_witdh=275.164&img_height=69.184"
        headers = {
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586"
        }
        if self.is_sign():
            data0 = {"platform":"8"}  #不带验证坐标的请求
            data = {"platform":"8",
                "captcha_pos":"137.00431974731889, 36.00431593261568",
                "img_witdh":"275.164",
                "img_height":"69.184"
            }  #带验证坐标的请求
            res = requests.post(url=url, headers=headers, data=data0)
            print(res.text)
            if not ("msg" in res.text):
                print('Cookie失效')
                self.sio.write('Cookie失效\n')
            else:
                sus = json.loads(res.text)["result"]
                print("免验证签到-->" + sus)
                if sus == "error":
                    for n in range(10):
                        requests.get(url=yz_url,headers=headers)
                        res = requests.post(url=url,headers=headers,data=data)
                        sus = json.loads(res.text)["result"]
                        print(str(n+1) + "尝试验证签到-->" + sus)
                        time.sleep(random.randint(0,5)/10)
                        if sus=="ok":
                            print(res.text)
                            break
                print("最终签到结果-->" + sus)
                self.sio.write(sus+'\n')
                # {"result":"ok","data":{"exp":0,"wealth":0,"weath_double":0,"count":5,"double":0,"gift_type":"space_5","gift_id":133,"url":""},"msg":""}

    def SignIn(self):
        print("【WPS签到 日志】")
        self.sio.write("【WPS签到】\n")
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
    Cookies = config.get('WPS')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            wps = WPS(Cookies['cookies'])
            sio = wps.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('WPS签到', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 WPS签到 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 WPS签到')