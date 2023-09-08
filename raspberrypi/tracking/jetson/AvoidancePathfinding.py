import bisect
import time
import numpy as np

def addNeigh(access, closed, open, x, y, ox, oy):
    if access[x][y][0] == 0 or access[x, y, 5] == 1:#closed.__contains__((x, y)) or open.__contains__((x, y))
        return
    access[x][y][1:3] = ox, oy
    access[x][y][3]=access[ox][oy][3]
    access[x, y, 5] = 1
    bisect.insort(open,(x,y),key=lambda c:access[c[0],c[1],3]+access[c[0],c[1],4])
    #open.append((x, y))

def lengthPath(path):
    l=0
    for i in range(len(path)-1):
        l+=np.linalg.norm(path[i]-path[i+1])
    return l

def computeLinePath(path, accessible):
    bpx = 0.5 + path[0, 0]
    bpy = 0.5 + path[0, 1]

    linePath = [[bpx, bpy]]
    for i in range(1, len(path)):
        epx = 0.5 + path[i, 0]
        epy = 0.5 + path[i, 1]
        cx = path[i, 0]
        cy = path[i, 1]
        vx = bpx - epx
        vy = bpy - epy

        dx = [-1, 1][vx > 0]
        dy = [-1, 1][vy > 0]

        intersect = False
        ix = 0.5 * dx + bpx
        iy = 0.5 * dy + bpy

        t = 0
        while t < 1 and not intersect:
            tx = abs((ix - bpx) / (10 ** -15 + vx))
            ty = abs((iy - bpy) / (10 ** -15 + vy))

            if (min(tx, ty) > 1):
                t = tx
                continue

            if (tx < ty):
                t = tx
                cx += dx
                ix += dx
                if (accessible[cx, cy, 0] == 0):
                    intersect = True
            else:
                t = ty
                cy += dy
                iy += dy
                if (accessible[cx, cy, 0] == 0):
                    intersect = True
        if (intersect):
            bpx = 0.5 + path[i - 1, 0]
            bpy = 0.5 + path[i - 1, 1]
            linePath.append([bpx, bpy])
    linePath.append([0.5 + path[len(path) - 1, 0], 0.5 + path[len(path) - 1, 1]])
    return linePath

def path_finding(map,dx,dy,ex,ey):
    d = time.time()
    accessible=np.zeros((map.shape[0],map.shape[1],6),dtype="int")
    accessible[:,:,0]=map

    currentX = dx
    currentY = dy
    closedList = []

    openList = []
    #opti ca

    for i in range (map.shape[0]):
        for j in range(map.shape[1]):
            accessible[i,j,4]=abs(i-ex)+abs(j-ey)
    accessible[currentX,currentY,5]=1
    while currentY != ey or currentX != ex:
        addNeigh(accessible, closedList, openList, currentX + 1, currentY, currentX, currentY)
        addNeigh(accessible, closedList, openList, currentX - 1, currentY, currentX, currentY)
        addNeigh(accessible, closedList, openList, currentX, currentY + 1, currentX, currentY)
        addNeigh(accessible, closedList, openList, currentX, currentY - 1, currentX, currentY)

        #closedList.append((currentX, currentY))
        if (len(openList) == 0):
            print("ERREUR CHEMIN INACCESSIBLE")
        currentX = openList[0][0]
        currentY = openList[0][1]
        del openList[0]

    path = [[ex, ey]]
    while currentY != dy or currentX != dx:
        currentX, currentY = accessible[currentX, currentY, 1:3]
        path.append([currentX, currentY])
    path = np.array(path)
    #50% du temps dedans (idée d'opti dichotomie entre point départ et point arrivée).
    linePathEndToBegin = np.flip(computeLinePath(path, accessible), axis=0)
    path = np.flip(path, axis=0)
    linePathBeginToEnd = np.array(computeLinePath(path, accessible))

    ##TROUVER INTERSECTIONS
    intersections = []
    for i in range(len(linePathBeginToEnd) - 1):

        dx, dy = linePathBeginToEnd[i]
        vx, vy = linePathBeginToEnd[i + 1] - linePathBeginToEnd[i]
        a1 = vy;
        b1 = -vx;
        d1 = -b1 * dy - a1 * dx
        l1 = vx ** 2 + vy ** 2
        for j in range(len(linePathEndToBegin) - 1):

            ex, ey = linePathEndToBegin[j]
            wx, wy = linePathEndToBegin[j + 1] - linePathEndToBegin[j]
            a2 = wy
            b2 = -wx
            d2 = -b2 * ey - a2 * ex
            l2 = wx ** 2 + wy ** 2
            if a1 * b2 - b1 * a2 != 0:

                intersect = np.linalg.solve(np.array([[a1, b1], [a2, b2]]),
                                            [-d1, -d2])  # flemme de coder l'inversion a la main

                t1 = ((intersect[0] - dx) * vx + (intersect[1] - dy) * vy) / l1
                t2 = ((intersect[0] - ex) * wx + (intersect[1] - ey) * wy) / l2

                if -10**-10 <= t1 <= 1+10**-10 and -10**-10 <= t2 <= 1+10**-10:
                    intersections.append([intersect, i, j])

    optiPath = []
    ##BOUCLER  PR CHEMIN + COURT
    for bout in range(len(intersections)-1):

        l1 = 0
        p1 = [intersections[bout][0]]
        if (intersections[bout][1] == intersections[bout + 1][1]):
            l1 = np.linalg.norm(intersections[bout + 1][0] - intersections[bout][0])
        else:
            l1 = np.linalg.norm(
                intersections[bout + 1][0] - linePathBeginToEnd[intersections[bout + 1][1]]) + np.linalg.norm(
                intersections[bout][0] - linePathBeginToEnd[intersections[bout][1]])
            for j in range(intersections[bout][1], intersections[bout + 1][1] - 1):
                p1.append(linePathBeginToEnd[j])
                l1 += np.linalg.norm(linePathBeginToEnd[j] - linePathBeginToEnd[j + 1])

        l2 = 0
        p2 = [intersections[bout][0]]
        if (intersections[bout][2] == intersections[bout + 1][2]):
            l2 = np.linalg.norm(intersections[bout + 1][0] - intersections[bout][0])
        else:
            l2 = np.linalg.norm(
                intersections[bout + 1][0] - linePathEndToBegin[intersections[bout + 1][2]]) + np.linalg.norm(
                intersections[bout][0] - linePathEndToBegin[intersections[bout][2]])
            for j in range(intersections[bout][2], intersections[bout + 1][2] - 1):
                p2.append(linePathEndToBegin[j])
                l2 += np.linalg.norm(linePathEndToBegin[j] - linePathEndToBegin[j + 1])

        if (l1 < l2):
            for i in range(len(p1)):
                optiPath.append(p1[i])
        else:
            for i in range(len(p2)):
                optiPath.append(p2[i])

    return optiPath