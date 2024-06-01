
#import imp
import time
import math
from daughter_cards.wheeledbase import *
from common.serialtalking import BYTE, LONG, FLOAT, INT
from daughter_cards.actionneur import Actionneur
from daughter_cards.sensors import Sensors
from setups.setup_logger import *
import numpy as np
from logs.logger import Logger

wheeledbase = WheeledBase()
sensors = Sensors()

wheeledbase.start_match()
wheeledbase.set_position(0,0, np.pi)
wheeledbase.goto_stop(10,0,np.pi)
time.sleep(90)
wheeledbase.set_position(10,0, np.pi)
wheeledbase.start_match()
wheeledbase.goto_stop(500,0, sensors, np.pi)
while 1:
    print(wheeledbase.get_position())
