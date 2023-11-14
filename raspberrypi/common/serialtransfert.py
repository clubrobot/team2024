import time
from pySerialTransfer import pySerialTransfer as txfer

#TODO: pensez à une trame efficace Faire avec des callback sur arduino uniquement?

MASTER_BYTE = b'R'
SLAVE_BYTE = b'A'

PING_OPCODE = 0x00
GETUUID_OPCODE = 0x01
SETUUID_OPCODE = 0x02
DISCONNECT_OPCODE = 0x03
GETEEPROM_OPCODE = 0x04
SETEEPROM_OPCODE = 0x05
GETBUFFERSIZE_OPCODE = 0x06

"""
class struct(object):
    z = ''
    y = 0.0
"""


if __name__ == '__main__':
     #Seuleument pour test
    
    try:
        #testStruct = struct
        link = txfer.SerialTransfer('/dev/ttyUSB0')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        while True:
            send_size = 0
            send_size = link.tx_obj(PING_OPCODE)
            link.send(send_size)

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
                ping_data = link.rx_obj(obj_type=str)
                recSize += len(ping_data)
                print("Ping data : {}".format(ping_data))
             
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