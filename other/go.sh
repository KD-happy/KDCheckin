#!/bin/bash
clear
file_name="script"
file_cookie="src/Cookie.yml"
if [ ! -d $file_name ];then
   mkdir $file_name
   echo "创建目录完成"
fi
cd script
git clone https://github.com/KD-happy/KDCheckin.git
echo "Clone完成"
cd ..
if [ ! -f $file_cookie ];then
    \cp script/KDCheckin/Cookie.yml src/
    echo "Cookie.yml 文件复制成功"
fi
\cp -fr script/KDCheckin/KDsrc src/
\cp -f script/KDCheckin/*.py src/KDsrc/
\cp -f script/KDCheckin/QianDao.py src/
echo "复制成功，可以直接运行了"