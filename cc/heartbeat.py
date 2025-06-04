#!/usr/bin/env python

import time

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("channel", type=str, help="Communication channel")
    args = parser.parse_args()

    with open(args.channel, 'wb') as handle:
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
