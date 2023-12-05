import cv2, glob
import math
import numpy as np
import time
import matplotlib.pyplot as plt

#wheeledbase
#sensors
#jetson


from time import sleep
import glob


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)*231/9

objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane.

cam= cv2.VideoCapture(0)
cam.set(3, 480)
cam.set(4, 480)
cam.set(10, 10)

total=0
print("Debut")
last_capture=time.time()
for i in range(1,50):
    sucessL, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('Frame',gray)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
    
    if(time.time-last_capture>1):
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
        if ret:
            total+=1
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            cv2.drawChessboardCorners(gray, (9,6), corners2, ret)
            last_capture=time.time()
    
    
    

ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(cameraMatrix)
np.save("raspberrypi/tracking/cameraMatrix",cameraMatrix)
print(distCoeffs)
np.save("raspberrypi/tracking/distCoeffs",distCoeffs)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, distCoeffs)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error

print("Mean error: ", mean_error / len(objpoints))

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    print(corner)
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img


for i in range(1,100):
    gray=np.load("res/"+str(i)+".npy")
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
    if ret:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        ret,rvecs, tvecs = cv2.solvePnP(objp, corners2, cameraMatrix, distCoeffs)
        print(tvecs)
        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, cameraMatrix, distCoeffs)
        #img = draw(gray,corners2,imgpts)
        cv2.drawFrameAxes(gray, cameraMatrix, distCoeffs, rvecs, tvecs, 2)
        cv2.imshow('img', gray)
        cv2.waitKey(200)