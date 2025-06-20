#!/usr/bin/env python

from threading import Thread, Lock
import time

MSG_IN_MESSAGE = 0
MSG_IN_BOOTLOADER = 1
MSG_OUT_RESET = 0
MSG_OUT_BOOTLOADER = 1
prompt = 'reset>'

class Console:
    def __init__(self):
        self.lock = Lock()

    def input(self):
        return input(prompt)

    def print(self, msg):
        with self.lock:
            print('\n'+msg+'\n'+prompt)

class CommunicationProcessor:
    COMMAND = 1
    BOOTLOADER = 2
    STM32_START = 0x7F
    STM32_ACK = 0x79

    def __init__(self, args, console):
        self.args = args
        self.console = console
        self.handlers = {MSG_IN_MESSAGE:self.printer}
        self.mode = None

    def openserial(self):
        import serial
        return serial.Serial(port=self.args.channel, baudrate=38400, parity=serial.PARITY_EVEN, bytesize=serial.EIGHTBITS,
                             stopbits=serial.STOPBITS_ONE)
    def listen(self):
        self.listener = Thread(target=self.reader, daemon=True )
        self.listener.start()

    def write(self, data):
        self.channel.write(data)

    def reader(self):
        with self.openserial() as channel:
            self.channel = channel
            nextreader = self.readercommand
            while nextreader != None:
                nextreader = nextreader()

    def readercommand(self):
        self.mode = self.COMMAND
        self.console.print('Open channel in command mode')
        while True:
            msgbytes = self.channel.read(4)
            if len(msgbytes) == 0:
                break
            msg = int.from_bytes(msgbytes, 'little')
            size = int.from_bytes(self.channel.read(4), 'little')
            if msg == MSG_IN_BOOTLOADER:
                self.mode = None
                self.console.print('Close channel in command mode')
                return self.readerbootloader
            elif msg in self.handlers:
                self.handlers[msg](size)
            else:
                self.channel.read(size)

    def readerbootloader(self):
        self.console.print('Open channel in bootloader mode')
        time.sleep(0.5)
        self.channel.write(self.STM32_START.to_bytes(1))
        if not self.bl_check_ack:
            return None
        self.mode = self.BOOTLOADER
        self.console.print('Bootloader mode acknowledged')
        while True:
            time.sleep(0.1)

    def bl_check_ack(self):
        if int.from_bytes(self.channel.read(1)) != self.STM32_ACK:
            print('No acknowledment from MCU')
            return False
        return True

    def printer(self, size):
        self.console.print( self.channel.read(size).decode('ascii') )

class CommandProcessor:
    def __init__(self, args, console, comm):
        self.console = console
        self.comm = comm
        self.quit = False
        self.handlers = { 'quit':self.cmdquit, 'reset':self.cmdreset, 'bootloader':self.cmdbootloader }

    def loop(self):
        while not self.quit:
           cmd = self.console.input()
           if cmd in self.handlers:
                self.handlers[cmd]()
           elif len(cmd) > 0:
                self.console.print(f"Unrecognized command '{cmd}'")

    def cmdquit(self):
        self.quit = True

    def cmdreset(self):
        self.comm.write(MSG_OUT_RESET.to_bytes(4, 'little'))
        self.comm.write((0).to_bytes(4, 'little'))

    def cmdbootloader(self):
        self.comm.write(MSG_OUT_BOOTLOADER.to_bytes(4, 'little'))
        self.comm.write((0).to_bytes(4, 'little'))

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Control center")
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    console = Console()
    comm = CommunicationProcessor(args, console)
    comm.listen()
    CommandProcessor(args, console, comm).loop()

if __name__ == "__main__":
    main()
