# -*- coding: utf-8 -*-
"""
cron: 10 6 * * *
new Env('乐同步');
"""

import requests, time, re, json, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send

class LenovoLTB:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
        self.totalSize = 0

    def LoginResponse(self):
        # url = 'https://uss.lenovomm.com/authen/1.2/st/getbycredential'
        url = 'https://passport.lenovo.com/authen/1.2/st/getbycredential'
        data = {
            'source': 'android:com.lenovo.leos.cloud.sync-5.0.70.99',
            'lang': 'zh-CN',
            'lpsutgt': self.cookie,
            'realm': 'contact.cloud.lps.lenovo.com',
            'packagename': 'com.lenovo.leos.cloud.sync',
            'packagesign': '',
            'appname': '乐同步',
        }
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; PCAM00 Build/RKQ1.201217.002)'
        }
        res = requests.post(url=url, headers=headers, data=data)
        # self.cookie = 'lenovoauth lpsust=' + re.findall('<Value>(.*)</Value>', res.text)[0]
        self.cookie = re.findall('<Value>(.*)</Value>', res.text)[0]

    def userinfo(self):
        url = 'https://pimapi.lenovomm.com/userspaceapi/storage/userinfo'
        headers = {
            'Authorization': f'LenovoAuth LPSUST="{self.cookie}"',
            'X-Lenovows-Authorization': f'LenovoAuth LPSUST="{self.cookie}"',
            "user-agent": "Mozilla/5.0 (Linux; Android 11; PCAM00 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 com.lenovo.leos.cloud.sync/6.3.0.99",
        }
        res = requests.post(url=url, headers=headers)
        if 'error' in res.text:
            self.sio.write('Cookie失效\n')
            print('Cookie失效')
        else:
            self.totalSize = res.json().get('data', {}).get('totalSize')//1048576

    # 签到
    def addspace(self):
        url = 'https://pim.lenovo.com/lesynch5/userspaceapi/v4/addspace'
        # url = 'https://pimapi.lenovomm.com/userspaceapi/v3/addspace'
        headers = {
            'Authorization': f'LenovoAuth LPSUST="{self.cookie}"',
            'X-Lenovows-Authorization': f'LenovoAuth LPSUST="{self.cookie}"',
            "user-agent": "Mozilla/5.0 (Linux; Android 11; PCAM00 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 com.lenovo.leos.cloud.sync/6.3.0.99",
        }
        res = requests.get(url=url, headers=headers)
        print(res.text)
        if 'spaceadd' in res.text:
            data = res.json()
            if 'lastspaceadd' in res.text:
                msg = f'今日以获{data.get("lastspaceadd")}M, 总空间{self.totalSize}M'
            else:
                msg = f'获得{data.get("spaceadd")}M, 总空间{self.totalSize + data.get("spaceadd")}M'
            self.sio.write(msg+'\n')
            print(msg)

    def SignIn(self):
        print("【乐同步 日志】")
        self.sio.write("【乐同步】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.LoginResponse()
                self.userinfo()
                self.addspace()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('LenovoLTB')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            ltb = LenovoLTB(Cookies['cookies'])
            sio = ltb.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('乐同步', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 乐同步 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 乐同步')