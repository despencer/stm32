#!/usr/bin/env python

import serial
import time
import functools
import operator

MSG_IN_BOOTLOADER = 1
MSG_OUT_BOOTLOADER = 1

STM32_BL_START = bytes.fromhex('7F')
STM32_BL_ACK = bytes.fromhex('79')
STM32_BL_READMEMORY = bytes.fromhex('11EE')

def xor(array):
    return bytes([ functools.reduce(operator.xor, array)  ])

def get_ack(channel):
    ack = channel.read(1)
    if ack != STM32_BL_ACK:
        print('No acknowledge with', ack)
        return False
    return True

def enter_bootloader(channel):
    print('Sending request to reset to bootloader mode')
    channel.write(MSG_OUT_BOOTLOADER.to_bytes(4, 'little'))
    channel.write((0).to_bytes(4, 'little'))
    while True:
        msgbytes = channel.read(4)
        if len(msgbytes) == 0:
            print('Unexpected break of communication')
            return False
        msg = int.from_bytes(msgbytes, 'little')
        size = int.from_bytes(channel.read(4), 'little')
        if msg == MSG_IN_BOOTLOADER:
            print('Bootloader mode activated')
            time.sleep(1)
            channel.write(STM32_BL_START)
            if not get_ack(channel):
                return False
            else:
                print('Bootloader mode is acknowledged')
                return True
        else:
            channel.read(size)

def read_memory(channel, target, start, size):
    if not enter_bootloader(channel):
        return
    while size > 0:
        chunk = min(size, 256) - 1
        channel.write(STM32_BL_READMEMORY)
        if not get_ack(channel):
            return
        channel.write(start.to_bytes(4, 'big'))
        channel.write( xor(start.to_bytes(4, 'big')) )
        if not get_ack(channel):
            return
        channel.write(chunk.to_bytes(1))
        channel.write((chunk ^ 255).to_bytes(1))
        if not get_ack(channel):
            return
        target.write(channel.read(chunk+1))
        size -= chunk+1
        start += chunk+1
        print('Read', chunk+1, 'bytes, left', sizem 'bytes')

def main():
    import argparse

    parser = argparse.ArgumentParser(description="STM32 Memory reader")
    parser.add_argument("channel", type=str, help="Channel name")
    parser.add_argument("start", type=str, help="Start address")
    parser.add_argument("size", type=str, help="Memory span")
    parser.add_argument("filename", type=str, help="File to dump")
    args = parser.parse_args()

    with serial.Serial(port=args.channel, baudrate=38400, parity=serial.PARITY_EVEN, bytesize=serial.EIGHTBITS,
                             stopbits=serial.STOPBITS_ONE) as channel:
        print('Open serial communication')
        with open(args.filename, 'wb') as target:
            read_memory(channel, target, eval(args.start), eval(args.size))

if __name__ == "__main__":
    main()

