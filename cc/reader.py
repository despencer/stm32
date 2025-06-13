#!/usr/bin/env python

import time

def openpipe(args):
    return open(args.channel, 'rb')

def getchannel(args):
    return {'pipe':openpipe}[args.chtype](args)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("chtype", type=str, help="Channel type")
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    with getchannel(args) as handle:
        while True:
            msgbytes = handle.read(4)
            if len(msgbytes) == 0:
                break
            msg = int.from_bytes(msgbytes, 'little')
            size = int.from_bytes(handle.read(4), 'little')
            body = handle.read(size)
            print(msg, size, body)

if __name__ == "__main__":
    main()