#!/usr/bin/env python

import time

def openpipe(args):
    return open(args.channel, 'rb')

def openserial(args):
    import serial
    return serial.Serial(port=args.channel, baudrate=38400, parity=serial.PARITY_EVEN, bytesize=serial.EIGHTBITS,
                         stopbits=serial.STOPBITS_ONE)

def getchannel(args):
    return {'pipe':openpipe,'serial':openserial}[args.chtype](args)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("chtype", type=str, help="Channel type")
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    with getchannel(args) as handle:
        while True:
#            cc = int.from_bytes(handle.read(1))
#            print(f'{cc:02X} {cc}\n')
             cb = handle.read(1)
             print(f'{cb[0]:02X} {cb.decode('ascii')}')
#             print(f'{cb[0]:02X}')

if __name__ == "__main__":
    main()