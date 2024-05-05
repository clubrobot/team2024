#from setups.setup_display import *
from behaviours.robot_behaviour import RobotBehavior
#from common.components import LightButtonProxy, SwitchProxy
from threading import Semaphore
from common.gpiodevices import Switch, LightButton, gpio_pins
from logs.logger import Logger
from threading import Thread
import time

class ButtonsManager:
    RED_PIN = 18  # 1
    RED_L0IGHT = 23
    BLUE_PIN = 12  # 2
    BLUE_LIGHT = 4
    GREEN_PIN = 6  # 3
    GREEN_LIGHT = 21
    ORANGE_PIN = 5  # 4
    ORANGE_LIGHT = 16
    TIRETTE_PIN = 26
    URGENCY_PIN = 20

    def begin(self):
        self.logger.sendLogStatus("Robot" ,"Start")
        Thread(target=self.team_stage, daemon=True).start()

        #self.red.set_function(
        #    Thread(target=self.team_stage, daemon=True).start)
        
        self.p.acquire()

    def team_stage(self):
        self.logger.sendLogStatus("Team" , "Choose")
        #ssd.set_message("set team")
        self.blue.set_function(
            Thread(target=self.set_team_blue, daemon=True).start)
        self.orange.set_function(
            Thread(target=self.set_team_yellow, daemon=True).start)

    def set_team_yellow(self):
        self.logger.sendLogStatus("Team" ,"Yellow")
        self.side = RobotBehavior.YELLOW_SIDE

        self.blue.set_function(None)
        self.orange.set_function(None)

        self.green.set_function(
            Thread(target=self.putrobot, daemon=True).start)

    def set_team_blue(self):
        self.logger.sendLogStatus("Team" , "Blue")
        self.side = RobotBehavior.BLUE_SIDE

        self.blue.set_function(None)
        self.orange.set_function(None)

        self.logger.sendLogStatus("Robot" ,"Put Robot & Green")

        self.green.set_function(
            Thread(target=self.putrobot, daemon=True).start)

    def putrobot(self):
        self.green.set_function(None)
        self.auto.set_side(self.side)
        self.auto.set_position()
        time.sleep(0.1)
        self.auto.positioning()
        self.ready_stage()

    def ready_stage(self):
        self.logger.sendLogStatus("Robot" ,"Robot Ready !")
        print("ready")
        self.tirette.set_function(
            Thread(target=self.run_match, daemon=True).start)
        #self.tirette.set_active_high(True)

    def run_match(self):
        self.logger.sendLogStatus("Robot" ,"Match !")
        print("MATCH")
        self.tirette.close()
        self.urgency.close()
        self.red.close()
        self.blue.close()
        self.orange.close()
        self.green.close()

        Thread(target=self.auto.start(), daemon=True).start()
        self.p.release()

    def __init__(self, auto):
        self.auto = auto
        self.side = None
        self.logger = Logger("Buttons")
        self.logger.init()

        self.logger.sendLog("INIT")
        self.red = LightButton(gpio_pins.INTER_1_PIN, gpio_pins.LED1_PIN)
        self.green = LightButton(gpio_pins.INTER_2_PIN, gpio_pins.LED2_PIN)
        self.blue = LightButton(gpio_pins.INTER_3_PIN, gpio_pins.LED3_PIN)
        self.orange = LightButton(gpio_pins.INTER_4_PIN, gpio_pins.LED4_PIN)
        self.tirette = Switch(gpio_pins.TIRETTE_PIN)
        self.red.on()
        self.green.on()
        self.blue.on()
        self.orange.on()
        self.logger.sendLog("ALLUME")
        #self.urgency = Switch(gpio_pins., print("tirette"))

        # Init Logger


        self.p = Semaphore(0)

