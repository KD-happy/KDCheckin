"""
cron: 0 6 * * *
new Env('签到集合')
"""

import traceback
from io import StringIO
from KDconfig import getYmlConfig, send
from KDsrc.more import map

all = StringIO()
all.write('【今日签到】\n')
config = getYmlConfig()

for name, sign in map.items():
    try:
        if config.get(name) != None:
            print(f'{sign[0]} 开始签到...')
            sio = sign[1](config.get(name).get('cookies')).SignIn()
            print(sio.getvalue())
            all.write(sio.getvalue())
    except:
        print(traceback.format_exc())
print(all.getvalue())
send('今日签到', all.getvalue())