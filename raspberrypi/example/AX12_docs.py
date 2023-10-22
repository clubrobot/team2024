from common.components import Manager
from daughter_cards.actionneur import Actionneur, AX12
from setups.setup_logger import *
import time

manager = Manager("10.0.0.11")#IP du RaspberryPi
manager.connect(7)


actio = Actionneur(manager) #Carte qui gère les AX12
"""
ID sur les AX12:
varie de 0 à 253
l'id 254 donne la commande à tout les ax12 connectés

Les vitesse ont pour valerus min 200 et max 1023
Le couple de 0 à 1023


"""
if False: #documentation
    pince = AX12(1, manager)#Déclarer un AX12 avec comme paramètre l'id et le manager

    pince.ping()#Renvoie vrai si l'AX12 est bien connecté sinon faux
    pince.reset()#Reset l'AX12 en cas de prob

    pince.move(90)#Bouge à une position précise
    pince.moveSpeed(90, 200)#Bouge à une position précise avec vitesse controler

    pince.readPosition()# Renvoie la pos
    pince.readSpeed()# Renvoie la vitesse
    pince.readTorque()# Renvoie le couple

    pince.setAngleLimit(-90, 90)#Met les limites d'angles de l'AX12

    pince.setEndlessMode(True)#met l'AX12 en mode sans fin
    pince.turn(300)#tourne à une vitesse donnée (pour l'autre sens donner une vitesse négative)
    pince.stop_turn(); #ça stop

