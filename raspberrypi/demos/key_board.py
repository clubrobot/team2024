import getch
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur, AX12
wb = WheeledBase('wheeledbase')
actionneur = Actionneur()

cane = AX12(1, actionneur)
elevateur = AX12(2, actionneur)
pince_droite = AX12(3, actionneur)
pince_gauche = AX12(4, actionneur)

pince_gauche.setEndlessMode(False)
pince_gauche.setMaxTorque(1023)

while True:
    key = getch.getch()
     
    if(ord(key)==65):
        wb.set_openloop_velocities(300,-300)
    elif(ord(key)==66):
        wb.set_openloop_velocities(-300,300)
    elif(ord(key)==67):
        wb.set_openloop_velocities(300,300)
    elif(ord(key)==68):
        wb.set_openloop_velocities(-300,-300)
    elif(key=='s'):
        wb.set_openloop_velocities(0,0)

    if(key=='0'):
        pince_gauche.move(200)
    elif(key=='1'):
        pince_gauche.move(230)



    ### pince gauche 200 ouvert; 230 fermé
    

    if key == 'x':
        break
