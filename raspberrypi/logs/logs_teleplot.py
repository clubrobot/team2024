from multiprocessing import Process, Queue
import math
import time
import socket
from utils.colors import colorise, Colors


class Teleplot:
    def __init__(self):
        self.teleplotAddr = ("127.0.0.1",47269)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        def format_unit(self, unit):
            if (unit == None or unit == ""):
                return "" 
            return ("§" + unit)

        def sendTelemetry(self, name, value, unit, now):
            flags = ""
            if (type(value) is str):
                flags += "t"

            msg = name+":"+str(now)+":"+str(value)+format_unit(unit)+"|"+flags
            if (now == None):
                msg = name+":"+str(value)+format_unit(unit)+"|"+flags

            self.sock.sendto(msg.encode(), self.teleplotAddr)

        def sendTelemetryXY(self, name, x, y, x1, y1, unit):

            now = time.time() * 1000
            msg = name+":"+str(x)+":"+str(y)+":"+str(now)+";" +str(x1)+":"+str(y1)+":"+str(now)+format_unit(unit)+"|xy"
            
            self.sock.sendto(msg.encode(), self.teleplotAddr)

        def sendLog(self, mstr, now):
            timestamp = ""
            if (now != None):
                timestamp = str(now)

            msg = (">"+timestamp+":"+mstr)
            self.sock.sendto(msg.encode(), self.teleplotAddr)

def f(q):
    q.put([42, None, 'hello'])
    print(q.get(timeout=100))
    print("ngmgr")

if __name__ == '__main__':
    i=0
    while 1:
        now = time.time() * 1000
        sendLog(colorise("Test", Colors.RED, Colors.URL), now=now)
        i+=0.1
        time.sleep(0.1)
		
        
    """
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    q.put([42, None, 'test'])
    p.join()
    """