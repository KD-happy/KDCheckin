import yaml, os, requests, json

def getYmlConfig(yaml_file='Cookie.yml'):
    ql_file = '/ql/config/env.sh'
    cookie_file = '/ql/config/Cookie.yml'
    if os.path.exists(ql_file):
        if os.path.exists(cookie_file):
            file = open(cookie_file, 'r', encoding="utf-8")
        else:
            print('未找到Cookie的配置文件\n请执行下面的命令行\ncp /ql/repo/KD-happy_QingLongCheckin/Cookie.yml /ql/config/Cookie.yml')
            return {}
    else:
        if os.path.exists(yaml_file):
            file = open(yaml_file, 'r', encoding="utf-8")
        else:
            print('当前目录下没有配置文件Cookie.yml')
            return {}
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)

# ======================= 自定义推送函数 =============================
# https://docs.go-cqhttp.org/
def gocq(title, message, url):
    url += f'&message={message}'
    res = requests.get(url=url, timeout=3)
    if '"status":"ok"' in res.text:
        return True
    else:
        return False

# https://www.pushplus.plus/
def pushplus(title, message, token):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": message
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    res = requests.post(url, data=body, headers=headers)
    if res.json()['code'] == 200:
        return True
    else:
        return False

# https://pushplus.hxtrip.com/
def push(title, message, token):
    url = 'http://pushplus.hxtrip.com/send'
    data = {
        "token": token,
        "title": title,
        "content": message.replace('\n', '<br>')
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    res = requests.post(url, data=body, headers=headers)
    if '200' in res.text:
        return True
    else:
        return False

sendList = [gocq, pushplus, push] # 函数名
sendTokenList = ['gocq', 'pushplusToken', 'push+Token'] # 配置文件中的相关要素
sendMes = ['gocq', 'pushplus', 'push+'] # 未配置对的提示

# =============== 判断函数 和 发送入口 ======================

def pd(send, no):
    if send.get(sendTokenList[no]) != None:
        if send[sendTokenList[no]] != '':
            return True
        else:
            print(f'{sendMes[no]} 推送未配置, 推送失败')
    return False

def send(title, message):
    send = getYmlConfig()
    if send.get('send') != None:
        send = send['send']
    if send.get('send') != None:
        if send['send'] == 0:
            print('已关闭推送...')
            return
    else:
        print('配置文件有问题')
        return
    for i in range(len(sendList)):
        try:
            if pd(send, i) and sendList[i](title, message, send[sendTokenList[i]]):
                print(f'{sendMes[i]} 推送完成')
                if send.get('all') == None:
                    return
                if send['all'] == 0:
                    return
            else:
                print(f'{sendMes[i]} 推送失败')
        except Exception as e:
            print('异常: ' + e)