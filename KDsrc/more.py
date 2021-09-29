"""
多签的配置文件
"""
from KDsrc.AcFun import AcFun
from KDsrc.AZG import AZG
from KDsrc.BLBL import BLBL
from KDsrc.CCAVA import CCAVA
from KDsrc.Cloud import Cloud
from KDsrc.CSDN import CSDN
from KDsrc.Egame import Egame
from KDsrc.EnShan import EnShan

map = {
    "AcFun": ["AcFun", AcFun],
    "AZG": ["爱助攻", AZG],
    "BLBL": ["哔哩哔哩", BLBL],
    "CCAVA": ["CCAVA", CCAVA],
    "Cloud": ["天翼云盘", Cloud],
    "CSDN": ["CSDN", CSDN],
    "Egame": ["企鹅电竞", Egame],
    "EnShan": ["恩山论坛", EnShan],
}