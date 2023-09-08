from common.serialtalks import BYTE, INT, LONG, FLOAT, USHORT, SerialTalks

class VL53(SerialTalks):
    def __init__(self, uuid='/dev/tty.SLAB_USBtoUART'):
        SerialTalks.__init__(self, uuid)

    def test(self):
        output = self.execute(0x10)
        return output.read(USHORT)

if __name__ == "__main__":
    sen = VL53("/dev/ttyUSB0")
    sen.connect()
    while 1:
        print(sen.test())