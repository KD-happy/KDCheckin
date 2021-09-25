# 青龙签到

拉取本站
```
ql repo https://github.com/KD-happy/QingLongCheckin.git "Cloud" "" "KDconfig.py"
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