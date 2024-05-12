import time
from common.serialtalking import BYTE, LONG, FLOAT, INT, UINT
from common.serialtalking import SerialTalking
from daughter_cards.wheeledbase import WheeledBase
import setups.setup_logger
import numpy as np
talking = WheeledBase("COM11")
talking.set_position(0,0,np.pi)
time.sleep(90)
while 1:
    talking.wheeledbase.getuuid()
    print(talking.get_position())
    
    print(talking.wheeledbase.request(0x25, UINT)[0]) 