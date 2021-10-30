import yaml, os, requests, json
import time, hmac, hashlib,  base64, urllib.parse

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

def ding(title, message, token):
    url = 'https://oapi.dingtalk.com/robot/send'
    if token.get('access_token') == '':
        print('ding 推送未配置, 推送失败')
        return False
    params = {
        'access_token': token.get('access_token')
    }
    if token.get('secret') != '':
        timestamp = str(round(time.time() * 1000))
        secret = token.get('secret')
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        params['sign'] = sign
        params['timestamp'] = timestamp
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": message.replace('\n', '\n\n')
        }
    }
    data = {"msgtype": "text", "text": {"content": message}}
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    res = requests.post(url=url, headers=headers, json=data, params=params)
    res.encoding = 'utf-8'
    if res.json()['errmsg'] == 'ok':
        return True
    else:
        return False

def qywx(title, message, token):
    qyextoken = token.replace(' ', '').split(',')
    corpid = qyextoken[0]
    agentid = qyextoken[1]
    corpsecret = qyextoken[2]
    touser = qyextoken[3]
    media_id = '2jtiZMCr8n2kIey-LH4Qj2lexpQKyn7cmbtgjNsiyVw3_a-eHWtOQPs1IswybpQ4V'
    if qyextoken[4] != '':
        media_id = qyextoken[4]
    res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
    token = res.json().get("access_token", False)
    data = {
        "touser": touser,
        "msgtype": "mpnews",
        "agentid": int(agentid),
        "mpnews": {
            "articles": [
                {
                    "title": title,
                    "thumb_media_id": media_id,
                    "author": "kdlong",
                    "content_source_url": "https://github.com/KD-happy/KDCheckin",
                    "content": message.replace("\n", "<br>"),
                    "digest": message,
                }
            ]
        },
    }
    res = requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", data=json.dumps(data))
    print(res.text)
    if res.json().get('errcode') == 0:
        return True
    return False

sendList = [gocq, pushplus, push, ding, qywx] # 函数名
sendTokenList = ['gocq', 'pushplusToken', 'push+Token', 'dingToken', 'qywxToken'] # 配置文件中的相关要素
sendMes = ['gocq', 'pushplus', 'push+', 'ding', 'qywx'] # 未配置对的提示

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
    while(message[-1] == '\n'):
        message = message[0:-1]
    for i in range(len(sendList)):
        try:
            if pd(send, i):
                if sendList[i](title, message, send[sendTokenList[i]]):
                    print(f'{sendMes[i]} 推送完成')
                    if send.get('all') == None:
                        return
                    if send['all'] == 0:
                        return
                else:
                    print(f'{sendMes[i]} 推送失败, 查看一下配置文件')
        except Exception as e:
            print('异常: ' + e)