import time
from pySerialTransfer import pySerialTransfer as txfer

#TODO: pensez à une trame efficace Faire avec des callback sur arduino uniquement?

class struct(object):
    z = ''
    y = 0.0

if __name__ == '__main__':
     #Seuleument pour test
    
    try:
        testStruct = struct

        link = txfer.SerialTransfer('COM3')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        
        while True:
            send_size = 0

            if link.available():
                recSize = 0

                testStruct.z = link.rx_obj(obj_type='c', start_pos=recSize)
                link.se
                recSize += txfer.STRUCT_FORMAT_LENGTHS['c']
                
                testStruct.y = link.rx_obj(obj_type='f', start_pos=recSize)
                recSize += txfer.STRUCT_FORMAT_LENGTHS['f']
    
                print('{} {}'.format(testStruct.z, testStruct.y))
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