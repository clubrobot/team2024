import math
import numpy as np
from time import sleep
from behaviours.robot_behaviour import RobotBehavior
from robots.team2024.barriere import Barriere
from daughter_cards.wheeledbase import WheeledBase

class PanneauxSolaires:
    def __init__(self, wheeledbase: WheeledBase, barriere:Barriere, robot, side, middle) -> None:
        self.wb=wheeledbase

        self.radiusRobot=400
        self.radiusAile=255 # - égal plus proche du mur; inversement
        self.forward_distance = 260
        self.barriere=barriere
        self.actionpoint=None
        self.orientation=None
        self.actionpoint_precision=None

        self.blue=side==RobotBehavior.BLUE_SIDE
        self.middle=middle
        self.robot=robot

    """ 
    def calc_point_approche(self, pos_plante, theta_normal):
        x = pos_plante[0] - self.approach_range*np.cos(theta_normal)
        y = pos_plante[1] - self.approach_range*np.sin(theta_normal)
        return (x,y) """

    def procedure(self):
        #Approche point départ
        #On tourne pi/2 ou -pi/2
        #bras
        #avance
        #bras
        #fin
        
        self.barriere.aile_d_ouvre()
        self.barriere.aile_g_ouvre()
        ############################################## Approche
        if(self.blue): 
            ang_approche = np.pi
            depart = np.array(self.robot.geo.get('PSBleuDépart')) + (self.radiusAile,0)
            fin = np.array(self.robot.geo.get('PSBleuFin')) + (self.radiusAile,0)
        else:
            ang_approche = 0
            depart = np.array(self.robot.geo.get('PSBleuDépart')) + (self.radiusAile,0)
            fin = np.array(self.robot.geo.get('PSBleuFin')) + (self.radiusAile,0)


        
        self.wb.goto_stop(depart[0],depart[1],self.robot.sensors,finalangle=ang_approche)
        if(self.blue): self.barriere.aile_d_ferme()
        else: self.barriere.aile_g_ferme()

        ############################################ Avance

        self.wb.goto_stop(fin[0],fin[1],self.robot.sensors,finalangle=ang_approche)

        if(self.blue): self.barriere.aile_d_ouvre()
        else: self.barriere.aile_g_ouvre()
