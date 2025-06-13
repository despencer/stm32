#!/usr/bin/env python

import time

def openpipe(args):
    return open(args.channel, 'wb')

def getchannel(args):
    return {'pipe':openpipe}[args.chtype](args)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("chtype", type=str, help="Channel type")
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    with getchannel(args) as handle:
        tick = 0
        while True:
            handle.write((0).to_bytes(4, 'little'))
            handle.write((4).to_bytes(4, 'little'))
            handle.write(tick.to_bytes(4, 'little'))
            handle.flush()
            tick += 1
            time.sleep(1)

if __name__ == "__main__":
    main()
