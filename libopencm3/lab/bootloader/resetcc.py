#!/usr/bin/env python

from threading import Thread, Lock

MSG_IN_MESSAGE = 0
MSG_OUT_RESET = 0
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
    def __init__(self, args, console):
        self.args = args
        self.console = console
        self.handlers = {MSG_IN_MESSAGE:self.printer}

    def openpipe(self):
        return open(self.args.channel, 'rb')

    def openserial(self):
        import serial
        return serial.Serial(port=self.args.channel, baudrate=38400, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS,
                             stopbits=serial.STOPBITS_ONE)

    def getchannel(self):
        return {'pipe':self.openpipe,'serial':self.openserial}[self.args.chtype]()

    def listen(self):
        self.listener = Thread(target=self.reader, daemon=True )
        self.listener.start()

    def write(self, data):
        self.channel.write(data)

    def reader(self):
        with self.getchannel() as channel:
            self.channel = channel
            while True:
                msgbytes = channel.read(4)
                if len(msgbytes) == 0:
                    break
                msg = int.from_bytes(msgbytes, 'little')
                size = int.from_bytes(channel.read(4), 'little')
                if msg in self.handlers:
                    self.handlers[msg](size)
                else:
                    channel.read(size)

    def printer(self, size):
        self.console.print( self.channel.read(size).decode('ascii') )

class CommandProcessor:
    def __init__(self, args, console, comm):
        self.console = console
        self.comm = comm
        self.quit = False
        self.handlers = { 'quit':self.cmdquit, 'reset':self.cmdreset }

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

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Control center")
    parser.add_argument("chtype", type=str, help="Channel type")
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    console = Console()
    comm = CommunicationProcessor(args, console)
    comm.listen()
    CommandProcessor(args, console, comm).loop()

if __name__ == "__main__":
    main()
