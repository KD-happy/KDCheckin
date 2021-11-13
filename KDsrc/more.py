"""
多签的配置文件
"""
from KDsrc.AcFun import AcFun
from KDsrc.AiHao import AiHao
from KDsrc.AZG import AZG
from KDsrc.BDTieBa import BDTieBa
from KDsrc.BLBL import BLBL
from KDsrc.CCAVA import CCAVA
from KDsrc.Cloud import Cloud
from KDsrc.CSDN import CSDN
from KDsrc.Du163 import Du163
from KDsrc.DuoKan import DuoKan
from KDsrc.Egame import Egame
from KDsrc.EnShan import EnShan
from KDsrc.Heytap import Heytap
from KDsrc.HeytapSleep import HeytapSleep
from KDsrc.HLX import HLX
from KDsrc.IQIYI import IQIYI
from KDsrc.Lenovo import Lenovo
from KDsrc.LenovoLTB import LenovoLTB
from KDsrc.Music163 import Music163
from KDsrc.NoteYouDao import NoteYouDao
from KDsrc.PTA import PTA
from KDsrc.SMZDM import SMZDM
from KDsrc.ToolLu import ToolLu
from KDsrc.VQQ import VQQ
from KDsrc.W2PJ import W2PJ
from KDsrc.Weather import Weather
from KDsrc.WPS import WPS
from KDsrc.XMYD import XMYD

map = {
    "AcFun": ["AcFun", AcFun],
    "AiHao": ["爱好论坛", AiHao],
    "AZG": ["爱助攻", AZG],
    "BDTieBa": ["百度贴吧", BDTieBa],
    "BLBL": ["哔哩哔哩", BLBL],
    "CCAVA": ["CCAVA", CCAVA],
    "Cloud": ["天翼云盘", Cloud],
    "CSDN": ["CSDN", CSDN],
    "Du163": ["网易读书", Du163],
    "DuoKan": ["多看阅读", DuoKan],
    "Egame": ["企鹅电竞", Egame],
    "EnShan": ["恩山论坛", EnShan],
    "Heytap": ["欢太商城", Heytap],
    "HeytapSleep": ["欢太早睡打卡", HeytapSleep],
    "HLX": ["葫芦侠", HLX],
    "IQIYI": ["爱奇艺", IQIYI],
    "Lenovo": ["联想商城", Lenovo],
    "LenovoLTB": ["乐同步", LenovoLTB],
    "Music163": ["网易云音乐", Music163],
    "NoteYouDao": ["有道云笔记", NoteYouDao],
    "PTA": ["PTA", PTA],
    "SMZDM": ["什么值得买", SMZDM],
    "ToolLu": ["Tool工具", ToolLu],
    "VQQ": ["腾讯视频", VQQ],
    "W2PJ": ["吾爱破解", W2PJ],
    "Weather": ["天气预报", Weather],
    "WPS": ["WPS签到", WPS],
    "XMYD": ["小米运动", XMYD]
}

# 欢太任务列表
act_task = [
    {
        "act_name": "赚积分",
        "aid": 1418,
        "if_task": True,  # 是否有任务
        "referer": "https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html?us=gerenzhongxin&um=hudongleyuan&uc=yingjifen",
        "if_draw": True,  # 是否有抽奖活动，已修复抽奖，如不需要抽奖请自行修改为False
        "extra_draw_cookie": 'app_innerutm={"uc":"yingjifen","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
        # 抽奖必要的额外cookie信息，请勿随意修改，否则可能导致不中奖
        "lid": 1307,  # 抽奖参数
        "draw_times": 3,  # 控制抽奖次数3
        "end_time": "2033-8-18 23:59:59",  # 长期任务
        "text": "每次扣取0积分，任务获取次数",
    },
    {
        "act_name": "realme积分大乱斗-8月",
        "aid": 1582,
        "if_task": True,
        "referer": "https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html",
        "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
        "extra_draw_cookie": 'app_innerutm={"uc":"renwuzhongxin","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
        "lid": 1466,
        "draw_times": 3,
        "end_time": "2022-8-31 23:59:59",
        "text": "每次扣取5积分，测试仍然可以中奖",
    },
    {
        "act_name": "realme积分大乱斗-9月",
        "aid": 1582,
        "if_task": True,
        "referer": "https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html?&us=realmenewshouye&um=yaofen&ut=right&uc=realmedaluandou",
        "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
        "extra_draw_cookie": 'app_innerutm={"uc":"renwuzhongxin","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};',
        "lid": 1554,  # 抽奖接口与8月不一样，测试可以独立抽奖
        "draw_times": 3,
        "end_time": "2022-8-31 23:59:59",
        "text": "每次扣取5积分",
    },
    {
        "act_name": "realme积分大乱斗-9月(2)",
        "aid": 1598,
        "if_task": True,
        "referer": "https://hd.oppo.com/act/m/2021/huantaishangchengjif/index.html?&us=realmeshouye&um=icon&ut=3&uc=realmejifendaluandou",
        "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
        "extra_draw_cookie": 'app_innerutm={"uc":"realmejifendaluandou","um":"icon","ut":"3","us":"realmeshouye"};',
        "lid": 1535,
        "draw_times": 3,
        "end_time": "2022-8-31 23:59:59",
        "text": "每次扣取10积分",
    },
    {
        "act_name": "天天积分翻倍",
        "aid": 675,
        "if_task": False,  # 该活动没有任务
        "referer": "https://hd.oppo.com/act/m/2019/jifenfanbei/index.html?us=qiandao&um=task",
        "if_draw": True,  # 已修复抽奖，如不需要抽奖请自行修改为False
        "extra_draw_cookie": 'app_innerutm={"uc":"direct","um":"zuoshangjiao","ut":"direct","us":"shouye"};',
        "lid": 1289,
        "draw_times": 1,
        "end_time": "2033-8-18 23:59:59",
        "text": "每次扣取10积分",
    },
    {
        "act_name": "双十一活动",
        "aid": 1768,
        "if_task": True,
        "referer": "https://hd.oppo.com/act/m/2021/choumiandan/index.html?us=shouye&um=youshangjiao&uc=2021oppowin",
        "if_draw": False,  # 已修复抽奖，如不需要抽奖请自行修改为False
        "extra_draw_cookie": 'app_innerutm={"uc":"direct","um":"direct","ut":"direct","us":"direct"};',
        "lid": 1586,
        "draw_times": 1,
        "end_time": "2021-11-13 23:59:59",
        "text": "每次扣取5积分",
    }
]