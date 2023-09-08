
from behaviours.robot_behaviour import RobotBehavior
from math import pi
from threading import Semaphore
from common.geogebra import Geogebra
from common.roadmap import RoadMap
from daughter_cards.wheeledbase import WheeledBase
from robots.team2023.ascenseur import Ascenseur
from robots.team2023.pince import Pince
from daughter_cards.sensors import Sensors
from threading import Thread
from robots.team2023.RecupPile import RecupPile
import os

COLOR = RobotBehavior.YELLOW_SIDE
PREPARATION = False


class Bornibus(RobotBehavior):
    """This class is the main objet of bornibus robot, it contain all the action list and initial configuration to run a match

    Args:
        RobotBehavior (class): The main bornibus class inherit from the global robot behaviour in order to have a common behaviour for each robot you want
    """

    def __init__(self, manager, *args, timelimit=None, **kwargs):
        """The initialisation function create all functional module of the robot. This function also instanciate all the match actions

        Args:
            manager (class): One instance of the manager client. It is the client part of th proxy to have access of all the arduino daughter cards
            timelimit (int, optional): The match time limit, usualy set to 100 seconds. Defaults to None.
        """
        RobotBehavior.__init__(self, manager, *args,
                               timelimit=timelimit, **kwargs)

        #self.avoidance_behaviour = AviodanceBehaviour(
        #    wheeledbase, roadmap, robot_beacon, sensors)
        for root, dirs, files in os.walk("."):
            for file in files:
                if file == "map_2023.ggb":
                    roadmap_path = os.path.join(root, file)
        
        self.geo  = Geogebra(roadmap_path)#"robots/team2023/map_2023.ggb"
        self.road = RoadMap.load(self.geo)
        self.side = RobotBehavior.BLUE_SIDE

        self.wheeledbase = WheeledBase(manager)
        #self.display = display
        self.pince= Pince(manager)
        self.ascenseur= Ascenseur(manager)
        self.sensors=Sensors(manager,"sensors")
        #self.sensors=None
        self.blue=self.side==RobotBehavior.BLUE_SIDE

        self.automate = []#get 3 couleurs puis gerber puis poser cerises
        if(self.blue):#couleur impaire
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Rose1'),self.geo.get('ZB1'),self.pince))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Jaune1'),self.geo.get('ZB1'),self.pince))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Noir1'),self.geo.get('ZB1'),self.pince))
        else:#couleur paire
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Rose2'),self.geo.get('ZV1'),self.pince))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Jaune2'),self.geo.get('ZV1'),self.pince))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Noir2'),self.geo.get('ZV1'),self.pince))

        self.automatestep = 0

        self.p = Semaphore(0)
        print("fin")

    def make_decision(self):
        """This function make a decision to choose the next action to play. Today it basically return th next action on list
           /!\ You can describe here you own decision behaviour but the return parameter needs to be the same.

        Returns:
            [function pointer, class pointer, tuple, float, float]: This function return the next action procedure pointer,
            a pointer of itself in order the have full robot acess inside procedure method. The destnation tuple and the precision to reach.
        """
        if(self.automatestep < len(self.automate)):
            action = self.automate[self.automatestep]
        else:
            #self.display.love(100)
            self.stop_event.set()
            return None, (self,), {}, (None, None)

        return action.procedure, (self,), {}, (action.actionpoint + (action.orientation,), (action.actionpoint_precision, None))

    def goto_procedure(self, destination, thresholds=(None, None)):
        """The method describe the behaviour to reach an action point, it use the avoidance beahviour class that describe how to avoid an obstacle.

        Args:
            destination (tuple): the x, y, theta action point
            thresholds (tuple, optional): The optional precision to reach a point. Defaults to (None, None).

        Returns:
            bool: Return True when the robot successfuly reach the desired position false other.
        """
        if self.wheeledbase.goto_stop(destination[0],destination[1],self.sensors ):
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
        if self.side == RobotBehavior.YELLOW_SIDE:
            self.wheeledbase.set_position(self.geo.get('ZV1'), -pi/2)
        else:
            self.wheeledbase.set_position(self.geo.get('ZB1'), pi/2)

    def positioning(self):
        """This optionnal function can be useful to do a small move after setting up the postion during the preparation phase
        """
        if self.side == RobotBehavior.YELLOW_SIDE:
            self.wheeledbase.goto(self.geo.get('ZV1'), -pi/2)
        else:
            self.wheeledbase.goto(self.geo.get('ZB1'), pi/2)

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
        import time
        time.sleep(95)
        self.actionneur.raise_flag()
        time.sleep(4)
        self.wheeledbase.stop()
        self.display.love(duration=1000)
        self.p.release()
        self.manager.end_game()


if __name__ == '__main__':
    manag=None#Manager('10.0.0.7')
    if PREPARATION:
        Bornibus(manag).start_preparation()
    else:
        robot = Bornibus(manag)
        robot.set_side(COLOR)
        #init_robot()
        robot.set_position()
        input()
        robot.positioning()
        input()
        robot.start()
