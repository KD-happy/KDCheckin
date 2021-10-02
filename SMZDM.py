# -*- coding: utf-8 -*-
"""
cron: 55 7 * * *
new Env('{签到的标题}');
"""

import requests, time, re, json, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send

class SMZDM:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def sign(self, session):
        try:
            current = session.get(url="https://zhiyou.smzdm.com/user/info/jsonp_get_current").json()
            if current["checkin"]["has_checkin"]:
                msg = [
                    {"name": "用户信息", "value": current.get("nickname", "")},
                    {"name": "目前积分", "value": current.get("point", "")},
                    {"name": "当前经验", "value": current.get("exp", "")},
                    {"name": "当前金币", "value": current.get("gold", "")},
                    {"name": "碎银子数", "value": current.get("silver", "")},
                    {"name": "当前威望", "value": current.get("prestige", "")},
                    {"name": "当前等级", "value": current.get("level", "")},
                    {"name": "已经签到", "value": f"{current.get('checkin', {}).get('daily_checkin_num', '')} 天"},
                ]
            else:
                response = session.get(url="https://zhiyou.smzdm.com/user/checkin/jsonp_checkin").json().get("data", {})
                msg = [
                    {"name": "用户信息", "value": current.get("nickname", "")},
                    {"name": "目前积分", "value": current.get("point", "")},
                    {"name": "增加积分", "value": current.get("add_point", "")},
                    {"name": "当前经验", "value": current.get("exp", "")},
                    {"name": "当前金币", "value": current.get("gold", "")},
                    {"name": "当前威望", "value": current.get("prestige", "")},
                    {"name": "当前等级", "value": current.get("rank", "")},
                    {"name": "已经签到", "value": f"{response.get('checkin_num', {})} 天"},
                ]
        except Exception as e:
            msg = [
                {"name": "签到状态", "value": "签到失败"},
                {"name": "错误信息", "value": str(e)},
            ]
        return msg

    def SignIn(self):
        print("【{签到的标题} 日志】")
        self.sio.write("【{签到的标题}】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            # self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                smzdm_cookie = {item.split("=")[0]: item.split("=")[1] for item in self.cookie.split("; ")}
                session = requests.session()
                requests.utils.add_dict_to_cookiejar(session.cookies, smzdm_cookie)
                session.headers.update(
                    {
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Connection": "keep-alive",
                        "Host": "zhiyou.smzdm.com",
                        "Referer": "https://www.smzdm.com/",
                        "Sec-Fetch-Dest": "script",
                        "Sec-Fetch-Mode": "no-cors",
                        "Sec-Fetch-Site": "same-site",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
                    }
                )
                msg = self.sign(session=session)
                msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
                print(msg)
                self.sio.write(f'{msg}\n')
            except:
                self.sio.write(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('SMZDM')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            smzdm = SMZDM(Cookies['cookies'])
            sio = smzdm.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('{签到的标题}', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 {签到的标题} 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 {签到的标题}')