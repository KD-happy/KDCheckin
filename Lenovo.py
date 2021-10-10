"""
cron: 2 6 * * *
new Env('联想商城');
"""

import requests, sys, re, traceback, time
from io import StringIO
from KDconfig import getYmlConfig, send

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
        if "success" in str(check):
            if "乐豆" in str(check):
                print(f"签到成功\n连续签到{check['data']['continueCount']}天")
                print(f"获得{check['data']['ledouValue']}乐豆, {check['data']['scoreValue']}积分")
                self.sio.write("签到成功\n")
                self.sio.write(f"连续签到{check['data']['continueCount']}天\n获得{check['data']['ledouValue']}乐豆, {check['data']['scoreValue']}积分\n")
            else:
                print("重复签到")
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
                self.sio.write(f'{cookie["name"]}: ')
                print(f'{cookie.get("name")} 开始签到...')
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'referer': 'https://club.lenovo.com.cn/signlist/',
                    'cookie': self.cookie,
                }
                res = requests.get('https://club.lenovo.com.cn/signlist/', headers=headers)
                test = re.findall('\$CONFIG\.token = "(.*)";', res.text)
                if test == []:
                    print('第二次尝试\n')
                    time.sleep(2)
                    res = requests.get('https://club.lenovo.com.cn/signlist/', headers=headers)
                    test = re.findall('\$CONFIG\.token = "(.*)";', res.text)
                if test == []:
                    self.token = ''
                else:
                    self.token = test[0]
                print(self.token)
                if self.token == '':
                    self.sio.write('Cookie失效\n')
                    continue
                self.signin()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
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