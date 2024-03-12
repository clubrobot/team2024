
#import imp
import time
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur
import setups.setup_logger


wb = WheeledBase("COM3")



print(wb.wheeledbase.getuuid())

wb