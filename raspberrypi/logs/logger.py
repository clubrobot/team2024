"""!
@file logger.py

@brief Prends en charge le log via la classe Logger
@author Boris HILKENS
"""

#Imports
from datetime import datetime
import time
import os

from logs.utils.colors import colorise, Colors
from logs.logs_teleplot import Teleplot


class Logger:
    """! La classe Logger, responsable de tout le log
    
    """
    ##Objet de Teleplot @see logs_teleplot.py
    teleplot = None
    ##Objet de classe Archiver @see log_archiver
    archiver = None
    
    ##Boolean pour savoir si les logs sont écrit dans un .txt
    saveToFile = False
    ##Boolean pour afficher (ou non) les logs dans la console d'exec
    verbose = False

    ##Boolean pour savoir si Teleplot a été init
    initied = False

    ##Constructeur, ne sert qu'à enregistrer l'origine
    def __init__(self, origin):
        self.origin = origin

    @staticmethod
    def init(IP="127.0.0.1", verbose=True, saveToFile=False):
        """! Méthode statique pour initialiser téleplot

        @param IP Ip du serveur teleplot
        @param verbose Boolean pour afficher (ou non) les logs dans la console d'exec
        @param saveToFile Boolean pour savoir si les logs sont écrit dans un .txt
        """
        if Logger.initied==True: return
        Logger.teleplot = Teleplot(IP)

        Logger.saveToFile = saveToFile
        Logger.verbose = verbose

        if(Logger.saveToFile): Logger.archiver = log_archiver()

        Logger.initied = True

    @staticmethod
    def sendGraph(name, value, unit="", now=None):
        """! Envoie une donnée sur un graph
        @param name Nom du graphique
        @param value valeur à plotter
        @param unit unité de la valeur
        @param now temps de l'execution, default: None
        """
        if(not Logger.initied): return #Logger not initied

        if(now==None): now=(time.time()+3600)*1000
        Logger.teleplot.sendTelemetry(name, value, unit, now)

    @staticmethod
    def sendXY(name, unit="", clr=False, now=None, *args):
        """! Envoie une donnée XY à Teleplot
        @param name nom du graphique
        @param x Valeur x
        @param y Valeur y
        @param unit unité des valeurs
        @param x1 Valeur x de la deuxième serie
        @param y1 Valeur y de la deuxième serie
        """
        if(not Logger.initied): return #Logger not initied
        if(len(args)%2!=0): return #Can't do xy if not even

        Logger.teleplot.sendTelemetryXY(name, unit, clr, now, *args)

    @staticmethod
    def sendLogStatic(message, origin="", now=None):
        """! Envoie un message
        @param message message à transmettre
        @param origin origine du message
        @param now temps de l'execution, default: None
        """
        if(not Logger.initied): return #Logger not initied

        if(now==None): now=time.time()+3600#Pour faire +1h
        time_hr = datetime.utcfromtimestamp(now).strftime("%H:%M:%S")

        if(origin==""): origin_msg = ""
        else: origin_msg=" | " +colorise(origin, Colors.WHITE2, Colors.URL)

        final_message = colorise(time_hr, Colors.GREEN) + origin_msg + " | " + message

        if(Logger.saveToFile): Logger.archiver.save_log(time_hr + " | " + origin + " | " + message + "\n")
        if(Logger.verbose): print(final_message)

        Logger.teleplot.sendLog(final_message, now*1000)

    def sendLog(self, message, now=None):
        """! Envoie un message avec l'origine de la classe
        @param message message à transmettre
        @param now temps de l'execution, default: None
        """
        Logger.sendLogStatic(message, self.origin, now)

class log_archiver:
    """! La classe log_archiver, responsable de toute la sauvegarde du log
    
    """
    def __init__(self):
        """! Initie la classe en créant le ficier txt"""
        self.create_log()

    def create_log(self):
        """! Crée le fichier txt"""
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
        """! Ajoute le message au fichier"""
        if(message):
            self.log_file.write(message)

if __name__ == '__main__':
    import math

    myLogger = Logger("sensors")
    myLogger.init("127.0.0.1", verbose=True, saveToFile=True)
    i=0
    
    while 1:
        myLogger.sendLog("Not connected")
        Logger.sendLogStatic("test")
        Logger.sendGraph("Test", math.sin(i), "km²")
        Logger.sendXY("XY", "km²", True ,None,math.cos(i), math.sin(i), math.cos(i)*2, math.sin(i)*0.5)
        i+=0.1
        time.sleep(0.1)
	
        
    

