# -*- coding: utf-8 -*-
"""
cron: 2 6 * * *
new Env('有道云');
"""

import requests, time, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send

class NoteYouDao:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
        self.name = ''

    def getSpace(self):
        url = 'https://note.youdao.com/yws/mapi/user?method=get'
        headers = {
            'Cookie': self.cookie
        }
        res = requests.get(url=url, headers=headers)
        # print(res.text)
        if res.json().get('q') == None:
            return 0
        return res.json().get('q')

    def Sign_in(self):
        print(f'签到前空间: {self.getSpace()//1048576}')
        c = ''
        ad = 0
        headers = {'Cookie': self.cookie}
        r = requests.get('http://note.youdao.com/login/acc/pe/getsess?product=YNOTE', headers=headers)
        for key, value in r.cookies.items(): # 聪明的一批
            c += key + '=' + value + ';'
        headers = {'Cookie': c}
        re = requests.post("https://note.youdao.com/yws/api/daupromotion?method=sync", headers=headers)
        if 'error' not in re.text:
            res = requests.post("https://note.youdao.com/yws/mapi/user?method=checkin", headers=headers)
            for _ in range(3):
                resp = requests.post("https://note.youdao.com/yws/mapi/user?method=adRandomPrompt", headers=headers)
                ad += resp.json()['space'] // 1048576
                time.sleep(2)
            logs = re.text +"\n"+ res.text +"\n"+ resp.text
            print(logs)
            if 'reward' in re.text:
                s = self.getSpace()
                print(f'签到后空间: {s}')
                sync = re.json()['rewardSpace'] // 1048576
                checkin = res.json()['space'] // 1048576
                space = str(sync + checkin + ad)
                message = f'获得空间{space}M, 总空间{int(s)//1048576}M'
        else:
            message = "Cookie失效"
        print(message)
        self.sio.write(message + '\n')

    def SignIn(self):
        print("【有道云 日志】")
        self.sio.write("【有道云】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            self.name = cookie.get('name')
            try:
                self.Sign_in()
            except:
                self.sio.write(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('NoteYouDao')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            note = NoteYouDao(Cookies['cookies'])
            sio = note.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('有道云', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 有道云 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 有道云')