import math
import numpy as np

A=np.array([[ 1.00000000e+00,  0.00000000e+00 , 0.00000000e+00 , 0.00000000e+00],
 [ 0.00000000e+00 , 8.45727822e-01 , 5.33614516e-01, 4.10883177e+02],
 [ 0.00000000e+00, 5.33614516e-01 , -8.45727822e-01 ,-6.51210423e+02],
 [ 0.00000000e+00 , 0.00000000e+00 , 0.00000000e+00,  1.00000000e+00]])
pos=np.array([0,0,1220,1])
#[-1.59377493e-01][ 5.09197442e+01][ 1.54207681e+03]
print(np.matmul(A,pos))
#print(np.linalg.inv(A))
print(np.matmul(np.linalg.inv(A),np.array([0,1.51207681e+03,0,1])))
#import cv2, glob
#
#from tracking.libs.positionDetectorMultiple import PositionDetectorMultiple
#print("a")
#cam = cv2.VideoCapture(1)

#if not cam.isOpened():
#    print("Cannot open camera")
#    exit()

#pd=PositionDetectorMultiple()
#pd.KNOW_WIDTH_MARKER=65
#pd.KNOW_WIDTH_MARKER=600
#pd.init([560,1000,880],0,-math.pi/2)
#print("read")
#while True:
#    ret_val, img = cam.read()
#    #print(img.shape)
#    cv2.imshow('my webcam', img)
#    if cv2.waitKey(1) == 27: 
#        break  # esc to quit
#cv2.destroyAllWindows()
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
#print("arrivé",wb.get_position())

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
