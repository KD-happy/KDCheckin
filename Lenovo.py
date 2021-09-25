import requests, sys
from bs4 import BeautifulSoup
from io import StringIO
from KDconfig import getYmlConfig, send

dio = StringIO()

HEADER_GET = {
    "user-agent": "Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36/lenovoofficialapp/16112154380982287_10181446134/newversion/versioncode-124/"
}

HEADER_COUNT = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
}

class Lenovo:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.username = ''
        self.password = ''

    def login(self):       #登录过程
        url = "https://reg.lenovo.com.cn/auth/v3/dologin"
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "Host": "reg.lenovo.com.cn",
            "Referer": "https://www.lenovo.com.cn/"
        }
        data = {"account": self.username, "password": self.password, "ticket": "e40e7004-4c8a-4963-8564-31271a8337d8", "ps": 1}
        session = requests.Session()
        session.get('https://club.lenovo.com.cn/', headers=header)
        r = session.post(url, headers=header, data=data)
        if '账号或密码错误' not in r.text:       #若未找到相关cookie则返回空值
            return None
        return session

    def getContinuousDays(self, session):
        url = "https://club.lenovo.com.cn/signlist/"
        c = session.get(url, headers=HEADER_COUNT)
        soup = BeautifulSoup(c.text,"html.parser")
        day = soup.select("body > div.signInMiddleWrapper > div > div.signInTimeInfo > div.signInTimeInfoMiddle > p.signInTimeMiddleBtn")
        day = day[0].get_text()
        print(f'已连续签到 {day} 天')
        self.sio.write(f'已连续签到 {day} 天\n')

    def signin(self, session):
        signin = session.get("https://i.lenovo.com.cn/signIn/add.jhtml?sts=e40e7004-4c8a-4963-8564-31271a8337d8", headers=HEADER_GET)
        check = str(signin.text)
        if "true" in check:
            if "乐豆" in check:
                print("签到成功")
                self.sio.write("签到成功\n")
            else:
                print("请不要重复签到")
                self.sio.write("重复签到\n")
        else:
            print("签到失败，请重试")
            self.sio.write("签到失败，请重试\n")

    def SignIn(self):
        print("【联想商店 日志】")
        self.sio.write("【联想商店】\n")
        for cookie in self.Cookies:
            try:
                cookie = cookie.get("user")
                self.username = cookie["username"]
                self.password = cookie["password"]
                self.sio.write(f'{cookie["username"]}: \n')
                s = self.login()
                if not s:
                    self.sio.write('登录失败, 请检查账号密码\n')
                    print('登录失败, 请检查账号密码')
                else:
                    self.signin(s)
                    self.getContinuousDays(s)
            except BaseException as e:
                print(f"{cookie.get('name')}: 异常 {e}\n")
        return self.sio

if __name__ == '__main__':
    config = getYmlConfig('Cookie.yml')
    Cookies = config.get('Lenovo')
    if Cookies != None:
        if Cookies.get('cookies') != None:
            lenovo = Lenovo(Cookies['cookies'])
            sio = lenovo.SignIn()
            print(f'\n{sio.getvalue()}')
            if Cookies.get('send') != None and Cookies['send'] == 1:
                send('联想签到', sio.getvalue())
            else:
                print('推送失败: 关闭了推送 or send配置问题')
        else:
            print('配置文件 联想签到 没有 "cookies"')
            sys.exit()
    else:
        print('配置文件没有 联想签到')