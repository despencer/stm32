#!/usr/bin/env python

import slpx
import channel
import datetime

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("--chtype", default='serial', help="Channel type (*serial, pipe)", required=False)
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    with channel.open(args) as port:
        with slpx.open(port) as line:
            reader = slpx.Reader()
            print('Press ENTER to stop')
            reader.read(line, lambda msg: print(f'{datetime.datetime.now():%Y-%m-%d %H-%M-%S} {msg}'))
            input()
            reader.stop()

if __name__ == "__main__":
    main()