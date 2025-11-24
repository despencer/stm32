#!/usr/bin/env python

import serial
import time
import functools
import operator
import yaml

class FlashPage:
    def __init__(self, start, size):
        self.start = start
        self.size = size

    @classmethod
    def load(cls, filename):
        with open(filename) as f:
            jmcu = yaml.load(f, Loader=yaml.Loader)
            pages = []
            for jpage in jmcu['flash']['pages']:
                pages.append( cls(jpage['address'], jpage['size']) )
            return pages

    @classmethod
    def select(cls, pages, start, size):
        if start < pages[0].start or (start+size) > (pages[-1].start + pages[-1].size):
            return None
        result = []
        for p in pages:
            if(  (p.start <= start and start < (p.start + p.size)) or
                 (p.start <= (start+size-1) and (start+size-1) < (p.start + p.size)) or
                 (start < p.start and (start+size-1) > (p.start + p.size))   ):
                 result.append(p)
        return result

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
        print('Read', chunk+1, 'bytes, left', size, 'bytes')

def erase_memory(channel, mcu, start, size):
    pages = FlashPage.load(mcu)
    pages = FlashPage.select(pages, start, size)
    print(f'start: {start:X} size:{size:X}')
    for p in pages:
        print(f'   page {p.start:X} size: {p.size:X}')

def main():
    import argparse

    parser = argparse.ArgumentParser(description="STM32 Memory writer")
    parser.add_argument("channel", type=str, help="Channel name")
    parser.add_argument("start", type=str, help="Start address")
    parser.add_argument("size", type=str, help="Memory span")
    parser.add_argument("filename", type=str, help="File to dump")
    parser.add_argument("mcu", type=str, help="MCU definition")
    args = parser.parse_args()
    erase_memory(None, args.mcu, 0x8000000, 16)
    erase_memory(None, args.mcu, 0x8000010, 16)
    erase_memory(None, args.mcu, 0x8000000, 16*1024)
    erase_memory(None, args.mcu, 0x8000000, 16*1024+1)
    return

    with serial.Serial(port=args.channel, baudrate=38400, parity=serial.PARITY_EVEN, bytesize=serial.EIGHTBITS,
                             stopbits=serial.STOPBITS_ONE) as channel:
        print('Open serial communication')
        with open(args.filename, 'wb') as target:
            read_memory(channel, target, eval(args.start), eval(args.size))

if __name__ == "__main__":
    main()

