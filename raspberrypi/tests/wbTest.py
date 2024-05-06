
#import imp
import time
import math
from daughter_cards.wheeledbase import *
from common.serialtalking import BYTE, LONG, FLOAT, INT
from daughter_cards.actionneur import Actionneur
from setups.setup_logger import *


wheeledbase = WheeledBase()


print(wheeledbase.wheeledbase.getuuid())

wheeledbase.goto(500,500)