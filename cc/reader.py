#!/usr/bin/env python

import time

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("channel", type=str, help="Communication channel")
    args = parser.parse_args()

    with open(args.channel, 'rb') as handle:
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