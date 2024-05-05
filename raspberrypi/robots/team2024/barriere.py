from daughter_cards.actionneur import Actionneur
import time
class Ascenseur:

    def __init__(self):
        self.actio = Actionneur()
        self.actio.SetServoAngle()