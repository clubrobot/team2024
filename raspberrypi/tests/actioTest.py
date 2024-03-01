#import imp
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur, AX12
import time

actionneur = Actionneur('actionneurs')

#ax1 = AX12(3, actionneur) #Cane



#ax1.turn(-400)

#while True:
    #print(ax1.readTorque())
cane = AX12(1, actionneur)
elevateur = AX12(2, actionneur)
pince_droite = AX12(3, actionneur)
pince_gauche = AX12(4, actionneur)

print(cane.ping())
cane.setEndlessMode(False)
cane.setMaxTorque(1023)
#cane.reset()
### pince gauche 200 ouvert; 230 fermé
### Cane en bas: 50; 0 en haut
cane.move(170)
time.sleep(1)
cane.move(260)
while True:
    print(cane.readPosition())