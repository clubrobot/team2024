#import imp
from daughter_cards.wheeledbase import WheeledBase, LINVELPID_KP_ID
from common.serialtypes import FLOAT, STRING, INT
from common.serialtalking import GETUUID_OPCODE
import time

wheeeee = WheeledBase(None, 'COM6')
time.sleep(1)
while 1:
    print(wheeeee.get_position())
    time.sleep(1)

	
#LEFTCODEWHEEL_RADIUS_VALUE              = 21.90460280828869
#RIGHTCODEWHEEL_RADIUS_VALUE         = 22.017182927267537
#ODOMETRY_AXLETRACK_VALUE            = 357.5722465739272
# verifier les moteurs sans assver (vrif les sens de marche) open loop velocities
# verifier les codeuses et leur sens
# Faire la metrologie et l'enregistrer
# calibrer l'odométrie (verif la precision)
# calib asservisseement
