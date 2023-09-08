#from setups.setup_display import *
from behaviours.robot_behaviour import RobotBehavior
#from common.components import LightButtonProxy, SwitchProxy
from threading import Semaphore
from common.gpiodevices import Switch, LightButton, gpio_pins
from logs.log_manager import *
from threading import Thread

class ButtonsManager:
    RED_PIN = 18  # 1
    RED_LIGHT = 23
    BLUE_PIN = 12  # 2
    BLUE_LIGHT = 4
    GREEN_PIN = 6  # 3
    GREEN_LIGHT = 21
    ORANGE_PIN = 5  # 4
    ORANGE_LIGHT = 16
    TIRETTE_PIN = 26
    URGENCY_PIN = 20

    def begin(self):
        self.logger(INFO, "Start")
        Thread(target=self.team_stage, daemon=True).start()
        self.red.set_function(
            Thread(target=self.team_stage, daemon=True).start)
        self.p.acquire()

    def team_stage(self):
        self.logger(INFO, "Team Stage")
        #ssd.set_message("set team")
        self.blue.set_function(
            Thread(target=self.set_team_blue, daemon=True).start)
        self.orange.set_function(
            Thread(target=self.set_team_yellow, daemon=True).start)

    def set_team_yellow(self):
        self.logger(INFO, "Yellow Team")
        self.side = RobotBehavior.YELLOW_SIDE
        #ssd.set_message("team : y")
        self.green.set_function(
            Thread(target=self.odometry_stage, daemon=True).start)

    def set_team_blue(self):
        self.logger(INFO, "Blue Team")
        self.side = RobotBehavior.BLUE_SIDE
        #ssd.set_message("team : b")
        self.green.set_function(
            Thread(target=self.odometry_stage, daemon=True).start)

    def odometry_stage(self):
        self.logger(INFO, "Team Validation")
        self.logger(INFO, "Odometry Stage")
        self.auto.set_side(self.side)
        #ssd.set_message("set pos")
        self.blue.set_function(None)
        self.orange.set_function(None)
        self.green.set_function(
            Thread(target=self.tirette_stage, daemon=True).start)

    def tirette_stage(self):
        self.logger(INFO, "Odometry Validation")
        self.auto.set_position()

        self.logger(INFO, "Tirret Stage")
        #ssd.set_message("tirret")
        self.tirette.set_function(
            Thread(target=self.urgency_stage, daemon=True).start)
        self.green.set_function(None)

    def urgency_stage(self):
        self.logger(INFO, "Tirret Validation")
        self.logger(INFO, "Urgency Button Stage")
        #ssd.set_message("urgency")
        self.urgency.set_function(
            Thread(target=self.positioning_stage, daemon=True).start)

    def positioning_stage(self):
        self.logger(INFO, "Urgency Button Validation")
        self.logger(INFO, "Robot Positionning")
        self.auto.positioning()
        self.ready_stage()

    def ready_stage(self):
        self.logger(INFO, "Robot Ready !")
        print("ready")
        self.tirette.set_function(
            Thread(target=self.run_match, daemon=True).start)
        self.tirette.set_active_high(True)

    def run_match(self):
        #self.logger(INFO, "MATCH LAUNCHED !!!")
        self.tirette.close();print("MATCH")
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

        #self.red = LightButton(gpio_pins.INTER_1_PIN, gpio_pins.LED1_PIN, print("BTN1"))
        #self.green = LightButton(gpio_pins.INTER_2_PIN, gpio_pins.LED2_PIN, print("BTN1"));
        #self.blue = LightButton(gpio_pins.INTER_3_PIN, gpio_pins.LED3_PIN, print("BTN1"));
        #self.orange = LightButton(gpio_pins.INTER_4_PIN, gpio_pins.LED4_PIN, print("BTN1"));
        print("INIT")
        self.red = LightButton(gpio_pins.INTER_1_PIN, gpio_pins.LED1_PIN, print("BTN1"))
        self.green = LightButton(gpio_pins.INTER_2_PIN, gpio_pins.LED2_PIN, print("BTN2"))
        self.blue = LightButton(gpio_pins.INTER_3_PIN, gpio_pins.LED3_PIN, print("BTN3"))
        self.orange = LightButton(gpio_pins.INTER_4_PIN, gpio_pins.LED4_PIN, print("BTN4"))
        self.tirette = Switch(gpio_pins.TIRETTE_PIN, print("tirette"))
        self.red.on()
        self.green.on()
        self.blue.on()
        self.orange.on()
        print("ALLUME")
        #self.urgency = Switch(gpio_pins., print("tirette"))

        # Init Logger
        self.logger = LogManager().getlogger(self.__class__.__name__, Logger.SHOW, INFO)

        self.p = Semaphore(0)

        # Init Logger
        self.logger = LogManager().getlogger(self.__class__.__name__, Logger.SHOW, INFO)

        self.p = Semaphore(0)
