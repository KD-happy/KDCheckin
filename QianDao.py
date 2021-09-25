from io import StringIO
from KDconfig import getYmlConfig
from KDsrc.more import map

config = getYmlConfig()

for name, sign in map.items():
    if config.get(name):
        print(f'{sign[0]} 开始签到...\n')
        dio, sio = sign[1](config.get(name)).SignIn()
        print(sio.getvalue())
    print()