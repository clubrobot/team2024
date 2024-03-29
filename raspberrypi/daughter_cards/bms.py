#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
# sys.path.append("../common/")

from common.serialutils import Deserializer
from common.serialtalks import BYTE, INT, LONG, FLOAT, SerialTalks
from daughter_cards.arduino import SecureArduino

GET_RSOC_OPCODE = 0x04
GET_ASOC_OPCODE = 0x05
GET_VOLTAGE_OPCODE = 0x06
GET_CYCLE_COUNT_OPCODE = 0x07
GET_CURRENT_OPCODE = 0x08
GET_AVERAGE_CURRENT_OPCODE = 0x09
GET_REMAINING_CAP_OPCODE = 0x0A
GET_AVERAGE_TIME_EMPTY_OPCODE = 0x0B
GET_AVERAGE_TIME_FULL_OPCODE = 0x0C

"""
This class acts as an interface between the raspeberry pi and the arduino.
It contains methods for each action of the Battery Management System. 
It allows the raspeberry pi to ask the arduino to perform an action via a specific OPCODE.
"""
class BMS(SecureArduino):
    _DEFAULT = {GET_RSOC_OPCODE: Deserializer(INT(100))}

    def __init__(self, uuid='/tmp/arduino/BMS'):
        SecureArduino.__init__(self, parent, "/dev/arduino/"+uuid, BMS._DEFAULT)

    def get_relative_soc(self):
        output = self.execute(GET_RSOC_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_absolute_soc(self):
        output = self.execute(GET_ASOC_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_voltage(self):
        output = self.execute(GET_VOLTAGE_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_cycle_count(self):
        output = self.execute(GET_CYCLE_COUNT_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_current(self):
        output = self.execute(GET_CURRENT_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_average_current(self):
        output = self.execute(GET_AVERAGE_CURRENT_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_remaining_capacity(self):
        output = self.execute(GET_REMAINING_CAP_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_average_time_to_empty(self):
        output = self.execute(GET_AVERAGE_TIME_EMPTY_OPCODE)
        rsoc = output.read(INT)
        return rsoc

    def get_average_time_to_full(self):
        output = self.execute(GET_AVERAGE_TIME_FULL_OPCODE)
        rsoc = output.read(INT)
        return rsoc
