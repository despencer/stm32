import builtins
import serial
import os
import time

class Pipe:
    def __init__(self, name):
        self.name = name
        self.readpipe = None
        self.sendpipe = None

    def open(self):
        names = self.name.split(':')
        self.readpipe = os.open(names[0], os.O_RDONLY | os.O_NONBLOCK)
        self.sendpipe = builtins.open(names[1], 'wb')

    def close(self):
        os.close(self.readpipe)
        self.sendpipe.close()

    def send_byte(self, data):
        self.sendpipe.write(data.to_bytes(1, 'little'))

    def read_byte(self):
        while True:
            try:
                buf = os.read(self.readpipe, 1)
                if buf != None and len(buf) > 0:
                    return buf[0]
            except OSError as e:
                if e.errno == 11:
                    time.sleep(0.5)
                else:
                    raise Exception(f"Pipe is broken with error {e}")

    def flush(self):
        self.sendpipe.flush()

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
        self.serial.write(data.to_bytes(1, 'little'))

    def read_byte(self):
        buf = self.serial.read(1)
        if len(buf) == 0:
            raise Exception("Serial port is broken")
        return buf[0]

    def flush(self):
        self.serial.flush()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, extype, exvalue, extrace):
        self.close()


def openpipe(args):
    return Pipe(args.channel)

def openserial(args):
    return Serial(args.channel)

def open(args):
    return {'pipe':openpipe,'serial':openserial}[args.chtype](args)
