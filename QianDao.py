"""
cron: 0 6 * * *
new Env('签到集合')
"""

import traceback, argparse
from io import StringIO
from KDconfig import getYmlConfig, send
from KDsrc.more import map

all = StringIO()
all.write('===== 每日签到 =====\n')
config = getYmlConfig()
signList = config.get('signList', '')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--include", nargs="+", help="任务执行包含的任务列表")
    parser.add_argument("-e", "--exclude", nargs="+", help="任务执行排除的任务列表")
    return parser.parse_args()

if signList == '':
    args = parse_arguments()
    print(args)
    include = args.include
    exclude = args.exclude
    if not include:
        include = list(map.keys())
    else:
        include = [one for one in include if one in map.keys()]
    if not exclude:
        exclude = []
    else:
        exclude = [one for one in exclude if one in map.keys()]
    task_list = list(set(include) - set(exclude))
    task_list.sort(key=include.index) # 通过此方法来实现 输入顺序是主顺序
else:
    task_list = [one for one in signList.replace(' ', '').split(',') if one in map.keys()]

for name in task_list:
    try:
        sign = map.get(name, [])
        if config.get(name) != None and len(sign) == 2:
            print(f'{sign[0]} 开始签到...')
            if config.get(name, {}).get('cookies') != None:
                sio = sign[1](config.get(name).get('cookies', {})).SignIn()
                print(sio.getvalue())
                all.write(sio.getvalue() + '\n')
            else:
                print(f'{sign[0]} 没有配置文件\n')
                all.write(f'{sign[0]} 没有配置文件\n\n')
        else:
            all.write(f'没有 {name} 相关签到\n\n')
    except:
        print(traceback.format_exc())
else:
    if len(task_list) == 0:
        all.write('无签到')
print(all.getvalue())
send('每日签到', all.getvalue())


# for name, sign in map.items():
# for name in signList.split(', '):
#     try:
#         sign = map.get(name, [])
#         if config.get(name) != None and len(sign) == 2:
#             print(f'{sign[0]} 开始签到...')
#             if config.get(name).get('cookies') != None:
#                 sio = sign[1](config.get(name).get('cookies', {})).SignIn()
#                 print(sio.getvalue())
#                 all.write(sio.getvalue() + '\n')
#             else:
#                 print(f'{sign[0]} 没有配置文件')
#                 all.write(f'{sign[0]} 没有配置文件\n')
#         else:
#             all.write(f'没有 {name} 相关签到\n\n')
#     except:
#         print(traceback.format_exc())
# else:
#     all.write('\n')
# print(all.getvalue().replace('\n\n\n', ''))
# send('每日签到', all.getvalue().replace('\n\n\n', ''))