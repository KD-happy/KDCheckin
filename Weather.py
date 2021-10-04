# -*- coding: utf-8 -*-
"""
cron: 30 6,13 * * *
new Env('天气预报');
"""

import requests, sys, traceback
from io import StringIO
from KDconfig import getYmlConfig, send

class Weather:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.city_id = ''

    def get_iciba_everyday(self):
        icbapi = 'http://open.iciba.com/dsapi/'
        eed = requests.get(icbapi)
        english = eed.json()['content']
        zh_CN = eed.json()['note']
        str = '\n【奇怪的知识】\n' + english + '\n' + zh_CN
        return str

    def getWeather(self):
        api = 'http://t.weather.itboy.net/api/weather/city/'             #API地址，必须配合城市代码使用
        tqurl = api + self.city_id
        response = requests.get(tqurl)
        d = response.json()         #将数据以json形式返回，这个d就是返回的json数据
        tdwt = ''
        if(d['status'] == 200):     #当返回状态码为200，输出天气状况
            print("城市：",d["cityInfo"]["parent"], d["cityInfo"]["city"])
            print("更新时间：",d["time"])
            print("日期：",d["data"]["forecast"][0]["ymd"])
            print("星期：",d["data"]["forecast"][0]["week"])
            print("天气：",d["data"]["forecast"][0]["type"])
            print("温度：",d["data"]["forecast"][0]["high"],d["data"]["forecast"][0]["low"])
            print("湿度：",d["data"]["shidu"])
            print("PM25:",d["data"]["pm25"])
            print("PM10:",d["data"]["pm10"])
            print("空气质量：",d["data"]["quality"])
            print("风力风向：",d["data"]["forecast"][0]["fx"],d["data"]["forecast"][0]["fl"])
            print("感冒指数：",d["data"]["ganmao"])
            print("温馨提示：",d["data"]["forecast"][0]["notice"],"。")

            tdwt = '【今日天气】\n城市：'+d['cityInfo']['parent']+' '+d['cityInfo']['city']+\
                '\n日期：'+d["data"]["forecast"][0]["ymd"]+' '+d["data"]["forecast"][0]["week"]+\
                '\n天气：'+d["data"]["forecast"][0]["type"]+\
                '\n温度：'+d["data"]["forecast"][0]["high"]+' '+d["data"]["forecast"][0]["low"]+\
                '\n湿度：'+d["data"]["shidu"]+\
                '\n空气质量：'+d["data"]["quality"]+\
                '\nPM2.5：' +str(d["data"]["pm25"]) + '\nPM10：' +str(d["data"]["pm10"]) +\
                '\n风力风向：'+d["data"]["forecast"][0]["fx"]+' '+d["data"]["forecast"][0]["fl"]+\
                '\n感冒指数：' +d["data"]["ganmao"] +\
                '\n温馨提示：'+d["data"]["forecast"][0]["notice"]+\
                '。\n[更新时间：'+d["time"]+']\n✁-----------------'+ self.get_iciba_everyday()
        self.sio.write(tdwt)
        

    def SignIn(self):
        print("【天气预报 日志】")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            # print(f"{cookie.get('name')} 开始签到...")
            # self.sio.write(f"{cookie.get('name')}: ")
            self.city_id = cookie.get('city_id')
            try:
                self.getWeather()
            except:
                self.sio.write(f"异常 {traceback.format_exc()}")
                if '天气获取异常异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('天气获取异常异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Weather')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            weather = Weather(Cookies['cookies'])
            sio = weather.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('天气预报', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 天气预报 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 天气预报')