# KD签到

##  简单的操作

拉取本站
```shell
ql repo https://github.com/KD-happy/KDCheckin.git "Cloud|Heytap|HLX|PTA|Lenovo|DuoKan|AcFun|W2PJ|AZG|Egame|CCAVA|CSDN|AiHao|EnShan" "KDsrc" "KDconfig.py"
```

将配置文件复制到指定位置
```shell
cp /ql/repo/KD-happy_KDCheckin/Cookie.yml /ql/config/Cookie.yml
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

## 详细操作

**1.安装 docer**

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
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/   linux/centos/docker-ce.repo
```

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
-v $pwd/ql/config:/ql/config \
-v $pwd/ql/log:/ql/log \
-v $pwd/ql/db:/ql/db \
-v $pwd/ql/scripts:/ql/scripts \
-v $pwd/ql/jbot:/ql/jbot \
-v $pwd/ql/repo:/ql/repo \
-p 5700:5700 \
-e ENABLE_HANGUP=true \
-e ENABLE_WEB_PANEL=true \
--name qinglong \
--hostname qinglong \
--restart always \
whyour/qinglong:latest
```

## 本仓库的文件配合

1. 支持根目录下的所有的签到单独执行
2. 支持由一个签到函数来调动其他的程序

> 由于技术限制，未实现的
> * 可以通过 Cookie.yml 配置文件中 signList 的参数来选取哪些需要签到
  
```
│  AcFun.py            # AcFun
│  AiHao.py            # 爱好论坛
│  AZG.py              # 爱助攻
│  CCAVA.py            # CCAVA
│  Cloud.py            # 天翼云盘
│  Cookie.yml          # 签到配置文件
│  CSDN.py             # CSDN
│  Duokan.py           # 多看阅读
│  Egame.py            # 企鹅电竞
│  EnShan.py           # 恩山论坛
│  Heytap.py           # 欢太商城
│  HeytapSleep.py      # 欢太早睡打卡
│  HLX.py              # 葫芦侠
│  KDconfig.py         # 文件读取、推送
│  Lenovo.py           # 联想
│  PTA.py              # PTA
│  QianDao.py          # 多文件签到的入口程序
│  README.md
│  requirements.txt    # 导包依赖库
│  W2PJ.py             # 吾爱破解
│  
└─KDsrc                # 多文件签到的程序文件夹
        Cloud.py
        HeytapTask.py
        more.py        # map变量程序
        模板.py         # 签到模板文件
```

## 支持的签到

🟢: 正常运行 🔴: 脚本暂不可用 🔵: 可以执行(需更新) 🟡: 待测试 🟤: 看脸
| 名称 | 备注 | 签到方式 | 当前状态 |
| ---- | ---- | ---- | ---- |
| [天翼云盘](https://cloud.189.cn/web/main/account) | 手机签到+抽奖、天翼云TV端 | cookie | 🟢️ |
| 欢太商城 | 每日签到、浏览商品、分享商品 | cookie | [🟢️](https://github.com/hwkxk/HeytapTask) |
| 欢太早睡打卡 | 自动报名、自动打卡 | cookie | [🟢️](https://github.com/Mashiro2000/HeyTapTask) |
| 葫芦侠 | 签到所有的模板 | 手机号、密码 | [🟢️](https://github.com/luck-ying01/3floor_sign) |
| [PTA](https://pintia.cn/market) | 每日签到 | cookie | 🟢️ |
| [联想](https://club.lenovo.com.cn/signlist/) | 每日签到 | cookie | [🟢](https://github.com/silence4u/lenovo_auto_signin) |
| [多看阅读](https://www.duokan.com/) | 签到、延期、领书、看广告、下载任务 等 | cookie | [🟢️](https://github.com/Oreomeow/checkinpanel/blob/master/ck_duokan.py) |
| [AcFun](https://www.acfun.cn/) | 签到、点赞、~~弹幕、香蕉、分享~~ | cookie | [🟢]([http](https://github.com/Oreomeow/checkinpanel/blob/master/ck_acfun.py)) |
| [吾爱破解](https://www.52pojie.cn/) | 签到、获取CB | cookie | 🟢️ |
| [爱助攻](https://www.aizhugong.com/) | 签到 | cookie | 🟢 |
| [企鹅电竞](https://egame.qq.com/) | 签到（后续任务未完成） | cookie | 🟢 |
| [CCAVA](https://pc.ccava.net/) | 签到 | cookie | 🟢 |
| [CSDN](https://www.csdn.net/) | 签到、抽奖 | cookie | 🟢 |
| [爱好论坛](https://www.aihao.cc/) | 打卡 | cookie | 🟢 |
| [恩山论坛](https://www.right.com.cn/forum/) | 签到 | cookie | 🟢 |