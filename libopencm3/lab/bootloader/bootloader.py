#!/usr/bin/env python

from threading import Thread, Lock

STM32_START = 0x7F
STM32_ACK = 0x79
STM32_GETCOMMAND = bytes.fromhex('00FF')
STM32_GETIDCOMMAND = bytes.fromhex('02FD')

class CommunicationProcessor:
    def __init__(self, args):
        self.args = args
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
    def __init__(self, args, channel):
        self.channel = channel
        self.quit = False
        self.handlers = { 'version':self.cmdversion }

    def handle(self, cmd):
        if cmd in self.handlers:
            self.handlers[cmd]()
        else:
            self.console.print(f"Unrecognized command '{cmd}'")

    def check_ack(self):
        if int.from_bytes(self.channel.read(1)) != STM32_ACK:
            print('No acknowledment from MCU')
            return False
        return True

    def start(self):
        self.channel.write(STM32_START.to_bytes(1))
        print('Initializing bootloader interface')
        return self.check_ack()

    def cmdversion(self):
        if not self.start():
            return
        self.channel.write(STM32_GETCOMMAND)
        print('Sending GET command')
        if not self.check_ack():
            return
        size = int.from_bytes(self.channel.read(1))
        version = int.from_bytes(self.channel.read(1))
        print(f'Bootloader version: {version:02X}')
        self.channel.read(size)
        self.check_ack()
        self.channel.write(STM32_GETIDCOMMAND)
        print('Sending GETID command')
        if not self.check_ack():
            return
        size = int.from_bytes(self.channel.read(1)) - 1
        did = int.from_bytes(self.channel.read(2), 'little')
        print(f'Device ID: {did:04X}')
        if size > 0:
            self.channel.read(size)
        self.check_ack()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="STM32 Bootloader")
    parser.add_argument("channel", type=str, help="Channel name")
    parser.add_argument("command", type=str, help="Command")
    args = parser.parse_args()

    with CommunicationProcessor(args) as comm:
        CommandProcessor(args, comm).handle(args.command)

if __name__ == "__main__":
    main()
