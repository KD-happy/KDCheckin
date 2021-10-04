# -*- coding: utf-8 -*-
"""
cron: 55 7 * * *
new Env('腾讯视频');
"""

import requests, time, re, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send
from urllib import parse

class VQQ:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''
        self.auth_refresh = ''

    def refresh_cookie(self, url, headers, cookies):
        login = requests.get(url=url, headers=headers, cookies=cookies)
        nick = re.findall(r'nick":"(.*?)"', login.text)
        if nick:
            nick = nick[0]
            try:
                nick = parse.unquote(nick)
            except Exception as e:
                print(f"nick 转换失败: {e}")
        else:
            nick = "未获取到用户"
        cookie = requests.utils.dict_from_cookiejar(login.cookies)
        return cookie, nick

    def sign_once(self, headers, cookies):
        url = "http://v.qq.com/x/bu/mobile_checkin?isDarkMode=0&uiType=REGULAR"
        res = requests.get(url=url, headers=headers, cookies=cookies)
        res.encoding = "utf8"
        match = re.search(r'isMultiple" />\s+(.*?)\s+<', res.text)
        if "isMultiple" in res.text:
            try:
                value = match.group(1)
            except Exception as e:
                print(res.text)
                value = "数据获取失败"
            msg = f"成长值x{value}"
        elif "Unauthorized" in res.text:
            msg = "cookie 失效"
        else:
            msg = "签到失败(可能已签到)\n签到失败: 自行在腾讯视频APP内登录网址签到 http://v.qq.com/x/bu/mobile_checkin (基本每周都需要手动签到一次才可以)"
        return msg

    def sign_twice(self, headers, cookies):
        this_time = int(round(time.time() * 1000))
        url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2&_=" + str(this_time)
        res = requests.get(url=url, headers=headers, cookies=cookies)
        res.encoding = "utf8"
        if "Account Verify Error" in res.text:
            msg = "签到失败-Cookie失效"
        elif "Not VIP" in res.text:
            msg = "非会员无法签到"
        else:
            try:
                value = re.search('checkin_score": (.*?),', res.text).group(1)
            except Exception as e:
                print("获取成长值失败", e)
                value = res.text
            msg = f"成长值x{value}"
        return msg

    def tasks(self, headers, cookies):
        task_map = {
            "1": "观看视频60min",
            "3": "使用弹幕特权",
            "6": "使用赠片特权",
            "7": "使用下载特权",
        }
        task_msg_list = []
        for task_id, task_name in task_map.items():
            this_time = int(round(time.time() * 1000))
            url = f"https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id={task_id}&_=${this_time}"
            res = requests.get(url=url, headers=headers, cookies=cookies)
            res.encoding = "utf8"
            if "score" in res.text:
                msg = f"获得+10成长值"
            elif "已发过货" in res.text:
                msg = "任务已完成"
            elif "任务未完成" in res.text:
                msg = "任务未完成，需手动完成任务"
            else:
                msg = res.text
            task_msg_list.append({"name": task_name, "value": msg})
            time.sleep(1)
        return task_msg_list

    def Sign_in(self):
        auth_refresh = self.auth_refresh
        if not auth_refresh:
            return "参数错误: 缺少 auth_refresh 参数，请查看配置文档"
        cookie = {item.split("=")[0]: item.split("=")[1] for item in self.cookie.split("; ")}
        headers = {
            "Referer": "https://v.qq.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36",
        }
        login_cookie, nick = self.refresh_cookie(url=auth_refresh, headers=headers, cookies=cookie)
        if login_cookie.get("main_login") == "qq":
            cookie["vqq_vusession"] = login_cookie.get("vqq_vusession")
        else:
            cookie["vusession"] = login_cookie.get("vusession")
            cookie["access_token"] = login_cookie.get("access_token")
        sign_once_msg = self.sign_once(headers=headers, cookies=cookie)
        sign_twice_msg = self.sign_twice(headers=headers, cookies=cookie)
        task_msg = self.tasks(headers=headers, cookies=cookie)
        msg = [
                  {"name": "用户信息", "value": nick},
                  {"name": "签到奖励1", "value": sign_once_msg},
                  {"name": "签到奖励2", "value": sign_twice_msg},
              ] + task_msg
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        print(msg)
        if '用户信息' in msg:
            self.sio.write('\n'+msg+'\n')
        else:
            self.sio.write(msg+'\n')

    def SignIn(self):
        print("【腾讯视频 日志】")
        self.sio.write("【腾讯视频】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            self.auth_refresh = cookie.get('auth_refresh')
            try:
                self.Sign_in()
            except:
                self.sio.write(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('VQQ')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            vqq = VQQ(Cookies['cookies'])
            sio = vqq.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('腾讯视频', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 腾讯视频 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 腾讯视频')