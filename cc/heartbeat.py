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
            tick = 0
            while True:
                line.send(slpx.SLPX_HEARTBEAT, tick.to_bytes(4, 'little'))
                tick += 1
                time.sleep(1)

if __name__ == "__main__":
    main()
