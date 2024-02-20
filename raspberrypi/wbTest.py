#import imp
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur


wb = WheeledBase(None, 'COM3')

while(True):
    print(wb.get_position())
	
