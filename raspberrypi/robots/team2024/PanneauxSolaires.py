import math
import numpy as np
from time import sleep
from behaviours.robot_behaviour import RobotBehavior
from robots.team2024.barriere import Barriere
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.sensors import Sensors

from tunings.tunings_robeur import POSITIONCONTROL_LINVELMAX_VALUE, POSITIONCONTROL_LINVELMAX_ID
from common.serialtypes import FLOAT, STRING, INT

class PanneauxSolaires:
    def __init__(self, wheeledbase: WheeledBase, barriere:Barriere, robot, side, middle,sensors:Sensors) -> None:
        self.wb=wheeledbase

        self.radiusRobot=400
        self.radiusAile=165 # diminue égal plus proche du mur; inversement
        self.forward_distance = 260
        self.barriere=barriere
        self.actionpoint=None
        self.orientation=None
        self.actionpoint_precision=None
        self.get_side = side
        self.middle=middle
        self.robot=robot
        self.sensors=sensors

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
            #depart = np.flip(np.array(self.robot.geo.get('BaseB1INIT')) + np.array([0,0]))
            fin = np.flip(np.array(self.robot.geo.get('PSBleuFin')) + np.array([self.radiusAile,-130]))
        else:
            ang_approche = 0
            #depart = np.flip(np.array(self.robot.geo.get('BaseJ1INIT')) + np.array([0,0]))
            fin = np.flip(np.array(self.robot.geo.get('PSJauneFin')) + np.array([self.radiusAile,140]))

        
        #self.wb.goto_stop(depart[0],depart[1],self.robot.sensors,theta=ang_approche)
        if(not self.yellow): 
            self.barriere.aile_d_ferme()
            self.barriere.ferme_droite()
        else: 
            self.barriere.aile_g_ferme()
            self.barriere.ferme_gauche()
        ############################################ Avance
        pos =self.wb.get_position()
        self.wb.goto_stop(pos[0],pos[1],self.sensors,theta=ang_approche)
        self.wb.goto_stop(fin[0],fin[1],self.sensors,theta=ang_approche, linvelmax=POSITIONCONTROL_LINVELMAX_VALUE*0.2)

        self.wb.set_parameter_value(POSITIONCONTROL_LINVELMAX_ID, POSITIONCONTROL_LINVELMAX_VALUE, FLOAT)

        if(not self.yellow): self.barriere.aile_d_ouvre()
        else: self.barriere.aile_g_ouvre()

        self.barriere.nicole_oouuuuuvre()
