#import imp
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur, AX12
import time

actionneur = Actionneur()

actionneur.SetServoAngle(80, 1)#droite 80 fermé 170 ouvert
actionneur.SetServoAngle(10, 2)# gauche 105 fermé 20 ouvert

while 1:
    actionneur.SetServoAngle(80, 1)
    actionneur.SetServoAngle(105, 2)
    time.sleep(1)
    actionneur.SetServoAngle(170, 1)
    actionneur.SetServoAngle(20, 2)
    time.sleep(1)
    
exit()
ax1 = AX12(1, actionneur) #pince droite 62 fermé 159 ouvert
ax2 = AX12(2, actionneur) #pince gauche 239 fermé 145 ouvert 
while 1:
    ax1.move(62)
    ax2.move_reached(239)
    time.sleep(0.5)
    ax1.move(159)
    ax2.move_reached(145)
    time.sleep(0.5)
while 0:
    print(str(ax1.readPosition()) + " | " +str(ax2.readPosition()))



for i in range(0,254):
    ax1 = AX12(i, actionneur) #Cane
    print(str(i) + " " +str(ax1.ping()))

#while True:
    #print(ax1.readTorque())
""" cane = AX12(1, actionneur)
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
    print(cane.readPosition()) """