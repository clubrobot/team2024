import math
import numpy as np
from daughter_cards.wheeledbase import *;

wb = WheeledBase()

print(wb.wheeledbase.getuuid())

while True:
    pos = wb.get_position()
    sen = np.array([True,True,True,True,True,True,True,True])
    if(pos[0]<300):
        if(wb.theta < 0 and wb.theta > -math.pi/2):
            # stop 0
            sen[0] = False
        elif(wb.theta < -math.pi/6 and wb.theta > -2*math.pi/3):
            # stop 1
            sen[1] = False
        elif(wb.theta < -math.pi/3 and wb.theta > -5*math.pi/6):
            # stop 2
            sen[2] = False
        elif(wb.theta < -math.pi/2 and wb.theta > -math.pi):
            # stop 3
            sen[3] = False
        elif(wb.theta > 0 and wb.theta < math.pi/2):
            # stop 7
            sen[7] = False
        elif(wb.theta > 2*math.pi/3 and wb.theta < 7*math.pi/6):
            # stop 6
            sen[6] = False
        elif(wb.theta > 5*math.pi/6 and wb.theta < 4*math.pi/3):
            # stop 5
            sen[5] = False
        elif(wb.theta > math.pi and wb.theta < 3*math.pi/2):
            # stop 4
            sen[4] = False

    elif(pos[0]>1700):
        if(wb.theta > 0 and wb.theta < math.pi/2):
            # stop 3
            sen[3] = False
        elif(wb.theta > math.pi/6 and wb.theta < 2*math.pi/3):
            # stop 2
            sen[2] = False
        elif(wb.theta > math.pi/3 and wb.theta < 5*math.pi/6):
            # stop 1
            sen[1] = False
        elif(wb.theta > math.pi/2 and wb.theta < math.pi):
            # stop 0
            sen[0] = False
        elif(wb.theta < 0 and wb.theta > -math.pi/2):
            # stop 4
            sen[4] = False
        elif(wb.theta < -math.pi/6 and wb.theta > -2*math.pi/3):
            # stop 5
            sen[5] = False
        elif(wb.theta < -math.pi/3 and wb.theta > -5*math.pi/6):
            # stop 6
            sen[6] = False
        elif(wb.theta < -math.pi/2 and wb.theta > -math.pi):
            # stop 7
            sen[7] = False
    if(pos[1]<300):
        if(wb.theta < -math.pi/2 and wb.theta > -math.pi):
            # stop 4
            sen[4] = False
        elif(wb.theta < -2*math.pi/3 and wb.theta > -7*math.pi/6):
            # stop 5
            sen[5] = False
        elif(wb.theta < -5*math.pi/6 and wb.theta > -4*math.pi/3):
            # stop 6
            sen[6] = False
        elif(wb.theta < -math.pi and wb.theta > -3*math.pi/2):
            # stop 7
            sen[7] = False
        elif(wb.theta > -math.pi/2 and wb.theta < 0):
            # stop 3
            sen[3] = False
        elif(wb.theta > -math.pi/3 and wb.theta < math.pi/6):
            # stop 2
            sen[2] = False
        elif(wb.theta > -math.pi/6 and wb.theta < math.pi/3):
            # stop 1
            sen[1] = False
        elif(wb.theta > 0 and wb.theta < math.pi/2):
            # stop 0
            sen[0] = False
    elif(pos[1]>2700):
        if(wb.theta > -math.pi/2 and wb.theta < 0):
            # stop 7
            sen[7] = False
        elif(wb.theta > -math.pi/3 and wb.theta < math.pi/6):
            # stop 6
            sen[6] = False
        elif(wb.theta > -math.pi/6 and wb.theta < math.pi/3):
            # stop 5
            sen[5] = False
        elif(wb.theta > 0 and wb.theta < math.pi/2):
            # stop 4
            sen[4] = False
        elif(wb.theta < -math.pi/2 and wb.theta > -math.pi):
            # stop 0
            sen[0] = False
        elif(wb.theta < -2*math.pi/3 and wb.theta > -7*math.pi/6):
            # stop 1
            sen[1] = False
        elif(wb.theta < -5*math.pi/6 and wb.theta > -4*math.pi/3):
            # stop 2
            sen[2] = False
        elif(wb.theta < -math.pi and wb.theta > -3*math.pi/2):
            # stop 3
            sen[3] = False

    # print the sensors with False value
    for i in range(8):
        if not sen[i]:
            print("Sensor " + str(i) + " is blocked")