import time
from common.serialtalking import BYTE, LONG, FLOAT, INT
from common.serialtalking import SerialTalking

talking = SerialTalking("COM4")

talking.ping()

print(talking.get_logs()) 