from daughter_cards.actionneur import Actionneur
import time
class Pince:

    def __init__(self,manager):
        self.pince = manager.AX12(1, manager)
        self.pince.setEndlessMode(False)
        self.pince.setAngleLimit(0,1023)
        self.pince.setMaxTorque(1023)
        

        

    def fermer(self):
        end=300
        deb=time.time()
        self.pince.move(end)
        print(self.pince.readPosition())
        while((abs(self.pince.readPosition()-end)>5 or self.pince.readSpeed()>0) and time.time()-deb<3):
            continue
    def ouvrir(self):
         end=0
         deb=time.time()
         self.pince.move(end)
         self.pince.readPosition()
         while((abs(self.pince.readPosition()-end)>5 or self.pince.readSpeed()>0) and time.time()-deb<3):
            continue
         
    def semi_ouvrir(self):
         end=150
         deb=time.time()
         self.pince.move(end)
         self.pince.readPosition()
         while((abs(self.pince.readPosition()-end)>5 or self.pince.readSpeed()>0) and time.time()-deb<3):
            continue

    def isFerme(self):
        return "TODO"
