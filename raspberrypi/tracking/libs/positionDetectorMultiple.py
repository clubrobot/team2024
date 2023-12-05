import cv2
import transformations as ts
from cv2 import aruco
import numpy as np
import math
import time



def getPosition(origin, dir, length):
    return origin + np.multiply(dir, length)


class PositionDetectorMultiple:

    #initialize all the values with defaults values
    def __init__(self):
        self.invViewMatrix = np.identity(4)
        self.invProjectionMatrix= np.identity(4)
        self.cameraPos = []
        self.cameraLeft = None
        self.cameraRight = None
        self.WIDTH = 480
        self.HEIGTH = 480
        self.CENTER_MARKER_ID=17
        self.KNOW_DISTANCE_TO_MARKER = 300
        self.KNOW_WIDTH_MARKER = 0.06
        self.DELTA_TIME_SPEED=100
        self.L=200

        self.markerIds=[]
        self.markerPositions={}
        self.dictionary = cv2.aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        self.parameters = aruco.DetectorParameters()
        self.detector=aruco.ArucoDetector(self.dictionary,self.parameters)

    #find the marker length on the screen
    def find_marker_length(self,img,idMarker):
        imgTree = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        markerCorners, markerids, rejectedCandidates = self.detector.detectMarkers(imgTree)
        if markerids is not None:
            for i in range(0, len(markerids)):
                if markerids[i][0] == idMarker:
                    p0 = markerCorners[0][0][0]
                    p1 = markerCorners[0][0][1]
                    p01 = p0 - p1
                    l = p01[0] * p01[0] + p01[1] * p01[1]
                    return math.sqrt(l)
        return -1

    #create rotation matrix with the position vector p of the camera multiply by -1 and 3 by 3 rotation matrix r
    #|r00 r01 r11 px|
    #|r10 r11 r12 py|
    #|r20 r21 r22 pz|
    #| 0   0   0  1 |
    def createViewMatrix(self,pitch, yaw, negativepos):
        E = ts.euler_matrix(pitch, yaw, 0, 'rxyz')
        T = ts.translation_matrix(negativepos)
        return ts.concatenate_matrices(E, T)

    #init the camera need the camera position and its orientation
    def init(self,camPos, pitchCam, yawCam):
        self.cameraLeft = cv2.VideoCapture(0)
        self.cameraLeft.set(3, self.WIDTH)
        self.cameraLeft.set(4, self.HEIGTH)
        self.cameraLeft.set(10, 10)

        self.cameraPos = camPos


        #compute view matrix
        viewMatrix=self.createViewMatrix(pitchCam, yawCam, [-camPos[0],-camPos[1],-camPos[2]])
        self.invViewMatrix = np.linalg.inv(viewMatrix)
        self.cameraMatrix=np.load("res/cameraMatrix.npy")
        self.distCoeffs=np.load("res/distCoeffs.npy")
        marker_size=66
        self.obj_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)


    #compute marker positions, velocities, and orientation
    def update(self):
        #capture an image
        sucessL, imgL = self.cameraLeft.read()
        self.markerPositions={}

        imgTreeL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)

        #On suppose que les dex camera detexte bien les tout les mêmes tags hein sinon on pleure
        markerCornersL, markeridsL, rejectedCandidates = self.detector.detectMarkers(imgTreeL)
       
        if markeridsL is not None:
            for i in range(0, len(markeridsL)):
                print( markeridsL[i][0],self.markerIds)
                if markeridsL[i][0] in self.markerIds:
                    #à tester
                    success, vector_rotation, vector_translation = cv2.solvePnP(self.obj_points , markerCornersL[i], self.cameraMatrix, self.distCoeffs, False,cv2.SOLVEPNP_IPPE_SQUARE)
                    pos=np.matmul(self.invViewMatrix,np.array([vector_translation[0],vector_translation[1],vector_translation[2],1]))
                    print(pos)
                    if not (markeridsL[i][0] in self.markerPositions.keys()):
                        self.markerPositions[markeridsL[i][0]]=[]
                    self.markerPositions[markeridsL[i][0]].append(pos)
                    cv2.drawFrameAxes(imgL, self.cameraMatrix, self.distCoeffs, vector_rotation, vector_translation, 33)
        # Press Q on keyboard to  exit
        cv2.imshow('Frame', imgL)
        time.sleep(0.2)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            print("a")
    #add a new maker to follow
    def addMarker(self,idMarker):
        self.markerIds.append(idMarker)
        

    #try to remove a marker from the marker's list return true if it works
    def removeMarker(self,idMarker):
        if idMarker not in self.markerIds:
            return False
        self.markerIds.remove(idMarker)

    #GETTERS AND SETTERS
    def setWIDTH(self, value):
        self.WIDTH = value

    def getWIDTH(self):
        return self.WIDTH

    def setHEIGHT(self, value):
        self.HEIGHT = value

    def getHEIGHT(self):
        return self.HEIGHT

    def setCENTER_MARKER(self, id,distanceToCamera,width):
        self.CENTER_MARKER_ID = id
        self.KNOW_DISTANCE_TO_MARKER=distanceToCamera
        self.KNOW_WIDTH_MARKER=width

    def getCENTER_MARKER_ID(self):
        return self.CENTER_MARKER_ID

    def setDictionary(self, value):
        self.dictionary = value

    def getDictionary(self):
        return self.dictionary

    def setDeltaTimeSpeed(self, value):
        self.DELTA_TIME_SPEED = value

    def getDeltaTimeSpeed(self):
        return self.DELTA_TIME_SPEED

    def getMarkerIds(self):
        return self.markerIds

    def getMarkerPosition(self):
        return self.markerPositions

    def getMarkerPosition(self, idMarker):
        if idMarker not in self.markerIds:
            return -999999
        return self.markerPositions[idMarker]