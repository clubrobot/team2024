#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections.abc import Callable, Iterable, Mapping
from typing import Any
from common.serialtalking import SerialTalking
from common.serialtypes import USHORT, UCHAR
import time

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

CHECK_ERROR_OPCODE = 0X18

GET_ALL_TOPIC_OPCODE = 0x01


class Sensors():
    TIMESTEP = 100
    MAX_DIST = 10000
    """     
    DEFAULT = {GET_SENSOR1_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR2_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR3_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR4_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR5_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR6_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR7_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR8_OPCODE: Deserializer(USHORT(MAX_DIST)), 
               CHECK_ERROR_OPCODE: Deserializer(USHORT(MAX_DIST)), 
              } """

    def __init__(self, uuid='SensorBoard'):
        self.sensors = SerialTalking("/dev/arduino/"+uuid)
        self.last_time = None

        try:
            if(self.execute(CHECK_ERROR_OPCODE).read(UCHAR)!=128): raise
            print("PASSE SENSORS")
        except:
            print("ERROR SENSORS")
            pass

        self.sensor1 = self.MAX_DIST
        self.sensor2 = self.MAX_DIST
        self.sensor3 = self.MAX_DIST
        self.sensor4 = self.MAX_DIST
        self.sensor5 = self.MAX_DIST
        self.sensor6 = self.MAX_DIST
        self.sensor7 = self.MAX_DIST
        self.sensor8 = self.MAX_DIST



    @TopicHandler(USHORT, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT)
    def get_all_sensors_handler(self, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8):
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.sensor3 = sensor3
        self.sensor4 = sensor4
        self.sensor5 = sensor5
        self.sensor6 = sensor6
        self.sensor7 = sensor7
        self.sensor8 = sensor8

    def get_all(self):
        return [self.sensor1, self.sensor2, self.sensor3, self.sensor4, self.sensor5, self.sensor6, self.sensor7, self.sensor8]

    def get_range_left_front(self):
        return self.sensor1

    def get_range_mid_left_front(self):
        return self.sensor2

    def get_range_mid_right_front(self):
        return self.sensor3

    def get_range_right_front(self):
        return self.sensor4

    def get_range_left_back(self):
        return self.sensor5

    def get_range_mid_left_back(self):
        return self.sensor6

    def get_range_mid_right_back(self):
        return self.sensor7

    def get_range_right_back(self):
        return self.sensor8

    def get_sensor1_range(self):
        return self.execute(GET_SENSOR1_OPCODE).read(USHORT)

    def get_sensor2_range(self):
        return self.execute(GET_SENSOR2_OPCODE).read(USHORT)

    def get_sensor3_range(self):
        return self.execute(GET_SENSOR3_OPCODE).read(USHORT)

    def get_sensor4_range(self):
        return self.execute(GET_SENSOR4_OPCODE).read(USHORT)

    def get_sensor5_range(self):
        return self.execute(GET_SENSOR5_OPCODE).read(USHORT)

    def get_sensor6_range(self):
        return self.execute(GET_SENSOR6_OPCODE).read(USHORT)

    def get_sensor7_range(self):
        return self.execute(GET_SENSOR7_OPCODE).read(USHORT)

    def get_sensor8_range(self):
        return self.execute(GET_SENSOR8_OPCODE).read(USHORT)

    def is_ready(self):
        try:
            return self.is_connected
        except:
            return False

    def check_errors(self):
        return self.execute(CHECK_ERROR_OPCODE).read(UCHAR)

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
    from setups.setup_serialtalks import *

    s = Sensors(manager, '/dev/ttyUSB0')
    print(s.get_sensor1_range())