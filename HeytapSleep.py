"""
cron: 45 17,19 * * *
new Env('欢太早睡打卡')
"""

import requests, re, json, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class HeytapSleep:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.session = requests.Session()
        self.name = ''
        self.ua = ''
        self.cookie = ''
        self.s_channel = "oppostore"
        self.source_type = "505"  # 初始化设置为505，会从cookie获取实际数据
        self.sa_distinct_id = ""
        self.sa_device_id = ""
        self.s_version = ""
        self.brand = "iPhone"  # 初始化设置为iPhone，会从cookie获取实际机型
    
    def SignIn(self):
        self.sio.write("【欢太早睡打卡】\n")
        print("【欢太早睡打卡】")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            self.ua = cookie.get("ua")
            self.name = cookie.get("name")
            self.cookie = cookie.get("cookie")
            self.get_cookie_data()
            try:
                if self.get_infouser() == False:
                    self.sio.write(f'【用户信息】: {self.name}: Cookie失效\n')
                    continue
                else:
                    self.sio.write(f'【用户信息】: {self.name}\n')
                    self.zaoshui_task()
            except BaseException as e:
                self.sio.write(f"【用户信息】: {self.name}: {e}\n")
        return self.sio
    
    # 获取cookie里的一些参数，部分请求需要使用到————hss修改
    def get_cookie_data(self):
        try:
            app_param = re.findall("app_param=(.*?)}", self.cookie)[0] + "}"
            app_param = json.loads(app_param)
            self.sa_device_id = app_param["sa_device_id"]
            self.brand = app_param["brand"]
            self.sa_distinct_id = re.findall(
                "sa_distinct_id=(.*?);", self.cookie)[0]
            self.source_type = re.findall(
                "source_type=(.*?);", self.cookie)[0]
            self.s_version = re.findall("s_version=(.*?);", self.cookie)[0]
            self.s_channel = re.findall("s_channel=(.*?);", self.cookie)[0]
        except Exception as e:
            print("获取Cookie部分数据失败，将采用默认设置，请检查Cookie是否包含s_channel，s_version，source_type，sa_distinct_id\n", e)
            self.s_channel = "ios_oppostore"
            self.source_type = "505"

    # 获取Cookie状态和用户个人信息
    def get_infouser(self):
        flag = False
        headers = {
            'Host': 'www.heytap.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': self.ua,
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'cookie': self.cookie
        }
        self.session = requests.Session()
        response = self.session.get('https://www.heytap.com/cn/oapi/users/web/member/info', headers=headers)
        response.encoding='utf-8'
        try:
            result = response.json()
            if result['code'] == 200:
                print('【登录成功】: ' + result['data']['realName'])
                flag = True
            else:
                print('【登录失败】: ' + result['errorMessage'])
        except Exception as e:
            print('【登录】: 异常 发生错误，原因为: ' + str(e) + '\n')
        if flag:
            return True
        else:
            return False

    def zaoshui_task(self):
        try:
            headers = {
                "Host": "store.oppo.com",
                "Connection": "keep-alive",
                "s_channel": self.s_channel,
                "utm_term": "direct",
                "utm_campaign": "direct",
                "utm_source": "direct",
                "ut": "direct",
                "uc": "zaoshuidaka",
                "sa_device_id": self.sa_device_id,
                "guid": self.sa_device_id,
                "sa_distinct_id": self.sa_distinct_id,
                "clientPackage": "com.oppo.store",
                "Cache-Control": "no-cache",
                "um": "hudongleyuan",
                "User-Agent": self.ua,
                "ouid": "",
                "Accept": "application/json, text/plain, */*",
                "source_type": self.source_type,
                "utm_medium": "direct",
                "brand": "iPhone",
                "appId": "",
                "s_version": self.s_version,
                "us": "gerenzhongxin",
                "appKey": "",
                "X-Requested-With": "com.oppo.store",
                "Referer": "https://store.oppo.com/cn/app/cardingActivities?utm_source=opposhop&utm_medium=task",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "cookie": self.cookie
            }
            res = self.session.get("https://store.oppo.com/cn/oapi/credits/web/clockin/applyOrClockIn", headers=headers).json()
            if "余额不足" in str(res):
                self.sio.write("【早睡打卡】: 申请失败，积分余额不足\n")
                print("【早睡打卡】\n申请失败，积分余额不足")
            else:
                applyStatus = res["data"]["applyStatus"]
                if applyStatus == 1:
                    self.sio.write("【早睡打卡】: 申请成功，请当天19:30-22:00手动打卡\n")
                    print("【早睡打卡】申请成功，请当天19:30-22:00手动打卡")
                if applyStatus == 0:
                    self.sio.write("【早睡打卡】: 申请失败，积分不足或报名时间已过\n")
                    print("【早睡打卡】申请失败，积分不足或报名时间已过")
                if applyStatus == 2:
                    self.sio.write("【早睡打卡】: 打卡成功，积分将于24:00前到账\n")
                    print("【早睡打卡】\n打卡成功，积分将于24:00前到账")
            # 打卡记录
            res = self.session.get("https://store.oppo.com/cn/oapi/credits/web/clockin/getMyRecord", headers=headers).json()
            if res["code"] == 200:
                record = res["data"]["everydayRecordForms"]
                self.sio.write("【早睡打卡记录】\n")
                print("【早睡打卡记录】")
                i = 0
                for data in record:
                    self.sio.write(data["everydayDate"] + "——" +\
                        data["applyClockInStatus"] + "——" +\
                        data["credits"] + "\n")
                    print(data["everydayDate"] + "——" +
                            data["applyClockInStatus"] + "——" +
                            data["credits"])
                    i += 1
                    if i == 4:  # 最多显示最近2条记录
                        break
        except Exception as e:
            self.sio.write("【早睡打卡】: 错误，原因为: " + str(e) + '\n')
            print("【早睡打卡】: 异常 错误，原因为: " + str(e) + "\n")

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Heytap')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            heytapSleep = HeytapSleep(Cookies['cookies'])
            sio = heytapSleep.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('欢太签到', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 欢太签到 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 欢太签到')