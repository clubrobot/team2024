import math

from tracking.jetson.AccessibleMap import AccessibleMap as AccessibleMap
from tracking.libs.positionDetectorMultiple import PositionDetectorMultiple
import numpy as np
from managers.simple_wifi import WiFiManager
import time
#manque concurrence et paramétrage
class JetsonManager:

    def __int__(self):
        GET_MARKER_POSITION_OPCODE = 0x20
        COMPUTE_PATH_OPCODE = 0x21  # attention calcul path si modif carte en même temps

        self.communication= WiFiManager("localhost",9542,"server")
        self.communication.functions_call[GET_MARKER_POSITION_OPCODE]=self.computePath
        self.communication.functions_call[COMPUTE_PATH_OPCODE]=self.computePath
        self.communication.start()

    def computePath(self,args):
        depart, arrive=args[0],args[1]
        #faire gaffe modif concurente
        return map.path_finding(depart[0],depart[1],arrive[0],arrive[1])

    def getMarkerPosition(self,id):
        if detector.markerPositions.keys().__contains__(id):
            return detector.markerPositions[id]
        return -1

if(__name__=="__main__"):
    cameraPosition = np.array([1500, 1000, 300])
    cameraPitch = math.pi / 2
    cameraYaw = 0

    markerObstacle = [17]
    markerFollow = []

    manager = JetsonManager()

    map = AccessibleMap(20, 100)
    detector = PositionDetectorMultiple()
    for marker in markerObstacle:
        detector.addMarker(marker)
    for marker in markerFollow:
        detector.addMarker(marker)

    # INIT
    detector.init(cameraPosition, cameraPitch, cameraYaw)
    print("FIN INIT")

    while (True):
        detector.update()
        map.reset()

        for m in markerObstacle:
            if not detector.markerPositions.keys().__contains__(m):
                continue
            for pos in detector.markerPositions[m]:
                if pos[0] >= 0 and pos[1] >= 0:
                    map.addAreaAroundPoint(pos[0], pos[1])

            time.sleep(0.05)