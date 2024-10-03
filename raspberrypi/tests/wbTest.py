
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

#wheeledbase.start_match()
#wheeledbase.set_position(0,0, np.pi)
#wheeledbase.goto_stop(10,0,np.pi)
#time.sleep(90)

for i in range(1):
    sen=sensors.get_all_sensors()
    detect=np.sum(np.array(sen)<5)>5

    print(i,sensors.get_all_sensors(),detect)
    if(detect):
        print("RESET------------------------------------------")
        sensors = Sensors()
    time.sleep(1)

print("BONNE ANN2e")
print("Sensors:",sensors)

wheeledbase.start_match()
wheeledbase.set_position(1000,1000,0)
wheeledbase.goto_stop(1000,1000, sensors,theta=-math.pi/2)

time.sleep(1)

#wheeledbase.goto_stop(1000,1000, sensors,theta=0)
#while 1:
#    print(wheeledbase.get_position(),sensors.get_all_sensors())
