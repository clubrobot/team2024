from common.components import Manager
from daughter_cards.actionneur import Actionneur
from daughter_cards.wheeledbase import WheeledBase
from robots.team2023.ascenseur import Ascenseur
from robots.team2023.pince import Pince
from daughter_cards.sensors import Sensors,ThreadSensors
from threading import Thread
from common.geogebra import Geogebra
from common.roadmap import RoadMap
from common.gpiodevices import Switch,LightButton,gpio_pins
from robots.team2023.RecupPile import RecupPile
from time import sleep,time
import numpy as np

import os
import math

class Robot:
    def __init__(self,manager,side) -> None:
        for root, dirs, files in os.walk("."):
            for file in files:
                if file == "map_2023.ggb":
                    roadmap_path = os.path.join(root, file)
        
        self.geo  = Geogebra(roadmap_path)#"robots/team2023/map_2023.ggb"
        self.road = RoadMap.load(self.geo)
        self.side = side

        self.actionneur = Actionneur(manager, "actionneurs")
        self.actionneur.SetServoAngle(300)
        self.wheeledbase = WheeledBase(manager)
        #self.display = display
        self.pince= Pince(self.actionneur)
        self.ascenseur=None
        self.ascenseur= Ascenseur(self.actionneur)
        self.sensors=Sensors(manager,"sensors")
        self.threadSensors=ThreadSensors(self.sensors,self)

        #self.sensors=None
        self.blue=self.side=="BLUE"

        h=115
        v=220


        self.automate = []#get 3 couleurs puis gerber puis poser cerises
        if(self.blue):#couleur impaire
            self.wheeledbase.set_position(v/2,3000-h/2-50,-math.pi/2)
            self.base=self.geo.get('ZB1')
            self.end=self.geo.get('ZB2')
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Rose1'),np.array(self.base)+(-90,110),self.pince,self.ascenseur))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Jaune1'),np.array(self.base)+(110,110),self.pince,self.ascenseur))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Noir1'),np.array(self.base)+(0,-80),self.pince,self.ascenseur))
            
        else:#couleur paire
            self.base=self.geo.get('ZV1')
            self.end=self.geo.get('ZV2')
            self.wheeledbase.set_position(2000-v/2,3000-h/2-50,-math.pi/2)
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Rose2'),np.array(self.base)+(90,110),self.pince,self.ascenseur))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Jaune2'),np.array(self.base)+(-90,110),self.pince,self.ascenseur))
            self.automate.append(RecupPile(self.wheeledbase,self.geo.get('Noir2'),np.array(self.base)+(0,-80),self.pince,self.ascenseur))
            

    def start(self):
        orange_button=LightButton(gpio_pins.INTER_4_PIN,gpio_pins.LED4_PIN)#orange:2 vert:1 bleu:3 rouge :4
        orange_button.set_function(orange_button.switch)
        orange_button.on()
        tirette=Switch(gpio_pins.TIRETTE_PIN)
        self.wheeledbase.goto_stop(self.base[0],self.base[1],sensors=self.sensors)
        #attend tirette
        while not tirette.button.is_pressed:
            if(orange_button.button.is_pressed):
                return False
            sleep(0.003)
        
        debut=time()
        print("tiretté")

        self.wheeledbase.goto_stop(3000-115/2-50,self.base[1],sensors=self.sensors,theta=-math.pi/2)
        self.actionneur.SetServoAngle(0)
        self.automate[0].procedure(self)
        if(orange_button.button.is_pressed or (time()-debut)>90):
            return (time()-debut)>90
        self.automate[1].procedure(self)
        if(orange_button.button.is_pressed or (time()-debut)>90):
            return (time()-debut)>90
        self.automate[2].procedure(self)
        if(orange_button.button.is_pressed or (time()-debut)>90):
            return (time()-debut)>90
        self.wheeledbase.goto_stop(self.end[0],self.end[1],sensors=self.sensors)
        self.threadSensors.looping=False
        return True


from common.components import Manager
manager = Manager("10.0.0.2")

manager.connect(7)

#1 VERIF QUE TURN ON THE SPOT s'arrète bien avec les capteurs
#2 TUNER LA DISTANCE D'ARRET
#3 FAIRE EXECUTER LE CODE EN LOCAL sur le robot
#4 pouvoir utiliser l'ascenseur et la pince 
#5 améliorer a stratégie 


from setups.setup_serialtalks import *
green_button=LightButton(gpio_pins.INTER_1_PIN,gpio_pins.LED1_PIN)#orange:2 vert:1 bleu:3 rouge :4
green_button.set_function(green_button.switch)
blue_button=LightButton(gpio_pins.INTER_3_PIN,gpio_pins.LED3_PIN)#orange:2 vert:1 bleu:3 rouge :4
blue_button.set_function(blue_button.switch)
blue_button.on()
green_button.on()
bornibus=None
print("CHOIX COULEUR")
initOk=False
while not initOk:
    #bornibus=Robot(manager=manager,side="BLUE")
    while(bornibus==None):
        if(green_button.button.is_pressed):
            bornibus=Robot(manager=manager,side="GREEN")
            blue_button.off()
            green_button.on()
            print("TEAM VERTE")
        elif(blue_button.button.is_pressed):
            bornibus=Robot(manager=manager,side="BLUE")
            green_button.off()
            blue_button.on()
            print("team bleu")
    
    initOk=bornibus.start()