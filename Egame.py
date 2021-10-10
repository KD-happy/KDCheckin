# -*- coding: utf-8 -*-
"""
cron: 11 8 * * *
new Env('企鹅电竞');
"""

"""
后续会添加的
1. 午间/晚间 登录
2. 关注/取关主播 尽量
"""

import requests, sys, traceback, time
from io import StringIO
from KDconfig import getYmlConfig, send

class Egame:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    # 报名
    def attendance_sign_up(self, class_type, act_title):
        url = f'https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?pgg_gtk=1960736180&_={int(time.time()*1000)}&pgg_tk=1960736180&pgg_gtk=1960736180'
        data = {
            'param': '{"0":{"param":{"amt_type":1,"class_type":class_type_th},"module":"pgg_operation_activity_mt_svr","method":"attendance_sign_up"}}'.replace('class_type_th', str(class_type)),
            'app_info': '{"platform":4,"terminal_type":4,"version_code":"","version_name":"undefined","pvid":"907134976","ssid":"4238740480","imei":"0","qimei":"0"}',
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.post(url=url, data=data, headers=headers)
        print(res.text)
        retMsg = res.json().get('data', {}).get('0', {}).get('retMsg', '')
        print(f'报名-{act_title}: {retMsg}')
        self.sio.write(f'报名-{act_title}: {retMsg}\n')
    
    # 打卡
    def attendance_mark(self, signup_ts, class_type, act_title):
        url = f'https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?pgg_gtk=1960736180&_={int(time.time()*1000)}&pgg_tk=1960736180&pgg_gtk=1960736180'
        data = {
            'param': '{"0":{"param":{"amt_type":1,"class_type":class_type_th,"signup_ts":signup_ts_th},"module":"pgg_operation_activity_mt_svr","method":"attendance_mark"}}'.replace('signup_ts_th', str(signup_ts)).replace('class_type_th', str(class_type)),
            'app_info': '{"platform":4,"terminal_type":4,"version_code":"","version_name":"undefined","pvid":"907134976","ssid":"3056811008","imei":"0","qimei":"0"}',
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.post(url=url, data=data, headers=headers)
        print(res.text)
        retMsg = res.json().get('data', {}).get('0', {}).get('retMsg', '')
        print(f'打卡-{act_title}: {retMsg}')
        self.sio.write(f'打卡-{act_title}: {retMsg}\n')

    # 获取报名情况
    def get_attendance_status(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        for i in range(3):
            url = f'https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?pgg_gtk=1960736180&_={int(time.time()*1000)}&pgg_tk=1960736180&pgg_gtk=1960736180'
            data = {
                'param': '{"0":{"param":{"amt_type":1,"class_type":class_type_th},"module":"pgg_operation_activity_mt_svr","method":"get_attendance_status"}}'.replace('class_type_th', str(i+1)),
                'app_info': '{"platform":4,"terminal_type":4,"version_code":"","version_name":"undefined","pvid":"907134976","ssid":"855127040","imei":"0","qimei":"0"}',
            }
            res = requests.post(url=url, data=data, headers=headers).json()
            print(str(res))
            if res.get('uid') == 0:
                print('Cookie失效 退出报名打卡')
                return
            else:
                data = res.get('data', {}).get('0', {}).get('retBody', {}).get('data', {})
                prev = data.get('prev', {})
                curr = data.get('curr', {})
                if prev.get('join_status', 0) != 0: # 0: 未报名, 1: 报名?, 2: 要打卡? ,3: 打卡了?
                    print(f'打卡 加入状态:{prev.get("join_status")} 标题:{prev.get("act_title")} 时间戳:{prev.get("signup_ts")} 类型:{prev.get("class_type")}')
                    time.sleep(1)
                    self.attendance_mark(prev.get("signup_ts"), prev.get("class_type"), prev.get("act_title"))
                if curr.get('join_status') == 0 and str(i+1) in self.sign: # 0: 未报名, 1: 已报名,
                    print(f'报名 加入状态:{curr.get("join_status")} 标题:{curr.get("act_title")} 类型:{curr.get("class_type")}')
                    time.sleep(1)
                    self.attendance_sign_up(prev.get("class_type"), prev.get("act_title"))

    # 签到
    def signin(self):
        url = 'https://game.egame.qq.com/cgi-bin/pgg_async_fcgi?param={"key":{"module":"pgg.user_task_srf_svr.CPGGUserTaskSrfSvrObj","method":"OldUserCheckin","param":{}}}'
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "cookie": self.cookie
        }
        res = requests.get(url, headers=header)
        print(res.text)
        data = res.json()
        if data.get('uid') == 0:
            print('Cookie失效')
            self.sio.write('Cookie失效\n')
        elif data['data']['key']['retMsg'] == '成功':
            print(f"签到成功, 获得{data['data']['key']['retBody']['data']['award']['description']}")
            self.sio.write(f"签到成功, 获得{data['data']['key']['retBody']['data']['award']['description']}\n")
        else:
            print(data['data']['key']['retMsg'])
            self.sio.write(f"{data['data']['key']['retMsg']}\n")    

    def SignIn(self):
        print("【企鹅电竞 日志】")
        self.sio.write("【企鹅电竞】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: \n")
            self.cookie = cookie.get('cookie')
            self.sign = cookie.get('sign')
            try:
                self.signin()
                self.get_attendance_status()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Egame')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            egame = Egame(Cookies['cookies'])
            sio = egame.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('企鹅电竞', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 企鹅电竞 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 企鹅电竞')