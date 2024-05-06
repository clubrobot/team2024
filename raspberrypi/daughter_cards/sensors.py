#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import sys
from common.serialtalking import SerialTalking
from common.serialtypes import USHORT, UCHAR
import time
from logs.logger import Logger, colorise, Colors

UNUSED_SENSOR = 65535

# Instructions
GET_SENSOR1_OPCODE = 0x10
GET_SENSOR2_OPCODE = 0x11
GET_SENSOR3_OPCODE = 0x12
GET_SENSOR4_OPCODE = 0x13
GET_SENSOR5_OPCODE = 0x14
GET_SENSOR6_OPCODE = 0x15
GET_SENSOR7_OPCODE = 0x16
GET_SENSOR8_OPCODE = 0x17
GET_ALL_SENSORS_OPCODE = 0x19

CHECK_ERROR_OPCODE = 0X18

GET_ALL_TOPIC_OPCODE = 0x01

def pol2cart(phi, rho):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

class Sensors():
    MAX_DIST = 10000

    def __init__(self, uuid='sensors'):
        if 'linux' in sys.platform:
            self.sensors = SerialTalking("/dev/arduino/"+uuid)
        else:
            self.sensors = SerialTalking(uuid)

        self.log = Logger("sensors")
        self.log.init()
        self.log.sendLogStatus("sensors" ,colorise("WAIT SENSORS", Colors.YELLOW))
        
        try:
            if(self.check_errors()!=128): raise
            self.log.sendLog("PASSE SENSORS")
        except:
            self.log.sendLog("ERROR SENSORS")
            pass

        self.sensor1 = self.MAX_DIST
        self.sensor2 = self.MAX_DIST
        self.sensor3 = self.MAX_DIST
        self.sensor4 = self.MAX_DIST
        self.sensor5 = self.MAX_DIST
        self.sensor6 = self.MAX_DIST
        self.sensor7 = self.MAX_DIST
        self.sensor8 = self.MAX_DIST

    def get_all_sensors(self):
        [self.sensor1, self.sensor2, self.sensor3, self.sensor4, self.sensor5, self.sensor6, self.sensor7, self.sensor8] = self.sensors.request(GET_ALL_SENSORS_OPCODE, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT)

        return [self.sensor1, self.sensor2, self.sensor3, self.sensor4, self.sensor5, self.sensor6, self.sensor7, self.sensor8]

    def get_sensor1_range(self):
        self.sensor1 = self.sensors.request(GET_SENSOR1_OPCODE, USHORT)[0]
        return self.sensor1

    def get_sensor2_range(self):
        self.sensor2 = self.sensors.request(GET_SENSOR2_OPCODE, USHORT)[0]
        return self.sensor2

    def get_sensor3_range(self):
        self.sensor3 = self.sensors.request(GET_SENSOR3_OPCODE, USHORT)[0]
        return self.sensor3

    def get_sensor4_range(self):
        self.sensor4 = self.sensors.request(GET_SENSOR4_OPCODE, USHORT)[0]
        return self.sensor4

    def get_sensor5_range(self):
        self.sensor5 = self.sensors.request(GET_SENSOR5_OPCODE, USHORT)[0]
        return self.sensor5

    def get_sensor6_range(self):
        self.sensor6 = self.sensors.request(GET_SENSOR6_OPCODE, USHORT)[0]
        return self.sensor6

    def get_sensor7_range(self):
        self.sensor7 = self.sensors.request(GET_SENSOR7_OPCODE, USHORT)[0]
        return self.sensor7

    def get_sensor8_range(self):
        self.senor8 = self.sensors.request(GET_SENSOR8_OPCODE, USHORT)[0]
        return self.sensor8

    def is_ready(self):
        try:
            return self.is_connected
        except:
            return False
    
    def publish_logs(self):
        try:
            if(self.check_errors()!=128): raise
            self.log.sendLogStatus("sensors" ,colorise("PASSE SENSORS", Colors.GREEN))
        except:
            self.log.sendLogStatus("sensors" ,colorise("ERROR SENSORS", Colors.RED))
            pass
        
        return
        self.get_all_sensors()
        co_sen1 = pol2cart(0, np.log(self.sensor1))
        co_sen2 = pol2cart(np.pi/4, np.log(self.sensor2))
        co_sen3 = pol2cart(np.pi/2, np.log(self.sensor3))
        co_sen4 = pol2cart(3*np.pi/4, np.log(self.sensor4))
        co_sen5 = pol2cart(np.pi, np.log(self.sensor5))
        co_sen6 = pol2cart(5*np.pi/4, np.log(self.sensor6))
        co_sen7 = pol2cart(3*np.pi/2, np.log(self.sensor7))
        co_sen8 = pol2cart(7*np.pi/4, np.log(self.sensor8))

        border_1 = (np.log(self.MAX_DIST),np.log(self.MAX_DIST))
        border_2 = (-np.log(self.MAX_DIST),np.log(self.MAX_DIST))
        border_3 = (np.log(self.MAX_DIST),-np.log(self.MAX_DIST))
        border_4 = (-np.log(self.MAX_DIST),-np.log(self.MAX_DIST))

        self.log.sendXY("Sensors", "cm", True, None,
                        co_sen1[0], co_sen1[1],
                        co_sen2[0], co_sen2[1],
                        co_sen3[0], co_sen3[1],
                        co_sen4[0], co_sen4[1],
                        co_sen5[0], co_sen5[1],
                        co_sen6[0], co_sen6[1],
                        co_sen7[0], co_sen7[1],
                        co_sen8[0], co_sen8[1],
                        border_1[0], border_1[1],
                        border_2[0], border_2[1],
                        border_3[0], border_3[1],
                        border_4[0], border_4[1]
                        )

    def check_errors(self):
        return self.sensors.request(CHECK_ERROR_OPCODE, UCHAR)[0]

import threading
class ThreadSensors():
    def __init__(self, sensors,robot):
        self.sensors=sensors
        self.robot=robot
        self.thread=threading.Thread(target=self.loop)
        print("debut2")
        self.thread.start()
    
    def loop(self):
        self.looping=True
        
        while(self.looping):
            self.sensors.sensor1=self.sensors.get_sensor1_range()
            #print(self.sensors.sensor1)
            self.sensors.sensor2=self.sensors.get_sensor2_range()
            self.sensors.sensor3=self.sensors.get_sensor3_range()
            self.sensors.sensor4=self.sensors.get_sensor4_range()
            self.sensors.sensor5=self.sensors.get_sensor5_range()
            self.sensors.sensor6=self.sensors.get_sensor6_range()
            self.sensors.sensor7=self.sensors.get_sensor7_range()
            self.sensors.sensor8=self.sensors.get_sensor8_range()
            


if __name__ == "__main__":

    s = Sensors("COM8")
    time.sleep(1)
    print(s.check_errors())
    print(s.sensors.getuuid())
    while 1:
        print(s.get_all_sensors())