import math
import numpy as np
from time import sleep
from behaviours.robot_behaviour import RobotBehavior
from robots.team2024.barriere import Barriere
from daughter_cards.wheeledbase import WheeledBase

from tunings.tunings_robeur import POSITIONCONTROL_LINVELMAX_VALUE, POSITIONCONTROL_LINVELMAX_ID
from common.serialtypes import FLOAT, STRING, INT

class PanneauxSolaires:
    def __init__(self, wheeledbase: WheeledBase, barriere:Barriere, robot, side, middle) -> None:
        self.wb=wheeledbase

        self.radiusRobot=400
        self.radiusAile=180 # - égal plus proche du mur; inversement
        self.forward_distance = 260
        self.barriere=barriere
        self.actionpoint=None
        self.orientation=None
        self.actionpoint_precision=None
        self.get_side = side
        self.middle=middle
        self.robot=robot

    """ 
    def calc_point_approche(self, pos_plante, theta_normal):
        x = pos_plante[0] - self.approach_range*np.cos(theta_normal)
        y = pos_plante[1] - self.approach_range*np.sin(theta_normal)
        return (x,y) """

    def procedure(self):
        self.yellow=self.get_side()
        #Approche point départ
        #On tourne pi/2 ou -pi/2
        #bras
        #avance
        #bras
        #fin
        
        self.barriere.aile_d_ouvre()
        self.barriere.aile_g_ouvre()
        ##############################################On fonce

        ############################################## Approche

        if(not self.yellow): 
            ang_approche = np.pi
            depart = np.flip(np.array(self.robot.geo.get('PSBleuFin')) + np.array([self.radiusAile,-120]))
            fin = np.flip(np.array(self.robot.geo.get('PSBleuDepart')) + np.array([self.radiusAile,120]))
        else:
            ang_approche = 0
            depart = np.flip(np.array(self.robot.geo.get('PSJauneFin')) + np.array([self.radiusAile,120]))
            fin = np.flip(np.array(self.robot.geo.get('PSJauneDepart')) + np.array([self.radiusAile,-120]))


        print(self.wb.get_position())
        print(depart)
        self.wb.goto_stop(depart[0],depart[1],self.robot.sensors,theta=ang_approche)
        if(not self.yellow): self.barriere.aile_d_ferme()
        else: self.barriere.aile_g_ferme()
        self.barriere.quarante_cinq()
        ############################################ Avance

        self.wb.goto_stop(fin[0],fin[1],self.robot.sensors,theta=ang_approche, linvelmax=POSITIONCONTROL_LINVELMAX_VALUE*0.4)

        self.wb.set_parameter_value(POSITIONCONTROL_LINVELMAX_ID, POSITIONCONTROL_LINVELMAX_VALUE, FLOAT)

        if(not self.yellow): self.barriere.aile_d_ouvre()
        else: self.barriere.aile_g_ouvre()