
#import imp
import time
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur
import setups.setup_logger


wb = WheeledBase("COM4")
wb.print_params()
print(wb.wheeledbase.getuuid())
print(wb.wheeledbase.get_logs())