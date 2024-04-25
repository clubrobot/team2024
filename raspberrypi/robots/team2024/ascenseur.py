from daughter_cards.actionneur import Actionneur
import time
class Ascenseur:

    def __init__(self,manager):
        self.asc = manager.AX12(3, manager)
        self.asc.setEndlessMode(True)
        self.asc.setMaxTorque(1023)
        self.v_bas=100
        self.pos=0
        self.oldPos=-9999
        #self.bas()

    """def update(self):
        newPos=self.asc.readPosition()
        if(abs(newPos-self.oldPos)>50 and (self.pos<15 or self.pos>185)):
            if(newPos>self.oldPos):
                self.pos-=self.oldPos+(360-newPos)
            else:
                self.pos+=newPos+(360-self.oldPos)
            self.oldPos=newPos
        elif(abs(newPos-self.oldPos)<50):
            self.pos+=(newPos-self.oldPos)
            self.oldPos=newPos"""
    def rouler(self):
        """obj=400
        self.asc.setAngleLimit(0,0)
        self.oldPos=self.asc.readPosition()
        print(self.oldPos)
        self.asc.turn(500)
        print("passe")
        while(self.pos<obj-5):
            self.update()
            print(self.pos,self.oldPos)"""

        end=1000
        self.asc.move(end)
        deb=time.time()
        self.asc.readPosition()
        while((abs(self.asc.readPosition()-end)>5 )and time.time()-deb<3):
            
            #print(abs(self.asc.readPosition()-end),self.asc.readSpeed())
            continue

#300 haut de la pince bas du magasin
    def bas(self):
        end=0
        #self.asc.setAngleLimit(0,1023)
        self.asc.move(0)
        deb=time.time()
        self.asc.readPosition()
        self.pos=0
        while((abs(self.asc.readPosition()-end)>5 or self.asc.readSpeed()>0)and time.time()-deb<3):
  
            
            #print(self.asc.readPosition(),self.asc.readTorque())
            continue
        print("fin")
            
        #self.asc.move(-500)