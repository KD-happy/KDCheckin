"""
cron: 10 6 * * *
new Env('欢太签到')
"""

import requests, time, re, json, sys
from io import StringIO
from KDconfig import getYmlConfig, send

class Heytap:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.session = requests.Session()
        self.name = ''
        self.ua = ''
        self.cookie = ''
    
    def SignIn(self):
        self.sio.write("【欢太商城】\n")
        print("【欢太商城】")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            self.ua = cookie.get("ua")
            self.name = cookie.get("name")
            self.cookie = cookie.get("cookie")
            try:
                if self.get_infouser() == False:
                    self.sio.write(f'{self.name}: Cookie失效\n')
                    continue
                else:
                    self.sio.write(f'{self.name}: \n')
                    self.daySign_task() #执行每日签到
                    self.daily_viewgoods() #执行每日商品浏览任务
                    self.daily_sharegoods() #执行每日商品分享任务
            except BaseException as e:
                self.sio.write(f"{self.name}: {e}\n")
        return self.sio
    
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
            print(response.text)
            result = response.json()
            if result['code'] == 200:
                print('【登录成功】: ' + result['data']['realName'])
                flag = True
            else:
                print('【登录失败】: ' + result['errorMessage'])
        except Exception as e:
            print('【登录】: 发生错误，原因为: ' + str(e))
        if flag:
            return True
        else:
            return False

    #任务中心列表，获取任务及任务状态
    def taskCenter(self):
        headers = {
            'Host': 'store.oppo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': self.ua,
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'cookie': self.cookie,
            'referer':'https://store.oppo.com/cn/app/taskCenter/index'
        }
        res1 = self.session.get('https://store.oppo.com/cn/oapi/credits/web/credits/show', headers=headers)
        res1 = res1.json()
        print(res1)
        return res1

    # 每日签到
    def daySign_task(self):
        try:
            dated = time.strftime("%Y-%m-%d")
            headers = {
            'Host': 'store.oppo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': self.ua,
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'cookie': self.cookie,
            'referer':'https://store.oppo.com/cn/app/taskCenter/index'
            }
            res = self.taskCenter()
            status = res['data']['userReportInfoForm']['status']
            if status == 0:
                res = res['data']['userReportInfoForm']['gifts']
                for data in res:
                    if data['date'] == dated:
                        qd = data
                if qd['today'] == False:
                    data = "amount=" + str(qd['credits'])
                    res1 = self.session.post('https://store.oppo.com/cn/oapi/credits/web/report/immediately', headers=headers,data=data)
                    res1 = res1.json()
                    if res1['code'] == 200:
                        self.sio.write('【每日签到成功】: ' + res1['data']['message'])
                        print('【每日签到成功】: ' + res1['data']['message'])
                    else:
                        self.sio.write('【每日签到失败】: ' + str(res1))
                        print('【每日签到失败】: ' + str(res1))
                else:
                    print(str(qd['credits']),str(qd['type']),str(qd['gift']))
                    if len(str(qd['type'])) < 1 :
                        data = "amount=" + str(qd['credits'])
                    else:
                        data = "amount=" + str(qd['credits']) + "&type=" + str(qd['type']) + "&gift=" + str(qd['gift'])
                    res1 = self.session.post('https://store.oppo.com/cn/oapi/credits/web/report/immediately',  headers=headers,data=data)
                    res1 = res1.json()
                    if res1['code'] == 200:
                        self.sio.write('【每日签到成功】: ' + res1['data']['message'] + '\n')
                        print('【每日签到成功】: ' + res1['data']['message'])
                    else:
                        self.sio.write('【每日签到失败】: ' + str(res1) + '\n')
                        print('【每日签到失败】: ' + str(res1))
            else:
                self.sio.write('【每日签到】: 已经签到过了！' )   
                print('【每日签到】: 已经签到过了！' )   
            time.sleep(1)
        except Exception as e:
            self.sio.write('【每日签到】: 错误，原因为: ' + str(e))
            print('【每日签到】: 错误，原因为: ' + str(e))

    #执行完成任务领取奖励
    def cashingCredits(self, info_marking, info_type, info_credits):
        headers = {
        'Host': 'store.oppo.com',
        'clientPackage': 'com.oppo.store',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': self.ua,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': self.cookie,
        'Origin': 'https://store.oppo.com',
        'X-Requested-With': 'com.oppo.store',
        'referer':'https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin'
        }

        data = "marking=" + str(info_marking) + "&type=" + str(info_type) + "&amount=" + str(info_credits)
        res = self.session.post('https://store.oppo.com/cn/oapi/credits/web/credits/cashingCredits', data=data, headers=headers)
        res = res.json()
        if res['code'] == 200:
            return True
        else:
            return False

    #浏览商品 10个sku +20 分
    #位置: APP → 我的 → 签到 → 每日任务 → 浏览商品
    def daily_viewgoods(self):
        try:
            headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
            'cookie': self.cookie,
            }
            res = self.taskCenter()
            res = res['data']['everydayList']
            for data in res:
                if data['name'] == '浏览商品':
                    qd = data
            if qd['completeStatus'] == 0:
                shopList = self.session.get('https://msec.opposhop.cn/goods/v1/SeckillRound/goods/115?pageSize=10&currentPage=1')
                res = shopList.json()
                if res['meta']['code'] == 200:
                    for skuinfo in res['detail']:
                        skuid = skuinfo['skuid']
                        print('正在浏览商品ID：', skuid)
                        self.session.get('https://msec.opposhop.cn/goods/v1/info/sku?skuId='+ str(skuid), headers=headers)
                        time.sleep(5)
                        
                    res2 = self.cashingCredits(qd['marking'],qd['type'],qd['credits'])
                    if res2 == True:
                        print('【每日浏览商品】: ' + '任务完成！积分领取+' + str(qd['credits']))
                        self.sio.write('【每日浏览商品】: ' + '任务完成！积分领取+' + str(qd['credits']) + '\n')
                    else:
                        self.sio.write('【每日浏览商品】: ' + "领取积分奖励出错！\n")
                        print('【每日浏览商品】: ' + "领取积分奖励出错！")
                else:
                    self.sio.write('【每日浏览商品】: ' + '错误，获取商品列表失败' + '\n')
                    print('【每日浏览商品】: ' + '错误，获取商品列表失败')
            elif qd['completeStatus'] == 1:
                res2 = self.cashingCredits(qd['marking'],qd['type'],qd['credits'])
                if res2 == True:
                    self.sio.write('【每日浏览商品】: ' + '任务完成！积分领取+' + str(qd['credits']) + '\n')
                    print('【每日浏览商品】: ' + '任务完成！积分领取+' + str(qd['credits']))
                else:
                    self.sio.write('【每日浏览商品】: ' + '领取积分奖励出错！\n')
                    print('【每日浏览商品】: ' + '领取积分奖励出错！')
            else:
                self.sio.write('【每日浏览商品】: ' + '任务已完成！\n')
                print('【每日浏览商品】: ' + '任务已完成！')
        except Exception as e:
            self.sio.write('【每日浏览任务】: 错误，原因为: ' + str(e) + '\n')
            print('【每日浏览任务】: 错误，原因为: ' + str(e) + '\n')

    # 执行每日商品分享任务
    def daily_sharegoods(self):
        try:
            headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
            'cookie': self.cookie,
            }
            daySignList = self.taskCenter()
            res = daySignList
            res = res['data']['everydayList']
            for data in res:
                if data['name'] == '分享商品到微信':
                    qd = data
            if qd['completeStatus'] == 0:
                count = qd['readCount']
                endcount = qd['times']
                while (count <= endcount):
                    self.session.get('https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_sharegoods', headers=headers)
                    count += 1
                res2 = self.cashingCredits(qd['marking'],qd['type'],qd['credits'])
                if res2 == True:
                    self.sio.write('【每日分享商品】: ' + '任务完成！积分领取+' + str(qd['credits']) + '\n')
                    print('【每日分享商品】: ' + '任务完成！积分领取+' + str(qd['credits']))
                else:
                    self.sio.write('【每日分享商品】: ' + '领取积分奖励出错！' + '\n')
                    print('【每日分享商品】: ' + '领取积分奖励出错！')
            elif qd['completeStatus'] == 1:
                res2 = self.cashingCredits(qd['marking'],qd['type'],qd['credits'])
                if res2 == True:
                    self.sio.write('【每日分享商品】: ' + '任务完成！积分领取+' + str(qd['credits']) + '\n')
                    print('【每日分享商品】: ' + '任务完成！积分领取+' + str(qd['credits']))
                else:
                    self.sio.write('【每日分享商品】: ' + '领取积分奖励出错！' + '\n')
                    print('【每日分享商品】: ' + '领取积分奖励出错！')
            else:
                self.sio.write('【每日分享商品】: ' + '任务已完成！' + '\n')
                print('【每日分享商品】: ' + '任务已完成！')
        except Exception as e:
            self.sio.write('【每日分享商品】: 错误，原因为: ' + str(e) + '\n')
            print('【每日分享商品】: 异常 错误，原因为: ' + str(e) + '\n')


if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Heytap')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            heytap = Heytap(Cookies['cookies'])
            sio = heytap.SignIn()
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