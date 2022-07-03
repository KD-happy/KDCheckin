# KD签到

## 免责声明

- 本仓库发的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
- 本人无法100%保证使用本项目之后不会造成账号异常问题，若出现任何账号异常问题本人概不负责，请根据情况自行判断再下载执行！否则请勿下载运行！
- 如果任何单位或个人认为该项目的脚本可能涉及侵犯其权利，则应及时通知并提供相关证明，我将在收到认证文件后删除相关脚本。
- 任何以任何方式查看此项目的人或直接或间接使用本项目的任何脚本的使用者都应仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或本项目的规则，则视为您已接受此免责声明。

> 您使用或者复制了本仓库且本人制作的任何脚本，则视为 `已接受` 此声明，请仔细阅读

##  简单的操作

拉取本站
```shell
ql repo https://github.com/KD-happy/KDCheckin.git "AiHao|DuoKan|QianDao|Weather|News" "" "KD"
\cp -f /ql/data/repo/KD-happy_KDCheckin/*.py /ql/data/scripts/KD-happy_KDCheckin/KDsrc
```

将配置文件复制到指定位置

下面的是直接执行再服务器里面的，还要查看是否位置相同（映射到本地的位置）

```shell
cp /ql/repo/KD-happy_KDCheckin/Cookie.yml /ql/config/Cookie.yml
```

不行就直接再qinglong里面执行下面的命令

```shell
cp /ql/data/repo/KD-happy_KDCheckin/Cookie.yml /ql/data/config/Cookie.yml
```

```shell
ql repo <repourl> <path> <blacklist> <dependence> <branch>
        <库地址>   <拉哪些> <不拉哪些> <依赖文件>    <分支>
```

进入容器
```shell
docker exec -it qinglong bash
```

退出容器
```shell
exit
```

添加相关依赖 requirements.txt 文件里面有相关的导包，请自行安装

## 详细操作

**1.安装 docer**

[可以看一下](https://zhuanlan.zhihu.com/p/387337954)

更新 yum, 确保 yum 包更新到最新
``` shell
sudo yum update
```

安装的yum工具集
```shell
yum install -y yum-utils
```

安装docker-ce的yum源:
```shell
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
[可以看一下](https://blog.csdn.net/weixin_46152207/article/details/111354882)

安装docker-ce
```shell
dnf install docker-ce
```
或者yum安装
```shell
yum install docker-ce
```

查看docker服务状态
```shell
systemctl status docker.service
```

开启自启动
```shell
systemctl enable docker.service
```

开启服务
```shell
systemctl start docker.service
```

**2.安装**

拉取镜像文件
```shell
docker pull whyour/qinglong:latest
```

创建容器
```shell
docker run -dit \
  -v $pwd/ql:/ql/data \
  -p 5700:5700 \
  --name qinglong \
  --hostname qinglong \
  --restart unless-stopped \
  whyour/qinglong:latest
```

创建第二个容器
```shell
docker run -dit \
  -v $PWD/ql:/ql/data \
  -p 5800:5700 \
  --name qinglong \
  --hostname qinglong \
  --restart unless-stopped \
  whyour/qinglong:latest
```

## 腾讯云一键部署

```shell
curl https://cdn.jsdelivr.net/gh/KD-happy/KDCheckin@main/other/go.sh|bash
```

需要自行添加函数名

## 本仓库的文件配合

1. 支持根目录下的所有的签到单独执行
2. 支持由一个签到函数来调动其他的程序

> 由于技术限制，未实现的
> * 可以通过 Cookie.yml 配置文件中 signList 的参数来选取哪些需要签到

<details>
<summary>文件说明</summary>

```
│  AcFun.py            # AcFun
│  AiHao.py            # 爱好论坛
│  BDTieBa.py          # 百度贴吧
│  BLBL.py             # 哔哩哔哩
│  CCAVA.py            # CCAVA
│  Cloud.py            # 天翼云盘
│  Cookie.yml          # 签到配置文件
│  CSDN.py             # CSDN
│  Du163.py            # 网易读书
│  Duokan.py           # 多看阅读
│  EnShan.py           # 恩山论坛
│  HLX.py              # 葫芦侠
│  IQIYI.py            # 爱奇艺
│  KDconfig.py         # 文件读取、推送
│  Lenovo.py           # 联想
│  LenovoLTB.py        # 联想乐同步
│  Music163.py         # 网易云音乐
│  News.py             # 每日新闻
│  NoteYouDao.py       # 有道云笔记
│  PTA.py              # PTA
│  QianDao.py          # 多文件签到的入口程序
│  README.md
│  requirements.txt    # 导包依赖库
│  SMZDM.py            # 什么值得买
│  ToolLu.py           # Tool工具
│  VQQ.py              # 腾讯视频
│  W2PJ.py             # 吾爱破解
│  Weather.py          # 天气预报
│  WPS.py              # WPS签到
│  XMYD.py             # 小米运动
│  YHZWW.py            # 油猴中文网
│
├─KDsrc                # 多文件签到的程序文件夹
│      more.py         # map变量程序
│
└─other
        bt.sh          # 宝塔一键部署
        go.sh          # 腾讯云函数一键部署
        ql.sh          # 青龙一键部署
        模板.py         # 模板文件
```

</details>

## 推送配置

[企业微信应用通知粗略教程](http://note.youdao.com/noteshare?id=874fe7233f8cec295bb3d01d38296727&sub=16035CD41B844F179DA230AB9FC531D4)

[企业微信推送设置](http://note.youdao.com/noteshare?id=b7322046a431975dff59c75025e1d2f3&sub=9A27E09849CB414890CBC094B43A43EF)

[获取钉钉自定义机器人webhook](http://note.youdao.com/noteshare?id=25d15ba93ca80a29cfbf550078d096a8&sub=78340C89F0BB4295A4E559E12ED2EC83)

## Cookie.yml 简单介绍

```yaml
# AcFun  <-  支持签到的名称
AcFun:
  send: 0 # <-  是否发送通知 0: 不发送，1: 发送
  cookies: # <-  cookies列表
    - user: # <- 用户1
        name: 'xxx1' # <- 用户1名称（用来记录日志或发送通知的名称）
        # acPasstoken, auth_key # <- 关键cookie，必须有的cookie
        cookie: 'acPasstoken=xxxxxxx; auth_key=xxxxxx'
    - user: # <- 用户2
        name: 'xxx2' # <- 用户2名称（用来记录日志或发送通知的名称）
        # acPasstoken, auth_key
        cookie: 'acPasstoken=xxxxxxx; auth_key=xxxxxx'
```

对应的json格式

```json
{
  "AcFun": {
    "send": 0,
    "cookies": [
      {
        "user": {
          "name": "xxx1",
          "cookie": "acPasstoken=xxxxxxx; auth_key=xxxxxx"
        }
      },
      {
        "user": {
          "name": "xxx2",
          "cookie": "acPasstoken=xxxxxxx; auth_key=xxxxxx"
        }
      }
    ]
  }
}
```

## 支持的签到

🟢: 正常运行 🔴: 脚本暂不可用 🔵: 可以执行(需更新) 🟡: 待测试 🟤: 看脸
| 名称 | 备注 | 签到方式 | 来源 | 当前状态 |
| ---- | ---- | ---- | ---- | ---- |
| [天翼云盘](https://cloud.189.cn/web/main/) | 手机签到+抽奖、天翼云TV端 | cookie | 找不到 + 自制 | 🟢️ |
| 葫芦侠 | 签到所有的模板 | 手机号、密码 | [luck-ying01](https://github.com/luck-ying01/3floor_sign) | 🟢️ |
| [PTA](https://pintia.cn/market) | 每日签到 | cookie | 自制 | 🟢️ |
| [联想](https://club.lenovo.com.cn/signlist/) | 每日签到 | cookie | [silence4u](https://github.com/silence4u/lenovo_auto_signin) + 自制修改 | 🟢 |
| [多看阅读](https://www.duokan.com/) | 签到、延期、领书、看广告、下载任务 等 | cookie | [Sitoi](https://github.com/Sitoi/dailycheckin) | 🟢️ |
| [AcFun](https://www.acfun.cn/) | 签到、点赞、弹幕、香蕉 ~~、分享~~ | cookie | [Sitoi](https://github.com/Sitoi/dailycheckin) + 自制修改 | 🟢 |
| [吾爱破解](https://www.52pojie.cn/) | 签到、获取CB | cookie | 自制 + 模仿 | 🟢️ |
| [CCAVA](https://pc.ccava.net/) | 签到 | cookie | 自制 | 🔴 |
| [CSDN](https://www.csdn.net/) | 签到、抽奖 | cookie | 自制 + 模仿 | 🟢 |
| [爱好论坛](https://www.aihao.cc/) | 打卡 | cookie | 自制 | 🟢 |
| [恩山论坛](https://www.right.com.cn/forum/) | 签到 | cookie | 自制 + 模仿 | 🟢 |
| [哔哩哔哩](https://www.bilibili.com/) | 签到、看&分享视频、银瓜子兑硬币、发送直播弹幕、送免费辣条、礼物过期提醒 | cookie | [Sitoi](https://github.com/Sitoi/dailycheckin) + 自制修改 | 🟢 |
| [有道云笔记](https://note.youdao.com/web/) | 签到、看广告、空间大小 | cookie | 找不到 + 自制 | 🟢 |
| [Tool工具](https://tool.lu/) | 签到 | cookie | 自制 | 🟢 |
| [百度贴吧](https://tieba.baidu.com/) | 签到 | cookie | [Sitoi](https://github.com/Sitoi/dailycheckin) | 🟢 |
| [什么值得买](https://www.smzdm.com/) | 签到 | cookie | [Sitoi](https://github.com/Sitoi/dailycheckin) | 🟡 |
| [网易读书](https://du.163.com/) | 签到 | cookie | [Wenmoux](https://github.com/Wenmoux/checkbox/blob/master/scripts/du163.js) + 自制修改 | 🟢 |
| 小米运动 | 刷步数 | 手机号、密码 | [Sitoi](https://github.com/Sitoi/dailycheckin) | 🟢 |
| [网易云音乐](https://music.163.com/) | 签到 | cookie | 自制 | 🟢 |
| [天气预报](https://www.qweather.com/) | 每日天气推送、奇怪的知识 | city_id | 自制 | 🟢 |
| [爱奇艺](https://www.iqiyi.com/) | 签7天奖1天，14天奖2天，28天奖7天；日常任务4成长值；随机成长值；三次抽奖 | cookie | [Sitoi](https://github.com/Sitoi/dailycheckin) | 🟡 |
| [腾讯视频](https://v.qq.com/) | 每日两次腾讯视频签到获取成长值 | cookie、auth_refresh | [Sitoi](https://github.com/Sitoi/dailycheckin) | 🟡 |
| 每日新闻 | 每日新闻、历史上的今天 | ip（可无） | [自制](http://icheer.me/201910/1099/) | 🟢 |
| [乐同步](https://pim.lenovo.com/contact/contact/portal/home.html) | 每日签到 | cookie | 自制 | 🟢 |
| [WPS签到](https://vip.wps.cn/) | 签到领空间和积分 | cookie | 自制 | 🟡 |
| [油猴中文网](https://bbs.tampermonkey.net.cn/) | 签到 | cookie | 自制 | 🟢 |

## 已下架

🟢: 正常运行 🔴: 脚本暂不可用 🔵: 可以执行(需更新) 🟡: 待测试 🟤: 看脸
| 名称 | 备注 | 签到方式 | 来源 | 当前状态 |
| ---- | ---- | ---- | ---- | ---- |
| [欢太商城](https://www.heytap.com/cn/m/ucenter/index) | 每日签到、浏览商品、分享商品 | cookie | [hwkxk](https://github.com/hwkxk/HeytapTask) | 🔴 |
| 欢太早睡打卡 | 自动报名、自动打卡 | cookie | [Mashiro2000](https://github.com/Mashiro2000/HeyTapTask) | 🔴 |
| [爱助攻](https://www.aizhugong.com/) | 签到 | cookie | 自制 | 🔴 |
| 神代汉化组 | 签到&点赞 | cookie | 自制 | 🔴 |
| [企鹅电竞](https://egame.qq.com/) | 签到、疯狂打卡（报名和打卡）、领取任务奖励 | cookie | 自制 | 🔴 |

## 特别说明

1. send.send的值为 `0` 时, 集合签到和单独签到都不会有通知
2. 只有send.send的值为 `1` 和 单独签到的send的值为 `1` 时, 才会通知
3. signList的值 `不为空` 时, 集合签到只会签到signList规定的
4. 只有signList的值`为空` 时, 参数签到才可以使用。
5. 可通过指令 `python QianDao.py -h` 查看参数的使用
6. `-i` 或 `--include` : 签到包含什么, 其他的都不包含
7. `-e` 或 `--exclude` : 签到不包含什么, 包含的都是剩余的
8. `Cookie.yml` 文件中的cookie格式一定要符合条件, 用 `; ` 作为两个变量中间的分隔符