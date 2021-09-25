from io import StringIO
from KDconfig import getYmlConfig, send
from KDsrc.more import map

all = StringIO()
all.write('今日签到\n')
config = getYmlConfig()

for name, sign in map.items():
    if config.get(name):
        print(f'{sign[0]} 开始签到...')
        sio = sign[1](config.get(name).get('cookies')).SignIn()
        print(sio.getvalue())
        all.write('\n'+sio.getvalue())
    print()
print(all.getvalue())
send('今日签到', all.getvalue())