# -*- coding: utf-8 -*-
"""
cron: 55 7 * * *
new Env('天翼云盘');
"""

import requests, time, re
from io import StringIO
from KDconfig import getYmlConfig

class Cloud:
    def __init__(self, cookie):
        self.dio = StringIO()
        self.sio = StringIO()
        self.Cookies = cookie

    def Sign_in(self, name, cookie):
        rand = str(round(time.time()*1000))
        url0 = "https://api.cloud.189.cn/mkt/userSign.action?rand="+str(rand)+"&clientType=TELEANDROID&version=8.6.3&model=SM-G930K"
        url1 = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN"
        url2 = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN"
        header = {
            "Cookie": cookie,
            'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
            "Host" : "m.cloud.189.cn",
            "Accept-Encoding" : "gzip"
        }
        s = requests.get(url0, headers=header) #签到
        s1 = requests.get(url1, headers=header) #抽奖1
        s2 = requests.get(url2, headers=header) #抽奖2
        self.dio.write("\n"+ str(name) +": \n"+ s.text +"\n"+ s1.text)
        if "User_Not_Chance" in str(s1.json()):
            s = "签到得"+ str(s.json()["netdiskBonus"]) +"M，两次抽奖机会已用完"
            self.sio.write("\n"+ str(name) +": "+ s)
        else:
            if "天翼云盘" in str(s1.json()):
                Obj = re.search(r"天翼云盘(.*)空间", s1.text, re.M|re.I)
                s1 = Obj.group(1)
                Obj = re.search(r"天翼云盘(.*)空间", s2.text, re.M|re.I)
                s2 = Obj.group(1)
                text = "签到得" + str(s.json()["netdiskBonus"]) +"M, 抽奖得: "+ s1 +"+"+ s2
                self.sio.write("\n"+ str(name) +": "+text)
            else:
                text = "Cookie失效"
                self.sio.write("\n"+ str(name) +": "+text)

    def Sign_in_TV(self, name, familyId, header):
        url = f"http://api.cloud.189.cn/family/manage/exeFamilyUserSign.action?familyId={familyId}"
        res = requests.get(url, headers=header)
        self.dio.write("\n"+ name +" TV: \n"+ res.text)
        Obj = re.search(r"<bonusSpace>(.*)</bonusSpace>", res.text, re.M|re.I)
        if Obj:
            text = name + " TV: 签到得" + Obj.group(1) + "M"
        else:
            text = name + " TV: Cookie失效"
        self.sio.write("\n" + text)

    def SignIn(self):
        self.dio.write("【天翼云盘 日志】")
        self.sio.write("【天翼云盘】")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            try:
                self.Sign_in(cookie.get('name'), cookie.get('cookie'))
            except BaseException as e:
                self.dio.write(f"\n{cookie.get('name')}: {e}")
            if cookie.get('TV') != None:
                try:
                    self.Sign_in_TV(cookie.get('name'), cookie.get('familyId'), cookie.get('header'))
                except BaseException as e:
                    print(e)
        return self.dio, self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Cloud')
    if Cookies != None:
        cloud = Cloud(Cookies)
        dio, sio = cloud.SignIn()
        print(dio.getvalue())
        print("\n\n")
        print(sio.getvalue())
    else:
        print('配置文件没有 天翼云盘')