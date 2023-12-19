from multiprocessing import Process, Queue
import math
import time
import socket
from datetime import datetime
from utils.colors import colorise, Colors


class Teleplot:
    def __init__(self, IP):
        self.teleplotAddr = (IP, 47269)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def format_unit(self, unit, ):
        if (unit == None or unit == ""):
            return "" 
        return ("§" + unit)

    def sendTelemetry(self, name, value, unit, now):
        flags = ""
        if (type(value) is str):
            flags += "t"

        msg = name+":"+str(now)+":"+str(value)+self.format_unit(unit)+"|"+flags
        if (now == None):
            msg = name+":"+str(value)+self.format_unit(unit)+"|"+flags

        self.sock.sendto(msg.encode(), self.teleplotAddr)

    def sendTelemetryXY(self, name, x, y, x1, y1, unit):

        now = time.time() * 1000
        msg = name+":"+str(x)+":"+str(y)+":"+str(now)+";" +str(x1)+":"+str(y1)+":"+str(now)+self.format_unit(unit)+"|xy"
        
        self.sock.sendto(msg.encode(), self.teleplotAddr)

    def sendLog(self, mstr, now):
        timestamp = ""
        if (now != None):
            timestamp = str(now)

        msg = (">"+timestamp+":"+mstr)
        self.sock.sendto(msg.encode(), self.teleplotAddr)


class Logger:
    def __init__(self, IP="127.0.0.1"):
        self.teleplot = Teleplot(IP)

    def sendGraph(self, name, value, unit="", now=None):
        if(now==None): now=time.time()*1000
        self.teleplot.sendTelemetry(name, value, unit, now)

    def sendXY(self, name, x, y, x1, y1, unit=""):
        self.teleplot.sendTelemetryXY(self, name, x, y, x1, y1, unit)

    def sendLog(self, message, origin=None, now=None):
        if(now==None): now=time.time()+3600#Pour faire +1h
        time_hr = datetime.utcfromtimestamp(now).strftime("%H:%M:%S")

        if(now==None): origin_msg = ""
        else: origin_msg=" | " +colorise(origin, Colors.WHITE2, Colors.URL)


        final_message = colorise(time_hr, Colors.GREEN) + origin_msg + " | " + message
        self.teleplot.sendLog(final_message, now)
    
def f(q):
    q.put([42, None, 'hello'])
    print(q.get(timeout=100))
    print("ngmgr")

if __name__ == '__main__':
    logger = Logger()
    i=0
    while 1:
        now = time.time() * 1000
        logger.sendLog("Not connected", "sensors")
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