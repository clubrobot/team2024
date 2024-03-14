import time
from common.serialtalking import BYTE, LONG, FLOAT, INT
from common.serialtalking import SerialTalking
import setups.setup_logger

talking = SerialTalking("wheeledbase")

talking.ping()

print(talking.getuuid()) 