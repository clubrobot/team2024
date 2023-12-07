'''
 SerialTalking Lib Work In progess: CRINSA 2024
 
 Negrache Gibril et Hilkens Boris
'''

import math
import time
import sys
from pySerialTransfer import pySerialTransfer as txfer

PING_OPCODE = 0x00
GETUUID_OPCODE = 0x01
SETUUID_OPCODE = 0x02
DISCONNECT_OPCODE = 0x03
GETEEPROM_OPCODE = 0x04
SETEEPROM_OPCODE = 0x05
GETBUFFERSIZE_OPCODE = 0x06

#https://docs.python.org/3/library/struct.html#format-characters
CHAR = 'c'
UCHAR = 'B'
SHORT = 'h'
USHORT = "H"
LONG = 'l'
ULONG = 'L'
FLOAT = 'f'
STRING = str
BYTE = CHAR
INT = SHORT #OUI CAR 16BIT = SHORT
UINT = USHORT
DOUBLE = 'd'

SERIALTALKING_SINGLE_MAGIC = 's' #comme single
SERIALTALKING_MULTIPLE_MAGIC = 'm' #comme multiple

#TODO: Les erreurs
#TODO: Faire un thread qui check périodiquement si l'arduino est alive (avec ping) lors qu'il ne communique pas
#TODO: Faire un meilleur log avec teleplot (à la fin)

class SerialTalking:
    def __init__(self, port):
        self.link = txfer.SerialTransfer(port)
        self.connect()
        time.sleep(2) # allow some time for the Arduino to completely reset

        self.recSize = 0
        self.sendSize = 0

    #Quand on utilise avec with
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self):
        self.disconnect()

    def connect(self):
        return self.link.open()
    
    def disconnect(self):
        self.link.close()
        return
    
    def available(self):
        return self.link.available()
    
    def get_status_code(self):
        return self.link.status

    def getuuid(self):
        return

    def setuuid(self, uuid):
        return

    #For each arg, on tx l'arg puis on envoie tout
    def order(self, opcode, *args):
        return

    #call order puis fait le tralala du request
    #à voir comment on gère ça
    def request(self, opcode, type,*args):
        return

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
        data_type = self.link.rx_obj(obj_type=str, start_pos=self.recSize, obj_byte_size=1)
        self.recSize += txfer.STRUCT_FORMAT_LENGTHS['c']
        #Si valeur seule
        if(data_type==SERIALTALKING_SINGLE_MAGIC):
            data_size=1
            data = self.link.rx_obj(obj_type=obj_type, start_pos=self.recSize)
            self.recSize += txfer.STRUCT_FORMAT_LENGTHS[obj_type]

        #Sinon si valeur multiple (liste)
        elif(data_type==SERIALTALKING_MULTIPLE_MAGIC):
            data_arr = []
            #On récupère le nombre d'élément dans notre liste
            data_size = self.link.rx_obj(obj_type=UCHAR, start_pos=self.recSize)
            self.recSize += txfer.STRUCT_FORMAT_LENGTHS[UCHAR]

            #~magie (juste on append un liste où les données sont les obj reçu)
            for i in range(int(data_size)):

                    if(obj_type==str):
                        data_arr.append(self.link.rx_obj(obj_type=CHAR, start_pos=self.recSize))
                        self.recSize += 1
                    else:
                        data_arr.append(self.link.rx_obj(obj_type=obj_type, start_pos=self.recSize))
                        self.recSize += txfer.STRUCT_FORMAT_LENGTHS[obj_type]

            if(obj_type==str):
                data= b''.join(data_arr).decode()
                
        else:
            return -1 #pas normal

        return (data, data_size)

    # Réception de donnée
    def write_buffer(self, data, val_type, data_size=1):
        self.sendSize = self.link.tx_obj(data_size, start_pos=self.sendSize, val_type_override=UCHAR) #1 octet (la taille est 255 ça suffit) (correspond à uint8_t en c++)
        if(type(data)==str):
            self.sendSize = self.link.tx_obj(data, start_pos=self.sendSize)
        else:
            self.sendSize = self.link.tx_obj(data, start_pos=self.sendSize, val_type_override=val_type)

if __name__ == '__main__':
     #Seulement pour test
    
    try:
        #Gestion du port série
        if 'linux' in sys.platform:
            serial_path = '/dev/ttyUSB0'
        else:
            serial_path = 'COM6'

        s = SerialTalking(serial_path)
        while True:
            # Envoi
            test = "yes of course"

            s.write_buffer(test, str, len(test))
            s.write_buffer(math.sin(time.time_ns()), FLOAT)
            s.send_buffer(PING_OPCODE)

            if s.available():
                #Réception
                s.free_receiver()
                ping_data, data_size = s.read_buffer(str)
                ping2_data, data2_size = s.read_buffer(FLOAT)

                print("Ping data 1 : {}, Str size: {} | Ping data 2 : {}, Str size: {}".format(ping_data, data_size, ping2_data, data2_size))

            elif s.get_status_code() < 0:
                if s.get_status_code() == txfer.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif s.get_status_code() == txfer.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif s.get_status_code() == txfer.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(s.get_status_code()))


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