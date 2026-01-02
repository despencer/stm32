#!/usr/bin/python3
import threading
import curses
import slpx
import channel
import datetime


class CursesInput:
    def __init__(self, handler):
        self.history = []
        self.keeprunning = False
        self.handler = handler
        self.lock = threading.Lock()

    def open(self):
        self.cout = curses.newwin(curses.LINES-3, curses.COLS, 0, 0)
        self.ccmd = curses.newwin(3, curses.COLS, curses.LINES-3, 0)
        self.cout.border()
        self.ccmd.border()
        self.cout.refresh()
        self.ccmd.addstr(1, 1, '>')
        self.ccmd.move(1, 2)

    def loop(self, stdscr):
        self.open()
        self.keeprunning = True
        while self.keeprunning:
            line = ''
            while True:
                key = self.ccmd.getkey()
                if key == '\n':
                    break
                self.ccmd.addstr(1, 2+len(line), key)
                line += key
                self.ccmd.refresh()
            handler(self, line)
            self.ccmd.addstr(1, 1, '>' + ' ' * (curses.COLS-3))
            self.ccmd.move(1, 2)
        stdscr.clear()
        stdscr.refresh()

    def run(self):
        curses.wrapper(self.loop)

    def addline(self, line):
        with self.lock:
            self.history.append(line)
            if self.keeprunning:
                wnd = curses.LINES-5
                for i in range(wnd):
                    if i < len(self.history):
                        self.cout.addstr(wnd-i, 1, self.history[ -i-1 ].ljust(curses.COLS-2) )
                self.cout.refresh()

    def stop(self):
        self.keeprunning = False

def handler(shell, command):
    shell.stop()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("--chtype", default='serial', help="Channel type (*serial, pipe)", required=False)
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    with channel.open(args) as port:
        with slpx.open(port) as line:
            shell = CursesInput(handler)
            reader = slpx.Reader()
            reader.read(line, lambda msg: shell.addline(f'{datetime.datetime.now():%Y-%m-%d %H-%M-%S} {msg}'))
            shell.run()

if __name__ == "__main__":
    main()
