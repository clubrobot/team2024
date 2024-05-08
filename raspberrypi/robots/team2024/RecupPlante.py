import math
import numpy as np
from time import sleep
from robots.team2024.barriere import Barriere
from daughter_cards.wheeledbase import WheeledBase

from tunings.tunings_robeur import POSITIONCONTROL_LINVELMAX_VALUE, POSITIONCONTROL_LINVELMAX_ID, POSITIONCONTROL_ANGVELMAX_VALUE, POSITIONCONTROL_ANGVELMAX_ID
from common.serialtypes import FLOAT, STRING, INT

class RecupPlante:
    def __init__(self, wheeledbase: WheeledBase, barriere:Barriere, robot, pos_depose, pos_plante, final) -> None:
        self.wb=wheeledbase
        self.robot=robot
        self.pos=np.flip(np.array(pos_plante))
        self.radiusRobot=220
        self.radiusPince=30
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

        ###APPROCHE
        pos = self.wb.get_position()
        rPos=np.array(pos[:2])
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

        ######On prends
        self.barriere.nicole_oouuuuuvre()

        stop=vecPos/length*(length-self.radiusPince)+rPos
        self.wb.goto_stop(stop[0],stop[1], self.robot.sensors,theta=ang, linvelmax=POSITIONCONTROL_LINVELMAX_VALUE*0.2)

        self.wb.set_parameter_value(POSITIONCONTROL_LINVELMAX_ID, POSITIONCONTROL_LINVELMAX_VALUE, FLOAT)

        self.barriere.ferme()

        #va poser à la fin
        pos = self.wb.get_position()
        rPos=np.array(pos[:2])
        vecPos=self.endPoint-rPos
        length=math.sqrt(vecPos[0]**2+vecPos[1]**2)
        stop=vecPos/length*(length-self.radiusPince)+rPos
        ang=math.acos(vecPos[0]/length)
        if(vecPos[1]<0):
            ang*=-1
        
        self.wb.goto_stop(rPos[0],rPos[1], self.robot.sensors,theta=ang, angvelmax=POSITIONCONTROL_ANGVELMAX_VALUE*0.05)
        self.wb.goto_stop(stop[0],stop[1], self.robot.sensors,theta=ang, angvelmax=POSITIONCONTROL_ANGVELMAX_VALUE, linvelmax=POSITIONCONTROL_LINVELMAX_VALUE*0.2)
        self.wb.set_parameter_value(POSITIONCONTROL_LINVELMAX_ID, POSITIONCONTROL_LINVELMAX_VALUE, FLOAT)

        self.barriere.nicole_oouuuuuvre()
        #On recule pour le prochain
        if(not self.final):
            stop[0]=stop[0]-150*np.cos(ang)
            stop[1]=stop[1]-150*np.sin(ang)
            self.wb.goto_stop(stop[0],stop[1], self.robot.sensors,theta=ang+np.pi)
        
        sleep(0.3)
        
        
        #si ascenseur pas besoin de ca
        #self.wb.set_openloop_velocities(-500,-500)
        #sleep(0.3)
        #self.wb.stop()
        