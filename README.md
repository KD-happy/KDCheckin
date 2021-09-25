# 青龙签到

##  简单的操作

拉取本站
```
ql repo https://github.com/KD-happy/QingLongCheckin.git "Cloud" "KDsrc" "KDconfig.py"
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
│  KDconfig.py         # 文件读取、推送
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

| 名称 | 备注 | 当前状态 |
| ---- | ---- | ---- |
| 天翼云盘 | 1.手机签到+抽奖<br>2.天翼云TV端 | 🟢️ |
| 欢太商城 | 1.每日签到<br>2.浏览商品<br>3.分享商品 | 🟢️ |