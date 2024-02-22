#import imp
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur, AX12


actionneur = Actionneur('COM7')

ax1 = AX12(3, actionneur) #Cane



ax1.turn(-400)

while True:
    print(ax1.readTorque())


""" for i in range(0,254):
    ax = AX12(i, actionneur)
    print(i)
    print(ax.ping()) """
