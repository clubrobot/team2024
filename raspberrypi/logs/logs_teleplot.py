import time
import socket


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

        now = (time.time()+3600)*1000
        if(x1==None):
            msg = name+":"+str(x)+":"+str(y)+":"+str(now)+self.format_unit(unit)+"|xy"
        else:
            msg = name+":"+str(x)+":"+str(y)+":"+str(now)+";" +str(x1)+":"+str(y1)+":"+str(now)+self.format_unit(unit)+"|xy"
        
        self.sock.sendto(msg.encode(), self.teleplotAddr)

    def sendLog(self, mstr, now):
        timestamp = ""
        if (now != None):
            timestamp = str(now)

        msg = (">"+timestamp+":"+mstr)
        self.sock.sendto(msg.encode(), self.teleplotAddr)


