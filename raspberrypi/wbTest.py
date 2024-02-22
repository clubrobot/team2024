#import imp
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur


wb = WheeledBase('wheeledbase')

while True:
    wb.goto(40,0)
    print(wb.get_velocities())
