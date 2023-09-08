import math

from team2022.raspberrypi.tracking.jetson.AccessibleMap import AccessibleMap as AccessibleMap
from team2022.raspberrypi.tracking.libs.positionDetectorMultiple import PositionDetectorMultiple
import numpy as np
from team2022.raspberrypi.common.tcptalks import TCPTalks
import time
#manque concurrence et paramétrage
class JetsonManager(TCPTalks):

    def __int__(self):
        GET_MARKER_POSITION_OPCODE = 0x20
        COMPUTE_PATH_OPCODE = 0x21  # attention calcul path si modif carte en même temps

        TCPTalks.__init__("10.0.0.2", port=10, id="pi", password="raspberry")
        TCPTalks.connect(10)
        #BIND et applications des fcts
        self.bind(GET_MARKER_POSITION_OPCODE, self.getMarkerPosition)
        self.bind(COMPUTE_PATH_OPCODE, self.computePath)

    def computePath(self,depart,arrive):
        #faire gaffe modif concurente
        return map.path_finding(depart[0],depart[1],arrive[0],arrive[1])

    def getMarkerPosition(self,id):
        if detector.markerPositions.keys().__contains__(id):
            return detector.markerPositions[id]
        return None


cameraPosition = np.array([1500,1000,300])
cameraPitch = math.pi/2
cameraYaw = 0

markerObstacle=[17]
markerFollow=[]

manager=JetsonManager()

map = AccessibleMap(10,100)
detector = PositionDetectorMultiple()
for marker in markerObstacle:
    detector.addMarker(marker)
for marker in markerFollow:
    detector.addMarker(marker)

#INIT
detector.init(cameraPosition,cameraPitch,cameraYaw)
print("FIN INIT")

while(True):
    detector.update()
    map.reset()

    for m in markerObstacle:
        if not detector.markerPositions.keys().__contains__(m):
            continue
        for pos in detector.markerPositions[m]:
            if pos[0]>=0 and pos[1]>=0:
                map.addAreaAroundPoint(pos[0],pos[1])

        time.sleep(0.05)