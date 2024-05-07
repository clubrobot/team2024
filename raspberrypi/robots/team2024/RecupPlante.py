import math
import numpy as np
from time import sleep
from robots.team2024.barriere import Barriere
from daughter_cards.wheeledbase import WheeledBase

class RecupPlante:
    def __init__(self, wheeledbase: WheeledBase, barriere:Barriere, robot, pos_depose, pos_plante, final) -> None:
        self.wb=wheeledbase
        self.robot=robot
        self.pos=np.flip(np.array(pos_plante))
        self.radiusRobot=220
        self.radiusPince=50
        self.barriere=barriere
        self.actionpoint=None
        self.orientation=None
        self.actionpoint_precision=None
        self.endPoint=np.flip(np.array(pos_depose))
        self.final= final

    """ 
    def calc_point_approche(self, pos_plante, theta_normal):
        x = pos_plante[0] - self.approach_range*np.cos(theta_normal)
        y = pos_plante[1] - self.approach_range*np.sin(theta_normal)
        return (x,y) """

    def procedure(self):
        #Pos à point d'approche puis angle normal
        #avance distance
        #ferme barriere
        #depose base
        #ouvre
        #recule
        #demi tour
        #et fini
        self.barriere.nicole_oouuuuuvre()

        rPos=np.array(self.wb.get_position()[:2])
        vecPos=self.pos-rPos[:2]
        length=math.sqrt(vecPos[0]**2+vecPos[1]**2)
        stop=vecPos/length*(length-self.radiusRobot)+rPos
        ang=math.acos(vecPos[0]/length)
        if(vecPos[1]<0):
            ang*=-1
        print(length-self.radiusRobot)
        if(length-self.radiusRobot>0):
            self.wb.goto_stop(stop[0],stop[1], self.robot.sensors,theta=ang)
            print(self.wb.get_position(),stop)

        self.barriere.nicole_oouuuuuvre()

        stop=vecPos/length*(length-self.radiusPince)+rPos
        self.wb.goto_stop(stop[0],stop[1], self.robot.sensors,theta=ang)

        self.barriere.ferme()

        #va poser à la fin
        rPos=np.array(self.wb.get_position()[:2])
        vecPos=self.endPoint-rPos
        length=math.sqrt(vecPos[0]**2+vecPos[1]**2)
        stop=vecPos/length*(length-self.radiusPince)+rPos
        ang=math.acos(vecPos[0]/length)
        if(vecPos[1]<0):
            ang*=-1

        self.wb.goto_stop(rPos[0],rPos[1], self.robot.sensors,theta=ang)
        self.wb.goto_stop(stop[0],stop[1], self.robot.sensors,theta=ang)
        #On recule pour le prochain
        if(not self.final):
            stop[0]=stop[0]-100*np.cos(ang)
            stop[1]=stop[1]-100*np.sin(ang)
            self.wb.goto_stop(stop[0],stop[1], self.robot.sensors,theta=ang)
        
        #sleep(4)
        self.barriere.nicole_oouuuuuvre()
        
        #si ascenseur pas besoin de ca
        #self.wb.set_openloop_velocities(-500,-500)
        #sleep(0.3)
        #self.wb.stop()
        