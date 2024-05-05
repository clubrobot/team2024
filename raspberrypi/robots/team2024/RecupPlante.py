import math
import numpy as np
from time import sleep
class RecupPile:

    def __init__(self, wheeledbase, barriere, pos_depose, pos_plante, theta_normal=None) -> None:
        self.wb=wheeledbase
        self.pos=np.array(positionPoint)
        self.radiusRobot=400
        self.radiusPince=230
        self.approach_range = 130
        self.forward_distance = 260
        self.barriere=barriere
        self.actionpoint=None
        self.orientation=None
        self.endPoint=np.array(endPoint)
        #Si theta normal is none, auto calcul avec getpos
        pass

    def calc_point_approche(self, pos_plante, theta_normal):
        x = pos_plante[0] - self.approach_range*np.cos(theta_normal)
        y = pos_plante[1] - self.approach_range*np.sin(theta_normal)
        return (x,y)

    def procedure(self, robot):
        #Pos à point d'approche puis angle normal
        #avance distance
        #ferme barriere
        #depose base
        #ouvre
        #recule
        #demi tour
        #et fini


        rPos=np.array(self.wb.get_position()[:2])
        vecPos=self.pos-rPos[:2]
        length=math.sqrt(vecPos[0]**2+vecPos[1]**2)
        stop=vecPos/length*(length-self.radiusRobot)+rPos
        ang=math.acos(vecPos[0]/length)
        if(vecPos[1]<0):
            ang*=-1
        if(length-self.radiusRobot>0):
            self.wb.goto_stop(stop[0],stop[1],robot.sensors,theta=ang)
            print(self.wb.get_position(),stop)
        self.pince.ouvrir()
        self.asc.bas()
        stop=vecPos/length*(length-self.radiusPince)+rPos
        self.wb.goto_stop(stop[0],stop[1],robot.sensors,theta=ang)
        print(self.wb.get_position(),stop)
        #sleep(2)
        self.pince.fermer()
        self.asc.rouler()

        #va poser à la fin
        rPos=np.array(self.wb.get_position()[:2])
        vecPos=self.endPoint-rPos
        length=math.sqrt(vecPos[0]**2+vecPos[1]**2)
        stop=vecPos/length*(length-self.radiusPince)+rPos
        ang=math.acos(vecPos[0]/length)
        if(vecPos[1]<0):
            ang*=-1

        self.wb.goto_stop(stop[0],stop[1],robot.sensors,theta=ang)
        print(self.wb.get_position(),stop)
        #sleep(4)
        self.asc.bas()
        self.pince.semi_ouvrir()
        self.asc.rouler()
        
        #si ascenseur pas besoin de ca
        #self.wb.set_openloop_velocities(-500,-500)
        #sleep(0.3)
        #self.wb.stop()
        