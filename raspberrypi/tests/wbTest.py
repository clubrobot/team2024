
#import imp
import time
import math
from daughter_cards.wheeledbase import *
from common.serialtalking import BYTE, LONG, FLOAT, INT
from daughter_cards.actionneur import Actionneur
from setups.setup_logger import *
import numpy as np

wheeledbase = WheeledBase()


print(wheeledbase.wheeledbase.getuuid())
    
Y_OFFSET=0
X_OFFSET=2000

wheeledbase.set_position(0,0,0)

wheeledbase.goto(700,0)