#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.serialtalking import BYTE, LONG, FLOAT, USHORT, INT
from common.serialtalking import SerialTalking

import time

# Instructions
RESET_OPCODE                = 0X12
PING_AX_OPCODE              = 0X13

SET_ID_OPCODE               = 0X14
SET_BD_OPCODE               = 0X15

MOVE_OPCODE                 = 0X16
MOVE_SPEED_OPCODE           = 0X17
TURN_OPCODE                 = 0x18

SET_ENDLESS_MODE_OPCODE     = 0X19
SET_TEMP_LIMIT_OPCODE       = 0X1A
SET_ANGLE_LIMIT_OPCODE      = 0X1B
SET_VOLTAGE_LIMIT_OPCODE    = 0X1C
SET_MAX_TORQUE_OPCODE       = 0X1D

READ_POSITION_OPCODE        = 0X1E
READ_SPEED_OPCODE           = 0X1F
READ_TORQUE_OPCODE          = 0X2A

SET_ANGLE_SERVO_OPCODE      = 0x2B

"""
This class acts as an interface between the raspeberry pi and the arduino.
It contains methods relating to each action of the actuator.
It allows the raspeberry pi to ask the arduino to perform an action via a specific OPCODE.
"""
class Actionneur():
    
    def __init__(self, uuid='actionneurs'):
        self.actio = SerialTalking(uuid)#"/dev/arduino/"
    
    def SetServoAngle(self, angle, id): self.actio.order(SET_ANGLE_SERVO_OPCODE, USHORT(angle), USHORT(id))

class AX12():
        def __init__(self, id, parent):
            self.parent = parent
            self.id = id

            self.setEndlessMode(False)
            self.setAngleLimit(0,300)
        
        def reset(self): self.parent.actio.order(RESET_OPCODE, BYTE(self.id))

        def ping(self):
            output = self.parent.actio.request(PING_AX_OPCODE, BYTE, send_args=[BYTE(self.id)])
            return bool(output[0])

        def setID(self, newID): self.parent.actio.order(SET_ID_OPCODE, BYTE(self.id), BYTE(newID))

        def setBD(self, newBD): self.parent.actio.order(SET_BD_OPCODE, BYTE(self.id), INT(newBD))

        def move(self, Pos): self.parent.actio.order(MOVE_OPCODE, BYTE(self.id), FLOAT(Pos))

        def turn(self, Speed): self.parent.actio.order(TURN_OPCODE, BYTE(self.id), FLOAT(Speed))

        def stop_turn(self): self.turn(0)
        
        def moveSpeed(self, Pos, Speed): self.parent.actio.order(MOVE_SPEED_OPCODE, BYTE(self.id), FLOAT(Pos), FLOAT(Speed))

        def setEndlessMode(self, Status): self.parent.actio.order(SET_ENDLESS_MODE_OPCODE, BYTE(self.id), BYTE(Status))

        def setTempLimit(self, Temp): self.parent.actio.order(SET_TEMP_LIMIT_OPCODE, BYTE(self.id), BYTE(Temp))

        def setAngleLimit(self, CWLimit, CCWLimit): self.parent.actio.order(SET_ANGLE_LIMIT_OPCODE, BYTE(self.id), FLOAT(CWLimit), FLOAT(CCWLimit))

        def setVoltageLimit(self, DVoltage, UVoltage): self.parent.actio.order(SET_VOLTAGE_LIMIT_OPCODE, BYTE(self.id), BYTE(DVoltage), BYTE(UVoltage))

        def setMaxTorque(self, MaxTorque): self.parent.actio.order(SET_MAX_TORQUE_OPCODE, BYTE(self.id), INT(MaxTorque))

        def readPosition(self):
            output = self.parent.actio.request(READ_POSITION_OPCODE, FLOAT, send_args=[BYTE(self.id)])
            return output[0]
        
        def readSpeed(self):
            output = self.parent.actio.request(READ_SPEED_OPCODE, FLOAT, send_args=[BYTE(self.id)])
            return output[0]

        def readTorque(self):
            output = self.parent.actio.request(READ_TORQUE_OPCODE, INT, BYTE(self.id))
            return output[0]

        #Move till' the angle is reached
        def move_reached(self, angle):
             #TODO: very sad code; too bad

            self.move(angle)
            self.readPosition()#On "ammorce" l'AX12 car la première valeur est 0° même si à x°
            while angle-1>=self.readPosition()>=angle+1:
                pass
        
            return

if __name__ == "__main__":
    from setups.setup_serialtalks import *

    s = Actionneur(manager)
    s.connect()

    ax = s.AX12(1, s)
    ax2 = s.AX12(3, s)
    
    ax2.move(100)
    ax.move(100)