"""
cron: 10 6 * * *
new Env('欢太签到')
"""

from random import randint
import requests, time, traceback, sys
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
        self.if_draw = True
        self.act_task = [
            {
                "act_name": "赚积分",
                "aid": 1418,
                "if_task": True,  # 是否有任务
                "referer": "https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html?us=gerenzhongxin&um=hudongleyuan&uc=yingjifen",
                "if_draw": False,  # 是否有抽奖活动，已修复抽奖，如不需要抽奖请自行修改为False
                "extra_draw_cookie": 'app_innerutm={"uc":"yingjifen","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
                # 抽奖必要的额外cookie信息，请勿随意修改，否则可能导致不中奖
                "lid": 1307,  # 抽奖参数
                "draw_times": 3,  # 控制抽奖次数3
                "end_time": "2033-8-18 23:59:59",  # 长期任务
                "text": "每次扣取0积分，任务获取次数",
            },
            {
                "act_name": "realme积分大乱斗-8月",
                "aid": 1582,
                "if_task": True,
                "referer": "https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html",
                "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                "extra_draw_cookie": 'app_innerutm={"uc":"renwuzhongxin","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
                "lid": 1466,
                "draw_times": 3,
                "end_time": "2022-8-31 23:59:59",
                "text": "每次扣取5积分，测试仍然可以中奖",
            },
            {
                "act_name": "realme积分大乱斗-9月",
                "aid": 1582,
                "if_task": True,
                "referer": "https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html?&us=realmenewshouye&um=yaofen&ut=right&uc=realmedaluandou",
                "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                "extra_draw_cookie": 'app_innerutm={"uc":"renwuzhongxin","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
                "lid": 1554,  # 抽奖接口与8月不一样，测试可以独立抽奖
                "draw_times": 3,
                "end_time": "2022-8-31 23:59:59",
                "text": "每次扣取5积分",
            },
            {
                "act_name": "realme积分大乱斗-9月(2)",
                "aid": 1598,
                "if_task": True,
                "referer": "https://hd.oppo.com/act/m/2021/huantaishangchengjif/index.html?&us=realmeshouye&um=icon&ut=3&uc=realmejifendaluandou",
                "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
                "extra_draw_cookie": 'app_innerutm={"uc":"realmejifendaluandou","um":"icon","ut":"3","us":"realmeshouye"};',
                "lid": 1535,
                "draw_times": 3,
                "end_time": "2022-8-31 23:59:59",
                "text": "每次扣取10积分",
            },
            {
                "act_name": "天天积分翻倍",
                "aid": 675,
                "if_task": False,  # 该活动没有任务
                "referer": "https://hd.oppo.com/act/m/2019/jifenfanbei/index.html?us=qiandao&um=task",
                "if_draw": True,  # 已修复抽奖，如不需要抽奖请自行修改为False
                "extra_draw_cookie": 'app_innerutm={"uc":"direct","um":"zuoshangjiao","ut":"direct","us":"shouye"};',
                "lid": 1289,
                "draw_times": 1,
                "end_time": "2033-8-18 23:59:59",
                "text": "每次扣取10积分",
            }
        ]
    
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
                    self.sio.write(f'【用户信息】: {self.name}: Cookie失效\n')
                    continue
                else:
                    self.sio.write(f'【用户信息】: {self.name}\n')
                    self.daySign_task() #执行每日签到
                    self.daily_viewgoods() #执行每日商品浏览任务
                    self.daily_sharegoods() #执行每日商品分享任务
                    self.do_task_and_draw()  # 自己修改的接口，针对活动任务及抽奖，新增及删除活动请修改act_list.py
            except BaseException as e:
                self.sio.write(f"【用户信息】: {self.name}: {e}\n")
                print(traceback.format_exc())
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
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
            print('【登录】: 发生错误，原因为: ' + str(traceback.format_exc()))
            if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                self.sio.write('签到存在异常, 请自行查看签到日志\n')
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
        print(str(res1)[:200])
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
                        print('【每日签到失败】: ' + str(res1)[:200])
                else:
                    print(str(qd['credits']), str(qd['type']), str(qd['gift']))
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
                self.sio.write('【每日签到】: 已经签到过了！\n')   
                print('【每日签到】: 已经签到过了！' )   
            time.sleep(1)
        except Exception as e:
            self.sio.write('【每日签到】: 错误，原因为: ' + str(e) + '\n')
            print('【每日签到】: 错误，原因为: ' + str(traceback.format_exc()))
            if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                self.sio.write('签到存在异常, 请自行查看签到日志\n')

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
                shopList = self.session.get('https://msec.opposhop.cn/goods/v1/SeckillRound/goods/115?pageSize=12&currentPage=1')
                res = shopList.json()
                if res['meta']['code'] == 200:
                    for skuinfo in res['detail']:
                        skuid = skuinfo['skuid']
                        print('正在浏览商品ID：', skuid)
                        self.session.get('https://msec.opposhop.cn/goods/v1/info/sku?skuId='+ str(skuid), headers=headers)
                        time.sleep(randint(1, 5))
                        
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
            if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                self.sio.write('签到存在异常, 请自行查看签到日志\n')

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
            if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                self.sio.write('签到存在异常, 请自行查看签到日志\n')

    # 活动平台完成任务接口
    def task_finish(self, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Connection": "keep-alive",
            "User-Agent": self.ua,
            "Accept-Encoding": "gzip, deflate",
            "cookie": self.cookie,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest",
        }
        datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = self.session.post("https://hd.oppo.com/task/finish", data=datas, headers=headers)
        return res.json()

    # 活动平台领取任务奖励接口
    def task_award(self, aid, t_index):
        headers = {
            "Accept": "application/json, text/plain, */*;q=0.01",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Connection": "keep-alive",
            "User-Agent": self.ua,
            "Accept-Encoding": "gzip, deflate",
            "cookie": self.cookie,
            "Origin": "https://hd.oppo.com",
            "X-Requested-With": "XMLHttpRequest",
        }
        datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
        res = self.session.post("https://hd.oppo.com/task/award", data=datas, headers=headers)
        return res.json()

    # 活动平台抽奖通用接口
    def lottery(self, datas, referer="", extra_draw_cookie=""):
        headers = {
            "Host": "hd.oppo.com",
            "User-Agent": self.ua,
            "Cookie": extra_draw_cookie + self.cookie,
            "Referer": referer,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "br, gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        res = self.session.get("https://hd.oppo.com/user/login", headers=headers).json()
        if res["no"] == "200":
            res = self.session.post("https://hd.oppo.com/platform/lottery", data=datas, headers=headers)
            res = res.json()
            return res
        else:
            return res

    # 做活动任务和抽奖通用接口  hss修改
    def do_task_and_draw(self):
        try:
            for act_list in self.act_task:
                act_name = act_list["act_name"]
                aid = act_list["aid"]
                referer = act_list["referer"]
                if_draw = act_list["if_draw"]
                if_task = act_list["if_task"]
                end_time = act_list["end_time"]
                headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Connection": "keep-alive",
                    "User-Agent": self.ua,
                    "Accept-Encoding": "gzip, deflate",
                    "cookie": self.cookie,
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": referer,
                }
                dated = int(time.time())
                end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))  # 设置活动结束日期
                if dated < end_time and if_task:
                    res = self.session.get(f"https://hd.oppo.com/task/list?aid={aid}", headers=headers)
                    tasklist = res.json()
                    print(f"【{act_name}-任务】")
                    for i, jobs in enumerate(tasklist["data"]):
                        title = jobs["title"]
                        t_index = jobs["t_index"]
                        aid = t_index[: t_index.index("i")]
                        if jobs["t_status"] == 0:
                            finishmsg = self.task_finish(aid, t_index)
                            if finishmsg["no"] == "200":
                                time.sleep(1)
                                awardmsg = self.task_award(aid, t_index)
                                msg = awardmsg["msg"]
                                print(f"{title}：{msg}")
                                time.sleep(3)
                        elif jobs["t_status"] == 1:
                            awardmsg = self.task_award(aid, t_index)
                            msg = awardmsg["msg"]
                            print(f"{title}：{msg}")
                            time.sleep(3)
                        else:
                            print(f"{title}：任务已完成")
                    if self.if_draw and if_draw:  # 判断当前用户是否抽奖 和 判断当前活动是否抽奖
                        lid = act_list["lid"]
                        extra_draw_cookie = act_list["extra_draw_cookie"]
                        draw_times = act_list["draw_times"]
                        print(f"【{act_name}-抽奖】：")
                        x = 0
                        while x < draw_times:
                            data = f"aid={aid}&lid={lid}&mobile=&authcode=&captcha=&isCheck=0&source_type=501&s_channel=oppo_appstore&sku=&spu="
                            res = self.lottery(data, referer, extra_draw_cookie)
                            msg = res["msg"]
                            if "次数已用完" in msg:
                                print("  第" + str(x + 1) + "抽奖：抽奖次数已用完")
                                break
                            if "活动已结束" in msg:
                                print("  第" + str(x + 1) + "抽奖：活动已结束，终止抽奖")
                                break
                            goods_name = res["data"]["goods_name"]
                            if goods_name:
                                print(("  第" + str(x + 1) + "次抽奖：" + str(goods_name)))
                            elif "提交成功" in msg:
                                print("  第" + str(x + 1) + "次抽奖：未中奖")
                            x += 1
                            time.sleep(5)
                    else:
                        print(f'【{act_name}-抽奖关闭】')
                else:
                    print(f"【{act_name}】：活动已结束，不再执行")
        except Exception as e:
            print(str(traceback.format_exc()))
            print("【执行任务和抽奖】：错误，原因为: " + str(e))

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