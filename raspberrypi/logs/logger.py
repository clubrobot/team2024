from datetime import datetime
import time
import os

from utils.colors import colorise, Colors
from logs_teleplot import Teleplot

class Logger:
    teleplot = None
    archiver = None
    
    saveToFile = False
    verbose = False

    initied = False

    @staticmethod
    def init(IP="127.0.0.1", verbose=False, saveToFile=False):
        Logger.teleplot = Teleplot(IP)

        Logger.saveToFile = saveToFile
        Logger.verbose = verbose

        if(Logger.saveToFile): Logger.archiver = log_archiver()

        Logger.initied = True

    @staticmethod
    def sendGraph(name, value, unit="", now=None):
        if(not Logger.initied): return #Logger not initied

        if(now==None): now=(time.time()+3600)*1000
        Logger.teleplot.sendTelemetry(name, value, unit, now)

    @staticmethod
    def sendXY( name, x, y, unit="", x1=None, y1=None):
        if(not Logger.initied): return #Logger not initied

        Logger.teleplot.sendTelemetryXY(name, x, y, x1, y1, unit)

    @staticmethod
    def sendLog( message, origin="", now=None):
        if(not Logger.initied): return #Logger not initied

        if(now==None): now=time.time()+3600#Pour faire +1h
        time_hr = datetime.utcfromtimestamp(now).strftime("%H:%M:%S")

        if(now==None): origin_msg = ""
        else: origin_msg=" | " +colorise(origin, Colors.WHITE2, Colors.URL)

        final_message = colorise(time_hr, Colors.GREEN) + origin_msg + " | " + message

        if(Logger.saveToFile): Logger.archiver.save_log(time_hr + " | " + origin + " | " + message + "\n")
        if(Logger.verbose): print(final_message)

        Logger.teleplot.sendLog(final_message, now*1000)

class log_archiver:
    def __init__(self):
        self.create_log()

    def create_log(self):
        i=0
        f=None
        path = os.path.dirname(os.path.abspath(__file__)) + "/dump/log_{}.txt"
        while True:
            try:
                f=open(path.format(i), "x")
                f.close()
                self.log_file = open(path.format(i), "w")
                break
            except FileExistsError:
                i=i+1
            except:
                f.close()
                break

    def save_log(self, message):
        if(message):
            self.log_file.write(message)


if __name__ == '__main__':
    import math

    Logger.init("127.0.0.1", verbose=True, saveToFile=True)
    i=0
    
    while 1:
        Logger.sendLog("Not connected", "sensors")
        Logger.sendGraph("Test", math.sin(i), "km²")
        Logger.sendXY("XY", math.cos(i), math.sin(i), "km²")
        i+=0.1
        time.sleep(0.1)
	
        
    

