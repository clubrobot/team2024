from team2022.raspberrypi.tracking.libs.positionDetectorMultiple import *
import math

posdetect=PositionDetectorMultiple()
posdetect.addMarker(17)
posdetect.init([0,0,0],math.radians(90),0)

while True:
    posdetect.update()
    print(posdetect.markerPositions)
