
#import imp
import time
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase, POSITIONCONTROL_LINPOSTHRESHOLD_ID
from common.serialtalking import BYTE, LONG, FLOAT, INT
from daughter_cards.actionneur import Actionneur
from setups.setup_logger import *


wb = WheeledBase("COM7")


print(wb.wheeledbase.getuuid())
wb.set_position(0,0,0)
wb.goto(100,100,0)
wb.goto(100,0,0)
wb.goto(0,100,0)
wb.goto(0,0,0)

