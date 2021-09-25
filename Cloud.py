"""
cron: 55 7 * * *
new Env('天翼云盘');
"""

import requests, time, re, json, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class Cloud:
    def __init__(self, cookie):
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
        print(str(name) + ": \n"+ s.text + "\n"+ s1.text)
        if "User_Not_Chance" in str(s1.json()):
            s = "签到得"+ str(s.json()["netdiskBonus"]) +"M，两次抽奖机会已用完"
            self.sio.write(str(name) + ": " + s + "\n")
        else:
            if "天翼云盘" in str(s1.json()):
                Obj = re.search(r"天翼云盘(.*)空间", s1.text, re.M|re.I)
                s1 = Obj.group(1)
                Obj = re.search(r"天翼云盘(.*)空间", s2.text, re.M|re.I)
                s2 = Obj.group(1)
                text = "签到得" + str(s.json()["netdiskBonus"]) +"M, 抽奖得: "+ s1 +"+"+ s2
                self.sio.write(str(name) +": "+text + "\n")
            else:
                text = "Cookie失效"
                self.sio.write(str(name) +": "+ text + "\n")

    def Sign_in_TV(self, name, familyId, header):
        url = f"http://api.cloud.189.cn/family/manage/exeFamilyUserSign.action?familyId={familyId}"
        res = requests.get(url, headers=header)
        print(name +" TV: \n"+ res.text)
        Obj = re.search(r"<bonusSpace>(.*)</bonusSpace>", res.text, re.M|re.I)
        if Obj:
            text = name + " TV: 签到得" + Obj.group(1) + "M"
        else:
            text = name + " TV: Cookie失效"
        self.sio.write(text + "\n")

    def SignIn(self):
        print("【天翼云盘 日志】")
        self.sio.write("【天翼云盘】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            try:
                self.Sign_in(cookie.get('name'), cookie.get('cookie'))
            except BaseException as e:
                print(f"{cookie.get('name')}: 异常 {e}\n")
            if cookie.get('TV') != None:
                try:
                    cookie = cookie.get('TV')
                    self.Sign_in_TV(cookie.get('name'), cookie.get('familyId'), json.loads(cookie.get('header')))
                except BaseException as e:
                    print(f"{cookie.get('name')}: 异常 {e}\n")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Cloud')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            cloud = Cloud(Cookies['cookies'])
            sio = cloud.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('天翼云签到', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 天翼云盘 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 天翼云盘')
