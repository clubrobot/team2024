import struct

class IntegerType():
    def __init__(self, formatt, byteorder):
        self.format = formatt
        self.byteorder = byteorder

    def __call__(self, value):
        self.value = value
        return self
    
    def to_bytes(self, integer):
        return int.to_bytes(integer, length=self.length, byteorder=self.byteorder)

    def from_bytes(self, rawbytes):
        return int.from_bytes(rawbytes[:self.length], byteorder=self.byteorder)


class FloatType():

    def __init__(self, formatt, byteorder):
        self.format = formatt  # May be 'f' (float) or 'd' (double)
        self.byteorder = byteorder

    def __call__(self, value):
        self.value = value
        return self

    def to_bytes(self, real):
        return struct.pack(self.standard, real)

    def from_bytes(self, rawbytes):
        length = {'f': 4, 'd': 8}[self.standard]
        return struct.unpack(self.standard, rawbytes[:length])[0]


class StringType():

    def __init__(self, encoding, byteorder):
        self.format ="str"
        self.byteorder = byteorder
        self.encoding = encoding

    def __call__(self, value):
        self.value = value
        return self

    def to_bytes(self, string):
        return string.encode(self.encoding) + b'\0'

    def from_bytes(self, rawbytes):
        index = rawbytes.index(b'\0')
        return rawbytes[:index].decode(self.encoding)