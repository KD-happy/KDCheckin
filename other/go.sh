#!/bin/bash
clear
file_name="script"
file_go="go.sh"
file_cookie="src/Cookie.yml"

# 创建script文件夹来存放clone的库
if [ ! -d $file_name ];then
    mkdir $file_name
    echo "创建目录完成"
fi

# 开始clone
cd script
git clone https://github.com/KD-happy/KDCheckin.git
echo "Clone完成"
cd ..

# 复制关键文件
if [ ! -f $file_cookie ];then
    \cp script/KDCheckin/Cookie.yml src/
    echo "Cookie.yml 文件复制成功"
else
    echo "如果添加功能了，要自行修改 Cookie.yml 文件"
fi
\cp -fr script/KDCheckin/KDsrc src/
\cp -f script/KDCheckin/*.py src/KDsrc/
\cp -f script/KDCheckin/QianDao.py src/
\cp -f script/KDCheckin/KDconfig.py src/
echo "复制成功，可以直接运行了"

# 下载go.sh并添加权限
if [ ! -e $file_go ];then
    curl https://cdn.jsdelivr.net/gh/KD-happy/KDCheckin@main/other/go.sh -O --progress
    chmod 777 go.sh
    echo -e "go.sh 文件下载完成\n以后就可以通过 ./go.sh 来更新"
fi