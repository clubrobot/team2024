# import imp
from managers.simple_wifi import WiFiManager
import time

def square(args):
    return args[0] ** 2


def printing(args):
    print(args)


communication = WiFiManager("10.0.0.11", 25565,"client")
communication.start()
print("printing",communication.send([4,"Coucou test"]))
t=time.time()
for i in range(100):
    print("square:",communication.send_return([3,i]))
print(time.time()-t)
communication.send([0x00])