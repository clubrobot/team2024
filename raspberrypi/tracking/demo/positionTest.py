import time
#from daughter_cards.sensors import Sensors
import cv2, glob
import math
import numpy as np
from tracking.libs.positionDetectorMultiple import PositionDetectorMultiple
from daughter_cards.wheeledbase import WheeledBase





print("b")
posDetect =PositionDetectorMultiple()
posCam=[0,0,0]
posDetect.addMarker(17)
print(posDetect.markerIds)
posDetect.init(posCam,0,0)

print("boucle")
datas=[]
while(True):
    t=time.time()
    sucess, img = posDetect.cameraLeft.read()
    
    posDetect.update()


        
                    
    

