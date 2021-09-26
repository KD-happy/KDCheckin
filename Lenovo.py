"""
cron: 2 6 * * *
new Env('联想商城');
"""
import requests, sys, re
from io import StringIO
from KDconfig import getYmlConfig, send

dio = StringIO()

HEADER_GET = {
    "user-agent": "Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36/lenovoofficialapp/16112154380982287_10181446134/newversion/versioncode-124/"
}

HEADER_COUNT = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
}

class Lenovo:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.token = ''
        self.cookie = ''

    def signin(self):
        url = 'https://club.lenovo.com.cn/sign'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'referer': 'https://club.lenovo.com.cn/signlist/',
            'cookie': self.cookie,
        }
        res = requests.post(url, headers=headers, data={'_token': self.token})
        check = res.json()
        print(check)
        if "true" in check:
            if "乐豆" in check:
                print("签到成功")
                self.sio.write("签到成功\n")
            else:
                print("请不要重复签到")
                self.sio.write("重复签到\n")
        else:
            print("签到失败，请重试")
            self.sio.write("签到失败，请重试\n")

    def SignIn(self):
        print("【联想商店 日志】")
        self.sio.write("【联想商店】\n")
        for cookie in self.Cookies:
            try:
                cookie = cookie.get("user")
                self.cookie = cookie['cookie']
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'referer': 'https://club.lenovo.com.cn/signlist/',
                    'cookie': self.cookie,
                }
                res = requests.get('https://club.lenovo.com.cn/signlist/', headers=headers)
                self.token = re.findall('\$CONFIG\.token = "(.*)";', res.text)[0]
                print(self.token)
                self.sio.write(f'{cookie["name"]}: ')
                self.signin()
            except BaseException as e:
                print(f"{cookie.get('name')}: 异常 {e}\n")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Lenovo')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            lenovo = Lenovo(Cookies['cookies'])
            sio = lenovo.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('联想签到', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 联想签到 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 联想签到')