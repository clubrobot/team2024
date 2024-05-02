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

    def sendTelemetryXY(self, name, unit, clr, now, *args):
        if now==None: now = (time.time()+3600)*1000

        msg = name+":"
        for i in range(0, len(args)-1, 2):
           msg +=str(args[i])+":"+str(args[i+1])+":"+str(now)+";"
        
        msg = msg[:-1]
        msg += self.format_unit(unit)
        if clr: msg+="|clr" 
        else: msg+="|xy"
        self.sock.sendto(msg.encode(), self.teleplotAddr)

    def sendLog(self, mstr, now):
        timestamp = ""
        if (now != None):
            timestamp = str(now)

        msg = (">"+timestamp+":"+mstr)
        self.sock.sendto(msg.encode(), self.teleplotAddr)

