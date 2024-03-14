'''
 @file serialtalking.py
 @brief SerialTalking Lib Work In progess: CRINSA 2024

 @author Negrache Gibril et Hilkens Boris
'''

import math
import time
import sys
from common.serialtypes import *
import common.pySerialTransfer as txfer

from logs.logger import Logger
from logs.utils.colors import colorise, Colors

BAUDRATE = 115200

#Défini les opcodes par défault
PING_OPCODE = 0x00
GETUUID_OPCODE = 0x01
SETUUID_OPCODE = 0x02
DISCONNECT_OPCODE = 0x03
GETEEPROM_OPCODE = 0x04
SETEEPROM_OPCODE = 0x05
CLEAREEPROM_OPCODE = 0x07

#Magics numbers
SERIALTALKING_SINGLE_MAGIC = 's' #comme single
SERIALTALKING_MULTIPLE_MAGIC = 'm' #comme multiple

# Exceptions

class AlreadyConnectedError(ConnectionError): pass

class ConnectionFailedError(ConnectionError): 
    pass
        

class NotConnectedError(ConnectionError): pass

class MuteError(TimeoutError): pass

class SerialTalksWarning(UserWarning, ConnectionError): pass

#TODO: Les erreurs (avec logs)
#TODO: Faire un thread qui check périodiquement si l'arduino est alive (avec ping) lors qu'il ne communique pas
#TODO: Faire un meilleur log avec teleplot (à la fin)
#TODO: Expliqer ASS (Asymetrical Serial Shit); mon protocol de tranfert mdr
#TODO: clean up & intégrer les fonctions de base
#TODO: Timeout & connections checks 

class SerialTalking:
    '''! Serial Talking (python)
    
    @brief Comme SerialTalks mais autre; middleware entre pyserialTransfert et l'user
    '''
    def __init__(self, port, timeout=10): 
        '''!Initie une instance de SerialTalking avec un arduino

        @param port port de l'arduino
        @param timeout temps max de connection (default à 5sec)
        '''
        self.port = port
        self.is_connected=False

        self.recSize = 0
        self.sendSize = 0

        self.logger = Logger("SerialTalking")

        self.connect(timeout)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self):
        self.disconnect()

    def connect(self, timeout=5):
        '''! Connecte à un arduino

        @param timeout timeout de bas à 5 sec
        '''
        if self.is_connected:
            self.logger.sendLog(colorise('{} is already connected'.format(self.port), Colors.RED))
            raise AlreadyConnectedError('{} is already connected'.format(self.port))

        # Connect to the serial port
        self.link = txfer.SerialTransfer(self.port, BAUDRATE)
        if(self.link.open()==False):
            raise ConnectionFailedError
        
        startingtime = time.monotonic()
        while not self.is_connected:
            try:
                shouldBePong = self.request(PING_OPCODE, STRING)[0]
                if(shouldBePong=="pong\x00"):
                    self.is_connected = True
                    self.logger.sendLog(colorise('\'{}\' is successfully connected!'.format(self.port), Colors.GREEN))
                time.sleep(0.1)
                if(time.monotonic() - startingtime > timeout): raise TimeoutError
            except TimeoutError:
                if time.monotonic() - startingtime > timeout:
                    self.disconnect()

                    raise MuteError(
                        colorise('\'{}\' is mute. It may not be an Arduino or it\'s sketch may not be correctly loaded.'.format(
                            self.port), Colors.RED, Colors.BOLD)) from None
                else:
                    continue

            except NotConnectedError:
                self.is_connected = False

    def disconnect(self):
        '''! Se deconnecte de l'arduino
        '''
        self.logger.sendLog(colorise('\'{}\' is getting disconnected!'.format(self.port), Colors.YELLOW))
        self.link.close()
        self.is_connected=False
        return
    
    def available(self):
        '''! écoute la ligne rx et décode le message entrant
        @return self.link.available()
        '''
        return self.link.available()
    
    def get_status_code(self):
        '''! Retourne le code de status de pySerialTransfert
        @return self.link.status
        '''
        return self.link.status

    def ping(self):
        '''! Ping l'arduino
        @return vrai si pingé, faux sinon
        '''
        shouldBePong = self.request(PING_OPCODE, STRING)[0]
        if(shouldBePong=="pong\x00"):
            return True
        else:
            return False

    def getuuid(self):
        '''! Retourne l'uuid de l'arduino
        @return uuid
        '''
        return self.request(GETUUID_OPCODE, STRING)[0]

    def setuuid(self, uuid):
        '''! Paramètre l'uuid
        @param uuid l'uuid à changer
        '''
        if uuid[-1]!='\x00': uuid=uuid+'\x00'
        self.order(SETUUID_OPCODE, STRING(uuid))
        return
    
    def clearEEPROM(self):
        '''! 
        @param 
        '''
        self.order(CLEAREEPROM_OPCODE)
        return
    
    def getEEPROM(self, address):
        '''! Renvoie une valeur de l'eeprom 
        @param address adresse de la valeur
        @return valeur à l'adresse
        '''
        return self.request(GETEEPROM_OPCODE, BYTE, send_args=[USHORT(address)])[0]
    
    def setEEPROM(self, address, value):
        '''! Change une valeur de l'eeprom
        @param address adresse de la valeur à changer
        @param value la valeur à changer
        '''
        self.order(SETEEPROM_OPCODE, USHORT(address), BYTE(value))
        return

    #For each arg, on tx l'arg puis on envoie tout
    def order(self, opcode, *args):
        '''! Envoie un ordre à l'arduino
        @param opcode Code de l'opération
        @param *args arguments d'envoi 
        '''
        if(len(args)==0): args = [BYTE(0x01)] #Si pas d'args
        #Oui le string fait chier
        for arg in args:
            if(arg["format"]=="str"):
                self.write_buffer(arg, len(arg["value"]))
            else:
                self.write_buffer(arg)

        self.send_buffer(opcode)
        return

    #call order puis fait le tralala du request
    def request(self, opcode, *args, send_args=None, timeout=5):
        '''! Requête à l'arduino
        @param opcode Code de l'opération
        @param *args type des éléments reçu 
        @param send_args liste des paramètre qui vont avec l'envoi
        @param timeout 5sec
        
        @return Renvoie une liste data des données reçue
        '''
        data, data_size = ([], []) #Notre array
        if(send_args==None):
            self.order(opcode)# On envoit l'ordre pour avoir la réponse
        else:
            self.order(opcode, *send_args)

        time.sleep(0.005)
        startingtime = time.monotonic()
        #Boucle while avec timeout
        while True:
            try:
                if(self.available()):#Tant que pas de réponse
                    for arg in args:#On cycle dans tout les valeurs excepté
                        datum, datum_size = self.read_buffer(arg) #On lit le buffer
                        data.append(datum)
                        data_size.append(datum_size)
                    if(len(data)==len(args)): break#Break from the loop if every args are there
                else:#si on a pas de réponse, on la force mdr
                    if(send_args==None):
                        self.order(opcode)# On envoit l'ordre pour avoir la réponse
                    else:
                        self.order(opcode, *send_args)
                    time.sleep(0.1)
                if(time.monotonic() - startingtime > timeout): raise TimeoutError
            except Exception as e:
                self.logger.sendLog(colorise('\'{}\' Got a little hiccup, gonna resend the command.'.format(
                            self.port), Colors.RED, Colors.BOLD))
                self.free_receiver()
        
        #On remet à 0 l'index RX
        self.free_receiver()
        return data

    def free_receiver(self):
        '''! Remet à zero le compteur RX
        '''
        self.recSize = 0

    def free_sender(self):
        '''! Remet à zero le compteur TX
        '''
        self.sendSize = 0

    def send_buffer(self, OPCODE):
        '''! Envoie le buffer préconfiguré
        @param OPCODE code de l'opération
        @return succes de l'opération
        '''
        success = self.link.send(self.sendSize, packet_id=OPCODE)# Opcode important
        self.free_sender()
        return success

    # Réception de donnée
    def read_buffer(self, obj_type):
        '''! Lit le buffer RX
        @param Type de l'obj
        @return valeur
        '''
        data_size=-1
        #On récupère la form de la donnée (liste ou valeur seule)
        data_type = self.link.rx_obj(obj_type=STRING, start_pos=self.recSize, obj_byte_size=1)
        self.recSize += txfer.STRUCT_FORMAT_LENGTHS[CHAR.format]
        #Si valeur seule
        if(data_type==SERIALTALKING_SINGLE_MAGIC):
            data_size=1
            data = self.link.rx_obj(obj_type=obj_type, start_pos=self.recSize)
            self.recSize += txfer.STRUCT_FORMAT_LENGTHS[obj_type.format]

        #Sinon si valeur multiple (liste)
        elif(data_type==SERIALTALKING_MULTIPLE_MAGIC):
            data_arr = []
            #On récupère le nombre d'élément dans notre liste
            data_size = self.link.rx_obj(obj_type=UCHAR, start_pos=self.recSize)
            self.recSize += txfer.STRUCT_FORMAT_LENGTHS[UCHAR.format]

            #~magie (juste on append un liste où les données sont les obj reçu)
            for i in range(int(data_size)):

                    if(obj_type.format=="str"):
                        data_arr.append(self.link.rx_obj(obj_type=CHAR, start_pos=self.recSize))
                        self.recSize += 1
                    else:
                        data_arr.append(self.link.rx_obj(obj_type=obj_type, start_pos=self.recSize))
                        self.recSize += txfer.STRUCT_FORMAT_LENGTHS[obj_type.format]

            if(obj_type.format=="str"):
                data= b''.join(data_arr).decode()
                
        else:
            return (-1,-1) #pas normal

        return (data, data_size)

    # Réception de donnée
    def write_buffer(self, data, data_size=1):
        '''!Ecrit dans le buffer
        '''
        self.sendSize = self.link.tx_obj(UCHAR(data_size), start_pos=self.sendSize) #1 octet (la taille est 255 ça suffit) (correspond à uint8_t en c++)
        self.sendSize = self.link.tx_obj(data, start_pos=self.sendSize)

    def get_logs(self):
        '''
        Description:
        ------------
        Return all communication that didn't started with 0X7E
        :return: log buffer
        '''
        return self.link.get_logs()
    
    def clear_logs(self):
        '''
        Description:
        ------------
        Clear the log_buffer
        :return: void
        '''
        self.link.clear_logs()

if __name__ == '__main__':
     #Seulement pour test
    
    try:
        #Gestion du port série
        if 'linux' in sys.platform:
            serial_path = '/dev/ttyUSB0'
        else:
            serial_path = 'COM6'

        s = SerialTalking(serial_path)
        s.connect(5)
        while True:
            # Envoi
            test = "yes of course"

            #Réception
            ping_data, data_size = s.request(PING_OPCODE, STRING)
            ping2_data, data2_size = s.request(GETUUID_OPCODE, STRING)

            print("Ping data 1 : {}, Str size: {} | Ping data 2 : {}, Str size: {}".format(ping_data, data_size, ping2_data, data2_size))
            


    except KeyboardInterrupt:
        try:
            s.disconnect()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            s.disconnect()
        except:
            pass
