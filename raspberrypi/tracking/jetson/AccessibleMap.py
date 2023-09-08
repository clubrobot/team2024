import numpy as np
import team2022.raspberrypi.tracking.jetson.AvoidancePathfinding as AvoidancePathfinding

class AccessibleMap:

    def __init__(self, h, radius):
        self.L = 2000
        self.H = 3000
        self.h = h
        self.nh = int(self.H / h + 2)
        self.nl = int(self.L / h + 2)
        self.radius = radius / h
        self.emptyMap = np.zeros((self.nl, self.nh), dtype=int)
        self.emptyMap[1:-1, 1:-1] = 1
        self.loadMapFromGeogebra()
        self.reset()

    def reset(self):
        self.map = np.copy(self.emptyMap)

    def path_finding(self,dx,dy,ex,ey):
        opti_path=AvoidancePathfinding.path_finding(self.map,int(dx/self.h)+1,int(dy/self.h)+1,int(ex/self.h)+1,int(ey/self.h)+1)
        print(opti_path)
        print(int(dx/self.h)+1,int(dy/self.h)+1,int(ex/self.h)+1,int(ey/self.h)+1)
        opti_path.append(np.array([ex,ey])/self.h+1)
        opti_path=np.array(opti_path)
        opti_path=(opti_path-1)*self.h
        return opti_path

    def loadMapFromGeogebra(self):
        print("Load map from geogebra")
        points = np.array([[[1000, 100], [1001, 2525]]], dtype=int)  # charger à partir de geogebra
        for rect in points:
            rect = rect / self.h + 1
            bottom = [int(min(rect[0, 0], rect[1, 0])), int(min(rect[0, 1], rect[1, 1]))]
            top = [int(max(rect[0, 0], rect[1, 0])), int(max(rect[0, 1], rect[1, 1]))]
            for i in range(bottom[0], top[0]):
                for j in range(bottom[1], top[1]):

                    self.addAreaAroundPoint(i, j, rescale=False, onEmptyMap=True)
            print(bottom, top)

    def addAreaAroundPoint(self, x, y, rescale=True, onEmptyMap=False):
        if rescale:
            x = int(x / self.h) + 1
            y = int(y / self.h) + 1
        mx = int(max(0, x - self.radius - 1))
        lx = int(min(self.nl - 1, x + self.radius + 3) - max(0, x - self.radius - 1))
        my = int(max(0, y - self.radius - 1))
        ly = int(min(self.nh - 1, y + self.radius + 3) - max(0, y - self.radius - 1))

        map = self.emptyMap[mx:(mx + lx), my:(my + ly)]

        if not onEmptyMap:
            map = self.map[mx:(mx + lx), my:(my + ly)]
        x_map = np.repeat(np.arange(mx, mx + lx), ly).reshape(lx, ly)-x

        y_map = np.transpose(np.repeat(np.arange(my, my + ly), lx).reshape(ly,lx))-y

        dist = np.sqrt(x_map ** 2 + y_map ** 2)
        map[dist <= self.radius] = 0

        if not onEmptyMap:
            self.map[mx:(mx + lx), my:(my + ly)] = map
        else:
            self.emptyMap[mx:(mx + lx), my:(my + ly)] = map
