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
        self.FOV = 70
        self.camera = None
        self.WIDTH = 480
        self.HEIGTH = 480
        self.CENTER_MARKER_ID=17
        self.KNOW_DISTANCE_TO_MARKER = 300
        self.KNOW_WIDTH_MARKER = 0.06
        self.DELTA_TIME_SPEED=100

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

    def distance_to_camera(self,knowWidth, focalLength, perWidth):
        return (knowWidth * focalLength) / perWidth

    #create rotation matrix with the position vector p of the camera multiply by -1 and 3 by 3 rotation matrix r
    #|r00 r01 r11 px|
    #|r10 r11 r12 py|
    #|r20 r21 r22 pz|
    #| 0   0   0  1 |
    def createViewMatrix(self,pitch, yaw, negativepos):
        E = ts.euler_matrix(pitch, yaw, 0, 'rxyz')
        T = ts.translation_matrix(negativepos)
        return ts.concatenate_matrices(E, T)

    #compute projection matrix a is screen height divide by width t is tan(FOV/2)
    # l is the frustum length equals to far plane minus near plane f=is far plane n is near plane
    #|1/(t*a) 0     0      0    |
    #|  0    1/t    0      0    |
    #|  0    0  -(f+n)/l -2fn/l |
    #|  0    0     -1      0    |
    def createProjectionMatrix(self,fov, aspect, near, far):
        M = np.identity(4)
        M[3, 3] = 0
        M[1, 1] = 1 / math.tan(fov / 2)
        M[0, 0] = 1 / math.tan(fov / 2) / aspect
        M[2, 2] = -((far + near)) / (far - near)
        M[2, 3] = -1
        M[3, 2] = -((far * near * 2)) / (far - near)
        return M

    #compute the ray the pixel pos
    def getRay(self,screenPos):
        screenPos[0] = screenPos[0] / self.WIDTH * 2 - 1
        screenPos[1] = screenPos[1] / self.HEIGTH* 2 - 1
        clipCoord = [screenPos[0], screenPos[1], -1, 1]
        eyeCoord = np.matmul(self.invProjectionMatrix, clipCoord)

        eyeCoord[2] = -1
        eyeCoord[3] = 0

        rayWorld = np.matmul(self.invViewMatrix, eyeCoord)
        length = rayWorld[0] * rayWorld[0] + rayWorld[1] * rayWorld[1] + rayWorld[2] * rayWorld[2]
        length = math.sqrt(length)
        return [rayWorld[0] / length, rayWorld[1] / length, rayWorld[2] / length]

    #init the camera need the camera position and its orientation
    def init(self,camPos, pitchCam, yawCam):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, self.WIDTH)
        self.camera.set(4, self.HEIGTH)
        self.camera.set(10, 10)

        self.cameraPos = camPos

        #compute view matrix
        viewMatrix=self.createViewMatrix(pitchCam, yawCam, [-camPos[0],-camPos[1],-camPos[2]])
        self.invViewMatrix = np.linalg.inv(viewMatrix)
        # compute projection matrix with the camera fov the images aspect ratio and random far and near value.
        self.invProjectionMatrix = np.linalg.inv(self.createProjectionMatrix(self.FOV, float(self.WIDTH) / self.HEIGTH, 1000, 0.1))

        #calibrate camera look for the center marker and when he see it calculate the camera focalLength
        d = -1
        while d < 0:
            sucess, img = self.camera.read()
            d = self.find_marker_length(img,self.CENTER_MARKER_ID)
        self.focalLength = (d * self.KNOW_DISTANCE_TO_MARKER) / self.KNOW_WIDTH_MARKER
        print(self.focalLength)

    #compute marker positions, velocities, and orientation
    def update(self):
        sucess, img = self.camera.read()

        self.markerPositions={}

        imgTree = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        markerCorners, markerids, rejectedCandidates = self.detector.detectMarkers(imgTree)
        if markerids is not None:
            for i in range(0, len(markerids)):
                if markerids[i][0] in self.markerIds:
                    p0 = markerCorners[0][0][0]
                    p1 = markerCorners[0][0][1]
                    p01 = p0 - p1
                    l = p01[0] * p01[0] + p01[1] * p01[1]
                    marker = math.sqrt(l)
                    dist = self.distance_to_camera(self.KNOW_WIDTH_MARKER, self.focalLength, marker)

                    point = markerCorners[0][0][0]

                    ray = self.getRay(point)
                    pos = getPosition(self.cameraPos, ray, dist)
                    if not (markerids[i][0] in self.markerPositions.keys()):
                        self.markerPositions[markerids[i][0]]=[]
                    self.markerPositions[markerids[i][0]].append(pos)

    #add a new maker to follow
    def addMarker(self,idMarker):
        self.markerIds.append(idMarker)
        

    #try to remove a marker from the marker's list return true if it works
    def removeMarker(self,idMarker):
        if idMarker not in self.markerIds:
            return False
        self.markerIds.remove(idMarker)

    #GETTERS AND SETTERS
    def setFOV(self,value):
        self.FOV=value

    def getFOV(self):
        return self.FOV

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