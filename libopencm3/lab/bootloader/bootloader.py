#!/usr/bin/env python

from threading import Thread, Lock

STM32_START = 0x7F

class Console:
    def __init__(self):
        self.lock = Lock()

    def input(self):
        return input(prompt)

    def print(self, msg):
        with self.lock:
            print('\n'+msg+'\n'+prompt)

class CommunicationProcessor:
    def __init__(self, args, console):
        self.args = args
        self.console = console
        import serial
        self.channel = serial.Serial(port=self.args.channel, baudrate=38400, parity=serial.PARITY_EVEN, bytesize=serial.EIGHTBITS,
                             stopbits=serial.STOPBITS_ONE)

    def open(self):
#        self.channel.open()
        pass

    def close(self):
        self.channel.close()

    def write(self, data):
        self.channel.write(data)

    def read(self, size):
        return self.channel.read(size)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, extype, exvalue, extrace):
        self.close()

class CommandProcessor:
    def __init__(self, args, console, channel):
        self.console = console
        self.channel = channel
        self.quit = False
        self.handlers = { 'version':self.cmdversion }

    def handle(self, cmd):
        if cmd in self.handlers:
            self.handlers[cmd]()
        else:
            self.console.print(f"Unrecognized command '{cmd}'")

    def cmdversion(self):
        self.channel.write(STM32_START.to_bytes(1))
        print(STM32_START.to_bytes(1))
        print(self.channel.read(1))

def main():
    import argparse

    parser = argparse.ArgumentParser(description="STM32 Bootloader")
    parser.add_argument("channel", type=str, help="Channel name")
    parser.add_argument("command", type=str, help="Command")
    args = parser.parse_args()

    console = Console()
    with CommunicationProcessor(args, console) as comm:
        CommandProcessor(args, console, comm).handle(args.command)

if __name__ == "__main__":
    main()
