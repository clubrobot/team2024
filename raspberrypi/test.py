from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur
#from tracking.libs.positionDetector import PositionDetector
from daughter_cards.sensors import Sensors
import time
from time import sleep
#from tracking.libs.positionDetectorMultiple import *
from robots.team2023.ascenseur import Ascenseur
import math
from robots.team2023.team2023Robot import Bornibus
from robots.team2023.pince import Pince
#from common.gpiodevices import Switch, LightButton, gpio_pins
manager = Manager("10.0.0.2")

manager.connect(7)

from setups.setup_serialtalks import *
actionneur = Actionneur(manager, "actionneurs")
#actionneur.connect()
pince=Pince(actionneur)
print("tourne")
actionneur.SetServoAngle(300)
#asc=Ascenseur(actionneur)
print("a")
#pince.ouvrir()
#asc.bas()
pince.fermer()

#asc.rouler()
#print("bas")
#asc.bas()
wb=WheeledBase(manager)
print()
"""
print(wb.left_codewheel_radius.get())
print(wb.right_wheel_radius.get())
ratio=wb.left_codewheel_radius.get()/wb.right_codewheel_radius.get()
radius=wb.right_codewheel_radius.get()
c=0.98
radius=23*c
ratio=1.0
print(wb.codewheels_axletrack.get())
wb.codewheels_axletrack.set(212.4*c)#212.4 23 1.0
print(wb.codewheels_axletrack.get())
wb.right_codewheel_radius.set(radius)
wb.left_codewheel_radius.set(ratio*radius)
print(ratio)

wb.set_position(0,1000,0)
#wb.goto_stop(1200,1000,None,theta=0)
#wb.set_openloop_velocities(500,0)
#for i in range(3*2+1):
    #print(i)
    #wb.goto_stop(1000,1000,None,theta=-i*math.pi)
"""
#wb.turnonthespot(math.pi)
#wb.save_parameters()
#while True:
#    True
    #print(wb.get_position())
print("arrivé",wb.get_position())

#from managers.buttons_manager import ButtonsManager
#ButtonsManager(None).begin()

#LEFTCODEWHEEL_RADIUS_VALUE              = 21.90460280828869
#RIGHTCODEWHEEL_RADIUS_VALUE         = 22.017182927267537
#ODOMETRY_AXLETRACK_VALUE            = 357.5722465739272
# verifier les moteurs sans assver (vrif les sens de marche) open loop velocities
# verifier les codeuses et leur sens
# Faire la metrologie et l'enregistrer
# calibrer l'odométrie (verif la precision)
# calib asservisseement
