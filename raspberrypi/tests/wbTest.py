
#import imp
import time
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur
from setups.setup_logger import *


wb = WheeledBase()


print(wb.wheeledbase.getuuid())
while True:
    print(wb.set_velocities(100,0))