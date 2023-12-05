import cv2, glob
import math
import numpy as np
import time
from time import sleep
import glob
"""
Script de calibration: prends des images d'un échiquier et calcule deux matrices de calibration
Bien mettre la même resolution à la caméra pour la calibration et pour l'utilisation
Il faut prendre des images avec un échiquier de taille n_carreau_longeur par n_carreau_largeur carreaux.
Les images doivent être le plus varie possible il faut en prendre avec des:
- rotations sur les 3 axes 
- pas que dans le centre de la caméra (bien insister sur les bords et les coins)
- à differente distance de la caméra
"""
#9 et 6 si l'échiquier fait bien 9 carreaux par 6 carreaux
n_carreau_longeur=9
n_carreau_largeur=6
taille_carreau_mm=231/9#taille d'un carreau en mm

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((n_carreau_largeur*n_carreau_longeur, 3), np.float32)
objp[:, :2] = np.mgrid[0:n_carreau_longeur, 0:n_carreau_largeur].T.reshape(-1, 2)*taille_carreau_mm
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane.

cam= cv2.VideoCapture(0)#mettre 1 ou 2 ... si la camera qui est detectée n'est pas celle que l'on souhaite calibrer
cam.set(3, 480)#résolution de la camera
cam.set(4, 480)#résolution de la camera
cam.set(10, 10)

total=0
print("Debut")
last_capture=time.time()
#boucle et et prends en photo l'échiquier toute les 1 secondes.
for i in range(1,50):
    sucessL, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('Frame',gray)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
    
    if(time.time-last_capture>1):
        #detecte l'echiquier
        ret, corners = cv2.findChessboardCorners(gray, (n_carreau_longeur, n_carreau_largeur), None)
        if ret:
            total+=1
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            last_capture=time.time()
    
    
#calcule et sauvegarde le résultat de la calibration
ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(cameraMatrix)
np.save("raspberrypi/tracking/cameraMatrix",cameraMatrix)
print(distCoeffs)
np.save("raspberrypi/tracking/distCoeffs",distCoeffs)

#calcule un indicateur de la qualité de la calibration 
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, distCoeffs)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error

print("Mean error: ", mean_error / len(objpoints))