#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
#from daughter_cards.sensors import Sensors
import cv2, glob
import math
import numpy as np
from tracking.libs.positionDetectorMultiple import PositionDetectorMultiple
from daughter_cards.wheeledbase import WheeledBase

print("b")
posDetect =PositionDetectorMultiple()
posCam=[0,0,770]
posDetect.addMarker(0)
print(posDetect.markerIds)
posDetect.init(posCam,math.radians(90-32.25),0)#bien itnit avec 90-angle jsp pk

print("boucle")
datas=[]
while(True):
    t=time.time()
    sucess, img = posDetect.cameraLeft.read()
    
    posDetect.update()
    print(1/(time.time()-t))
    #time.sleep(0.2)
#[[ 1.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]
# [ 0.00000000e+00  8.45727822e-01  5.33614516e-01 -4.10883177e+02]
# [ 0.00000000e+00 -5.33614516e-01  8.45727822e-01 -6.51210423e+02]
# [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  1.00000000e+00]

