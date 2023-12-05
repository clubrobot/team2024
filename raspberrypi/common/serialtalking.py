'''
 SerialTalking Lib Work In progess: CRINSA 2024
 
 Negrache Gibril et Hilkens Boris
'''

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
STRING = 's'
BYTE = UCHAR
INT = SHORT
UINT = USHORT
DOUBLE = FLOAT

#TODO: Les erreurs
#TODO: Faire un thread qui check périodiquement si l'arduino est alive (avec ping) lors qu'il ne communique pas
#TODO: Faire un meilleur log avec teleplot (à la fin)

class SerialTalking:
    def __init__(self):
        pass

    #Quand on utilise avec with
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self):
        self.disconnect()

    def connect(self, timeout=5):
        return
    
    def disconnect(self):
        return
    
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

    # Réception de donnée
    def recieve_transfert(self, obj_type):
        data_size = link.rx_obj(obj_type='H', start_pos=self.recSize) #le type h à 2octects (correspond à uint16_t en c++)
        data = link.rx_obj(obj_type=obj_type, start_pos=self.recSize, obj_byte_size=data_size)
        if (obj_type == str):
            data_size = len(data)
        else:
            data_size = txfer.STRUCT_FORMAT_LENGTHS[obj_type]
        self.recSize += data_size
        return (data, data_size)

    # Réception de donnée
    def send_transfert(self, data, data_size,val_type_override=''):
        self.sendSize = link.tx_obj(data_size, start_pos=self.sendSize,val_type_override=USHORT) #le type h à 2octects (correspond à uint16_t en c++)
        self.sendSize = link.tx_obj(data, start_pos=self.sendSize,val_type_override)
        return self.sendSize

if __name__ == '__main__':
     #Seulement pour test
    
    try:
        #Gestion du port série
        if 'linux' in sys.platform:
            serial_path = '/dev/ttyUSB0'
        else:
            serial_path = 'COM6'
        link = txfer.SerialTransfer(serial_path)
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset

        s = SerialTalking()
        while True:
            # Envoi
            """
            send_size = 0
            send_size = link.tx_obj(1, send_size, val_type_override=USHORT)#On met la size d'envoie ici
            send_size = link.tx_obj(5.8, send_size, val_type_override=FLOAT)#On met les params ici!
            send_size = link.tx_obj(1, send_size, val_type_override=USHORT)#On met la size d'envoie ici
            send_size = link.tx_obj(8, send_size, val_type_override=BYTE)#On met les params ici!"""
            s.free_sender()
            send_size = s.send_transfert(5.8,1,FLOAT)
            send_size = s.send_transfert(8,1,BYTE)
            link.send(send_size, packet_id=PING_OPCODE)# Opcode important

            if link.available():
                #Réception
                s.free_receiver()

                ping_data, data_size = s.recieve_transfert(str)
                ping2_data, data2_size = s.recieve_transfert('f')
                ping3_data, data3_size = s.recieve_transfert(BYTE)

                print(repr("Ping data 1 : {}, Str size: {}".format(ping_data, data_size)))
                print(repr("Ping data 2 : {}, Str size: {}".format(ping2_data, data2_size)))
                print(repr("Ping data 3 : {}, Str size: {}".format(ping3_data, data3_size)))
            elif link.status < 0:
                if link.status == txfer.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif link.status == txfer.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif link.status == txfer.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(link.status))


    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass