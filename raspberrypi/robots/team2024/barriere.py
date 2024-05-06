from daughter_cards.actionneur import Actionneur, AX12
import time

class Barriere:
#droite 80 fermé 170 ouvert
# gauche 105 fermé 20 ouvert
    def __init__(self):
        self.actio = Actionneur()

        self.aileD = AX12(1, self.actio) #pince droite 62 fermé 159 ouvert
        self.aileG = AX12(2, self.actio) #pince gauche 239 fermé 145 ouvert 
    
    def ferme(self):
        self.actio.SetServoAngle(80, 1)
        self.actio.SetServoAngle(105, 2)

    def nicole_oouuuuuvre(self):
        self.actio.SetServoAngle(170, 1)
        self.actio.SetServoAngle(20, 2)

    def aile_d_ouvre(self):
        self.aileD.move_reached(159)

    def aile_d_ferme(self):
        self.aileD.move_reached(62)

    def aile_g_ouvre(self):
        self.aileG.move_reached(145)

    def aile_g_ferme(self):
        self.aileG.move_reached(239)