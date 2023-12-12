'''
 SerialTalking Lib Work In progess: CRINSA 2024
 
 Negrache Gibril et Hilkens Boris
'''

import math
import time
import sys
from serialtypes import IntegerType, FloatType, StringType
import pySerialTransfer as txfer

BAUDRATE = 115200

#Défini les opcodes par défault
PING_OPCODE = 0x00
GETUUID_OPCODE = 0x01
SETUUID_OPCODE = 0x02
DISCONNECT_OPCODE = 0x03
GETEEPROM_OPCODE = 0x04
SETEEPROM_OPCODE = 0x05
GETBUFFERSIZE_OPCODE = 0x06

#Taille des chars
#https://docs.python.org/3/library/struct.html#format-characters

BYTEORDER = '<' #equal to little endian
ENCODING = 'utf-8'

CHAR = IntegerType('c', BYTEORDER)
UCHAR = IntegerType('B', BYTEORDER)
SHORT = IntegerType('h', BYTEORDER)
USHORT = IntegerType('H', BYTEORDER)
LONG = IntegerType('l', BYTEORDER)
ULONG = IntegerType('L', BYTEORDER)

FLOAT = FloatType('f', BYTEORDER)

STRING = StringType(ENCODING, BYTEORDER)

BYTE = UCHAR
INT = SHORT
UINT = USHORT
DOUBLE = FLOAT


#Magics numbers
SERIALTALKING_SINGLE_MAGIC = 's' #comme single
SERIALTALKING_MULTIPLE_MAGIC = 'm' #comme multiple

# Exceptions

class AlreadyConnectedError(ConnectionError): pass

class ConnectionFailedError(ConnectionError): pass

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
    def __init__(self, port):    
        self.port = port
        self.is_connected=False

        self.recSize = 0
        self.sendSize = 0

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self):
        self.disconnect()

    def connect(self, timeout=5):
        if self.is_connected:
            raise AlreadyConnectedError('{} is already connected'.format(self.port))

        # Connect to the serial port
        try:
            self.link = txfer.SerialTransfer(self.port, BAUDRATE)
            if(self.link.open()==False):
                raise ConnectionFailedError
        except Exception as e:
            raise ConnectionFailedError(str(e))
        
        startingtime = time.monotonic()
        while not self.is_connected:
            try:
                shouldBePong = self.request(PING_OPCODE, STRING)[0]
                if(shouldBePong[0]=="pong\x00"):
                    self.is_connected = True
                if(time.monotonic() - startingtime > timeout): raise TimeoutError
            except TimeoutError:
                if time.monotonic() - startingtime > timeout:
                    self.disconnect()
                    raise MuteError(
                        '\'{}\' is mute. It may not be an Arduino or it\'s sketch may not be correctly loaded.'.format(
                            self.port)) from None
                else:
                    continue

            except NotConnectedError:
                self.is_connected = False
    
    def disconnect(self):
        self.link.close()
        return
    
    def available(self):
        return self.link.available()
    
    def get_status_code(self):
        return self.link.status

    def getuuid(self):
        return self.request(GETUUID_OPCODE, return_type=str)

    def setuuid(self, uuid):
        return

    #For each arg, on tx l'arg puis on envoie tout
    def order(self, opcode, *args):
        if(len(args)==0): args = [BYTE(0x01)] #Si pas d'args
        #Oui le string fait chier
        for arg in args:
            if(arg.format=="str"):
                self.write_buffer(arg, len(arg.value))
            else:
                self.write_buffer(arg)
        self.send_buffer(opcode)
        return

    #call order puis fait le tralala du request
    def request(self, opcode, *args, timeout=5):
        data, data_size = ([], []) #Notre array
        self.order(opcode)# On envoit l'ordre pour avoir la réponse

        time.sleep(0.005)
        startingtime = time.monotonic()
        #Boucle while avec timeout
        while True:
            if(self.available()):#Tant que pas de réponse
                for arg in args:#On cycle dans tout les valeurs excepté
                    datum, datum_size = self.read_buffer(arg) #On lit le buffer
                    data.append(datum)
                    data_size.append(datum_size)
                break
            else:#si on a pas de réponse, on la force mdr
                self.order(opcode)
                time.sleep(0.005)
            if(time.monotonic() - startingtime > timeout): raise TimeoutError

        #On remet à 0 l'index RX
        self.free_receiver()
        return (data, data_size)

    def free_receiver(self):
        self.recSize = 0

    def free_sender(self):
        self.sendSize = 0

    def send_buffer(self, OPCODE):
        self.link.send(self.sendSize, packet_id=OPCODE)# Opcode important
        self.free_sender()

    # Réception de donnée
    def read_buffer(self, obj_type):
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
        self.sendSize = self.link.tx_obj(UCHAR(data_size), start_pos=self.sendSize) #1 octet (la taille est 255 ça suffit) (correspond à uint8_t en c++)
        self.sendSize = self.link.tx_obj(data, start_pos=self.sendSize)

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