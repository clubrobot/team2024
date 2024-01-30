#import imp
from daughter_cards.wheeledbase import WheeledBase, POSITIONCONTROL_LINVELKP_ID
from daughter_cards.actionneur import Actionneur
from common.serialtypes import FLOAT, STRING, INT
from common.serialtalking import GETUUID_OPCODE, SerialTalking
import time
import sys

#Gestion du port série
if 'linux' in sys.platform:
    serial_path = '/dev/ttyUSB0'
else:
    serial_path = 'COM11'
ww = WheeledBase(None, serial_path)

ww.set_position(10,0,0)

#while 1:
    #ww.set_velocities(1,0)
    #print(ww.get_position())

#ww.turnonthespot(180)
#ww.set_velocities(1,0)

	
#LEFTCODEWHEEL_RADIUS_VALUE              = 21.90460280828869
#RIGHTCODEWHEEL_RADIUS_VALUE         = 22.017182927267537
#ODOMETRY_AXLETRACK_VALUE            = 357.5722465739272
# verifier les moteurs sans assver (vrif les sens de marche) open loop velocities
# verifier les codeuses et leur sens
# Faire la metrologie et l'enregistrer
# calibrer l'odométrie (verif la precision)
# calib asservisseement
