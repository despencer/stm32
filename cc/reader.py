#!/usr/bin/env python

import slpx
import channel
import time

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("--chtype", default='serial', help="Channel type (*serial, pipe)", required=False)
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    with channel.open(args) as port:
        with slpx.open(port) as line:
            while True:
                (funcid, data) = line.read()
                print(f'{funcid:04X} {data}')

if __name__ == "__main__":
    main()