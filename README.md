# 青龙签到

##  简单的操作

拉取本站
```
ql repo https://github.com/KD-happy/QingLongCheckin.git "Cloud|Heytap|HLX|PTA|Lenovo" "KDsrc" "KDconfig.py"
```

将配置文件复制到指定位置
```
cp /ql/repo/KD-happy_QingLongCheckin/Cookie.yml /ql/config/Cookie.yml
```

```
ql repo <repourl> <path> <blacklist> <dependence> <branch>
        <库地址>   <拉哪些> <不拉哪些> <依赖文件>    <分支>
```

进入容器

```
docker exec -it qinglong bash
```

退出容器

```
exit
```

## 本仓库的文件配合

1. 支持根目录下的所有的签到单独执行
2. 支持由一个签到函数来调动其他的程序
  
```
│  Cloud.py            # 天翼云盘
│  Cookie.yml          # 签到配置文件
│  Heytap.py           # 欢太商城
│  HeytapSleep.py      # 欢太早睡打卡
│  HLX.py              # 葫芦侠
│  KDconfig.py         # 文件读取、推送
│  Lenovo.py           # 联想
│  PTA.py              # PTA
│  QianDao.py          # 多文件签到的入口程序
│  README.md
│  requirements.txt    # 导包依赖库
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
| 天翼云盘 | 手机签到+抽奖、天翼云TV端 | cookie | 🟢️ |
| 欢太商城 | 每日签到、浏览商品、分享商品 | cookie | [🟢️](https://github.com/hwkxk/HeytapTask) |
| 欢太早睡打卡 | 自动报名、自动打卡 | cookie | [🟢️](https://github.com/Mashiro2000/HeyTapTask) |
| 葫芦侠 | 签到所有的模板 | 手机号、密码 | [🟢️](https://github.com/luck-ying01/3floor_sign) |
| PTA | 每日签到 | cookie | 🟢️ |
| 联想 | 每日签到 | 手机号、密码 | [🟡](https://github.com/silence4u/lenovo_auto_signin) |