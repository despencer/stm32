import serial

class Pipe:
    def __init__(self, name):
        self.name = name
        self.pipe = None

    def open(self):
        self.pipe = open(self.name, 'wb+')

    def close(self)
        self.pipe.close()

    def send_byte(self, data):
        self.pipe.write(data.to_bytes(1, 'little'))

    def read_byte(self, data):
        buf = self.pipe.read(1)
        if len(buf) == 0:
            raise Exception("Pipe is broken")
        return buf[0]

    def flush(self):
        self.pipe.flush()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, extype, exvalue, extrace):
        self.close()

class Serial:
    def __init__(self, name):
        self.port = name
        self.baudrate = 38400
        self.parity = serial.PARITY_EVEN
        self.bytesize=serial.EIGHTBITS
        self.stopbits=serial.STOPBITS_ONE

    def open(self):
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, parity = self.parity, bytesize=self.bytesize, stopbits=self.stopbits)

    def close(self):
        self.serial.close()

    def send_byte(self, data):
        self.port.write(data.to_bytes(1, 'little'))

    def read_byte(self, data):
        buf = self.port.read(1)
        if len(buf) == 0:
            raise Exception("Serial port is broken")
        return buf[0]

    def flush(self):
        self.pipe.flush()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, extype, exvalue, extrace):
        self.close()


def openpipe(args):
    return Pipe(args.channel)

def openserial(args):
    return Serial(args.channel)

def getchannel(args):
    return {'pipe':openpipe,'serial':openserial}[args.chtype](args)
