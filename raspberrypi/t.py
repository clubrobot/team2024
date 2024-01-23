#import imp
from daughter_cards.wheeledbase import WheeledBase, POSITIONCONTROL_LINVELKP_ID
from daughter_cards.actionneur import Actionneur
from common.serialtypes import FLOAT, STRING, INT
from common.serialtalking import GETUUID_OPCODE, SerialTalking
import time


ww = WheeledBase(None, 'COM11')
while 1:
    print(ww.set_velocities(10,0))

	
#LEFTCODEWHEEL_RADIUS_VALUE              = 21.90460280828869
#RIGHTCODEWHEEL_RADIUS_VALUE         = 22.017182927267537
#ODOMETRY_AXLETRACK_VALUE            = 357.5722465739272
# verifier les moteurs sans assver (vrif les sens de marche) open loop velocities
# verifier les codeuses et leur sens
# Faire la metrologie et l'enregistrer
# calibrer l'odométrie (verif la precision)
# calib asservisseement
