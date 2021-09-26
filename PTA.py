"""
cron: 6 6 * * *
new Env('PTA')
"""

import requests, sys
from io import StringIO
from KDconfig import getYmlConfig, send

dio = StringIO()

class PTA:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.name = ''
        self.cookie = ''

    def Sign_in(self):
        url = "https://pintia.cn/api/users/checkin"
        res = requests.post(url, headers={"Cookie": self.cookie})
        print(str(self.name) +": "+ res.text)
        if "TODO" in res.text:
            s = "重复签到"
        else: 
            if "DAILY_CHECK_IN" in res.text:
                s = "签到成功，获得5个金币"
            else:
                s = "Cookie失效"
        print(str(self.name) +": "+ s)
        self.sio.write(str(self.name) +": "+ s + "\n")

    def SignIn(self):
        print("【PTA签到 日志】")
        self.sio.write("【PTA签到】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            self.cookie = cookie['cookie']
            self.name = cookie['name']
            print(f'{self.name} 开始签到...')
            try:
                self.Sign_in()
            except BaseException as e:
                print(f"{self.name}: 异常 {e}\n")
        return self.sio


if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('PTA')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            pta = PTA(Cookies['cookies'])
            sio = pta.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('PTA', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 PTA 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 PTA')