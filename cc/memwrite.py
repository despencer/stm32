#!/usr/bin/env python

import slpx
import sbup
import channel
import datetime
import time
import yaml
import control
import os

class FlashPage:
    def __init__(self, idx, start, size):
        self.idx = idx
        self.start = start
        self.size = size

    @classmethod
    def load(cls, filename):
        with open(filename) as f:
            jmcu = yaml.load(f, Loader=yaml.Loader)
            pages = []
            for jpage in jmcu['flash']['pages']:
                pages.append( cls(len(pages), jpage['address'], jpage['size']) )
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


def erase_memory(bline, mcu, start, size, extended=False):
    pages = FlashPage.load(mcu)
    pages = FlashPage.select(pages, start, size)
    if len(pages) == 0:
        print('Nothing to erase')
        return False
    print(f'Memory erase start: {start:X} size:0x{size:X} ({size})')
    if extended:
        pdata = [ 0, len(pages)-1 ]
        cmd = sbup.SBUP_CMD_EXTERASEMEMORY
    else:
        pdata = [ len(pages)-1 ]
        cmd = sbup.SBUP_CMD_ERASEMEMORY
    for p in pages:
        print(f'   page #{p.idx} {p.start:X} size: 0x{p.size:X} ({p.size})')
        if extended:
            pdata.append(0)
        pdata.append(p.idx)
    if not bline.send_command(cmd):
        print('Failed to execute Erase Memory command')
        return False
    data = bytes(pdata)
    if not bline.send_data(data):
        print(f'Failed to send erase data {data}')
        return False
    return True

def write_memory(line, mcu, filename, start):
    size = os.path.getsize(filename)
    bline = control.enter_bootloader(line)
    if bline == None:
        return
    if not erase_memory(bline, mcu, start, size, extended=True):
        return
    with open(filename, 'rb') as source:
        while size > 0:
            chunk = min(size, 256) - 1
            if not bline.send_command(sbup.SBUP_CMD_WRITEMEMORY):
                print('Failed to execute Write Memory command')
                return
            if not bline.send_data(start.to_bytes(4, 'big')):
                print('Failed to send address')
                return
            data = source.read(chunk+1)
            data = bytes([chunk] + list(data))
            if not bline.send_data(data):
                print('Failed to send data')
                return
            size -= chunk+1
            print(f'Write {chunk+1} bytes at {start:X}, left {size} bytes')
            start += chunk+1
    print('All data was written successfully')

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Writes a file to a chip memory")
    parser.add_argument("--chtype", default='serial', help="Channel type (*serial, pipe)", required=False)
    parser.add_argument("channel", type=str, help="Channel name")
    parser.add_argument("mcu", type=str, help="MCU definition")
    parser.add_argument("start", type=str, help="Start address")
    parser.add_argument("filename", type=str, help="Source file")
    args = parser.parse_args()

    with channel.open(args) as port:
        line = slpx.open(port)
        line.open()
        write_memory(line, args.mcu, args.filename, eval(args.start) )

if __name__ == "__main__":
    main()
