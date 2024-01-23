'''!
@file SerialTalkingExample.py
@brief ptit tuto comment l'utiliser
@example SerialTalkingExample.py
'''

from common.serialtalking import BYTE, LONG, FLOAT, USHORT, INT
from common.serialtalking import SerialTalking

import time

# Instructions
RESET_OPCODE                = 0X12
PING_AX_OPCODE              = 0X13

MOVE_OPCODE                 = 0X16
MOVE_SPEED_OPCODE           = 0X17

READ_POSITION_OPCODE        = 0X1E
READ_TORQUE_OPCODE          = 0X2A

class Example():
    def __init__(self, uuid='actionneurs'):
        self.actio = SerialTalking(uuid)
        
    def reset(self): self.actio.order(RESET_OPCODE, BYTE(self.id))

    def ping(self):
        output = self.actio.request(PING_AX_OPCODE, BYTE, send_args=[BYTE(self.id)])[0]
        return not bool(output)

    def move(self, Pos): self.actio.order(MOVE_OPCODE, BYTE(self.id), FLOAT(Pos))
    
    def moveSpeed(self, Pos, Speed): self.actio.order(MOVE_SPEED_OPCODE, BYTE(self.id), FLOAT(Pos), FLOAT(Speed))

    def readPosition(self):
        output = self.actio.request(READ_POSITION_OPCODE, FLOAT, send_args=[BYTE(self.id)])[0]
        return output

    def readTorque(self):
        output = self.actio.request(READ_TORQUE_OPCODE, INT, BYTE(self.id))[0]
        return output