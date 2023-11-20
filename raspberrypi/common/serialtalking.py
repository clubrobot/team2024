'''
 SerialTalking Lib Work In progess: CRINSA 2024
 
 Negrache Gibril et Hilkens Boris
'''

import time
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
USHORT = 'H'
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

    def __exit__(self, exc_type, exc_value, traceback):
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

if __name__ == '__main__':
     #Seuleument pour test
    
    try:
        #testStruct = struct
        link = txfer.SerialTransfer('COM3')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        while True:
            send_size = 0
            send_size = link.tx_obj(0)#On met les params ici!
            link.send(send_size, packet_id=PING_OPCODE)

            if link.available():
                """
                recSize = 0

                testStruct.z = link.rx_obj(obj_type='c', start_pos=recSize)
                link.se
                recSize += txfer.STRUCT_FORMAT_LENGTHS['c']
                
                testStruct.y = link.rx_obj(obj_type='f', start_pos=recSize)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['f']
    
                print('{} {}'.format(testStruct.z, testStruct.y))"""

                recSize = 0

                data_size = link.rx_obj(obj_type='H', start_pos=recSize)#le type h à 2octects (correspond à uint16_t en c++)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['H']

                ping_data = link.rx_obj(obj_type=str, start_pos=recSize, obj_byte_size=data_size)
                recSize += len(ping_data)

                data2_size = link.rx_obj(obj_type='H', start_pos=recSize)#le type h à 2octects (correspond à uint16_t en c++)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['H']

                ping2_data = link.rx_obj(obj_type="H", start_pos=recSize)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['H']
                print(repr("Ping data : {}, Str size: {}".format(ping_data, data_size)))
                print(repr("Ping data : {}, Str size: {}".format(ping2_data, data2_size)))
             
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