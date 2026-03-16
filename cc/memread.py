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
            chunk = min(size, 256)
            data = control.read_chunk(bline, start, chunk)
            if data == None:
                return
            target.write(data)
            size -= chunk
            print(f'Read {chunk} bytes at {start:X}, left {size} bytes')
            start += chunk
    print('All data was read successfully')
    control.exit_bootloader(bline)

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
