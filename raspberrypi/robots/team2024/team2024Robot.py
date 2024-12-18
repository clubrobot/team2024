
from behaviours.robot_behaviour import RobotBehavior
from math import pi
import numpy as np
from threading import Semaphore
from common.geogebra import Geogebra
from common.roadmap import RoadMap
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.sensors import Sensors
import time
from robots.team2024.RecupPlante import RecupPlante
from robots.team2024.PanneauxSolaires import PanneauxSolaires
from robots.team2024.barriere import Barriere

from threading import Thread
import os

COLOR = RobotBehavior.YELLOW_SIDE
PREPARATION = True

ROBOT_LENGHT = 0 #en mm, longeur
ROBOT_WIDTH = 0 #en mm, largeur

class Robeur(RobotBehavior):
    """This class is the main objet of bornibus robot, it contain all the action list and initial configuration to run a match

    Args:
        RobotBehavior (class): The main bornibus class inherit from the global robot behaviour in order to have a common behaviour for each robot you want
    """

    def __init__(self, *args, timelimit=None, **kwargs):
        """The initialisation function create all functional module of the robot. This function also instanciate all the match actions

        Args:
            manager (class): One instance of the manager client. It is the client part of th proxy to have access of all the arduino daughter cards
            timelimit (int, optional): The match time limit, usualy set to 100 seconds. Defaults to None.
        """
        RobotBehavior.__init__(self, *args,
                               timelimit=timelimit, **kwargs)

        #self.avoidance_behaviour = AviodanceBehaviour(
        #    wheeledbase, roadmap, robot_beacon, sensors)
        for root, dirs, files in os.walk("."):
            for file in files:
                if file == "map_2024.ggb":
                    roadmap_path = os.path.join(root, file)
        
        self.geo  = Geogebra(roadmap_path)#"robots/team2023/map_2024.ggb"
        self.road = RoadMap.load(self.geo)
        self.side = RobotBehavior.BLUE_SIDE

        """ 
         self.wheeledbase = WheeledBase()
        self.wheeledbase.start_match()
        """
        #self.display = display

        self.sensors=Sensors("sensors")
        self.sensors.publish_logs()

        self.barriere=Barriere()
        self.barriere.nicole_oouuuuuvre()
        self.barriere.aile_d_ouvre()
        self.barriere.aile_g_ouvre()
        self.blue=self.side==RobotBehavior.BLUE_SIDE
        
        self.automate = []
        #self.automate.append(PanneauxSolaires(self.wheeledbase,self.barriere,self, self.get_side, False))
        #self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseJ1'), np.array(self.geo.get('BaseJ1'))+np.array([0,670])))
        '''
        if(self.blue):#couleur impaire
            self.automate.append(PanneauxSolaires(self.wheeledbase,self.barriere,self, self.get_side, False))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseB1'), self.geo.get('PlanteB1'), False))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseB2'), self.geo.get('PlanteB2'), False))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseB3'), self.geo.get('PlantePAMI'), True))
        else:#couleur paire
            self.automate.append(PanneauxSolaires(self.wheeledbase,self.barriere,self, self.get_side, False))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseJ1'), self.geo.get('PlanteJ1'), False))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseJ2'), self.geo.get('PlanteJ2'), False))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseJ3'), self.geo.get('PlantePAMI'), True))
        '''

        print("BLUEEE")
        print(self.blue)
        self.automatestep = 0

        self.p = Semaphore(0)
        print("fin")

    def get_side(self):
        return self.side

    def make_decision(self):
        """This function make a decision to choose the next action to play. Today it basically return th next action on list
           /!\ You can describe here you own decision behaviour but the return parameter needs to be the same.

        Returns:
            [function pointer, class pointer, tuple, float, float]: This function return the next action procedure pointer,
            a pointer of itself in order the have full robot acess inside procedure method. The destnation tuple and the precision to reach.
        """
        action=None

        if(self.automatestep < len(self.automate)):
            action = self.automate[self.automatestep]
        else:
            #self.display.love(100)
            self.stop_event.set()
            return None
        return action.procedure

    def goto_procedure(self, destination, thresholds=(None, None)):
        """The method describe the behaviour to reach an action point, it use the avoidance beahviour class that describe how to avoid an obstacle.

        Args:
            destination (tuple): the x, y, theta action point
            thresholds (tuple, optional): The optional precision to reach a point. Defaults to (None, None).

        Returns:
            bool: Return True when the robot successfuly reach the desired position false other.
        """
        if self.wheeledbase.goto_stop(destination[0],destination[1],self.sensors):
            #self.display.happy()
            self.automatestep += 1
            return True
        else:
            #self.display.surprised()
            return False

    def set_side(self, side):
        """This function is called during the preparation phase in order to choose the starting side

        Args:
            side (int): Yellow or blue
        """
        self.side = side

    def set_position(self):
        """This function apply the starting position of the robot reagading to the choosed side
        """
        print("SIDDDDEEE: {}".format(self.side))
        if self.side == RobotBehavior.YELLOW_SIDE:
            #150 en x 100 en y
            self.wheeledbase.set_position(100, 150, 0)
        else:
            self.wheeledbase.set_position(2900, 150, pi)
            
        self.blue=self.side==RobotBehavior.BLUE_SIDE
        if(self.blue):#couleur impaire
            self.automate.append(PanneauxSolaires(self.wheeledbase,self.barriere,self, self.get_side, False,self.sensors))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseB1'), self.geo.get('PlanteB1'), False,self.sensors))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseB2'), self.geo.get('PlanteB2'), False,self.sensors))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseB3'), self.geo.get('PlantePAMI'), True,self.sensors))
        else:#couleur paire
            self.automate.append(PanneauxSolaires(self.wheeledbase,self.barriere,self, self.get_side, False,self.sensors))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseJ1'), self.geo.get('PlanteJ1'), False,self.sensors))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseJ2'), self.geo.get('PlanteJ2'), False,self.sensors))
            self.automate.append(RecupPlante(self.wheeledbase, self.barriere, self, self.geo.get('BaseJ3'), self.geo.get('PlantePAMI'), True,self.sensors))

    def positioning(self):
        """This optionnal function can be useful to do a small move after setting up the postion during the preparation phase
        """
        print(self.wheeledbase.get_position())
        print(self.geo.get('BaseJ1'))
        print(self.geo.get('BaseB1'))
        if self.side == RobotBehavior.YELLOW_SIDE:
            self.wheeledbase.goto(self.geo.get('BaseJ1INIT')[1], self.geo.get('BaseJ1INIT')[0],0)
        else:
            print("GOTO bLUE")
            self.wheeledbase.goto(self.geo.get('BaseB1INIT')[1], self.geo.get('BaseB1INIT')[0], pi)

        #time.sleep(1)
        #self.lastknownpos = self.wheeledbase.get_position()
        #self.wheeledbase.wheeledbase.disconnect()
    def start_procedure(self):
        """This action is launched at the beggining of the match
        """

        Thread(target=self.stop_match).start()
        #self.display.start()

    def stop_procedure(self):
        """Optionnal function running at the end of match. Usually used to check if the funny action is end
        """
        self.p.acquire(blocking=True)

    def stop_match(self):
        pass
        '''import time
        time.sleep(95)
        time.sleep(4)
        self.wheeledbase.stop()
        self.p.release()
        '''


if __name__ == '__main__':
    if PREPARATION:
        Robeur().start_preparation()
    else:
        robot = Robeur()
        robot.set_side(COLOR)
        #init_robot()
        robot.set_position()
        input()
        robot.positioning()
        input()
        robot.start()
