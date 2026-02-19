#!/usr/bin/env python

import slpx
import sbup
import channel
import datetime
import time
import control

def read_memory(line, filename, start, size):
    bline = control.enter_bootloader(line)
    if bline == None:
        return
    with open(filename, 'wb') as target:
        while size > 0:
            chunk = min(size, 256) - 1
            if not bline.send_command(sbup.SBUP_CMD_READMEMORY):
                print('Failed to execute Read Memory command')
                return
            if not bline.send_data(start.to_bytes(4, 'big')):
                print('Failed to send address')
                return
            if not bline.send_command(chunk):
                print('Failed to send size')
                return
            target.write(bline.read(chunk+1))
            size -= chunk+1
            print(f'Read {chunk+1} bytes at {start:X}, left {size} bytes')
            start += chunk+1
    print('All data was read successfully')

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Reads a chip memory to a file")
    parser.add_argument("--chtype", default='serial', help="Channel type (*serial, pipe)", required=False)
    parser.add_argument("channel", type=str, help="Channel name")
    parser.add_argument("start", type=str, help="Start address")
    parser.add_argument("size", type=str, help="Memory span")
    parser.add_argument("filename", type=str, help="File to dump")
    args = parser.parse_args()

    with channel.open(args) as port:
        line = slpx.open(port)
        line.open()
        read_memory(line, args.filename, eval(args.start), eval(args.size))

if __name__ == "__main__":
    main()
