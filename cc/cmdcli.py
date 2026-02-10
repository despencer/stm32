#!/usr/bin/python3
import threading
import curses
import slpx
import sbup
import channel
import datetime

class CursesInput:
    def __init__(self):
        self.history = []
        self.keeprunning = False
        self.handler = None
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
            self.handler(self, line)
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

class Bootloader:
    def __init__(self, line, shell, manager):
        self.line = sbup.open(line.channel)
        self.shell = shell
        self.manager = manager
        self.commands = {'quit': lambda s,c: s.stop(), 'id': self.getid }

    def start(self):
        self.shell.addline('-B Start bootloader mode')
        self.shell.handler = self.handler
        if self.line.start():
            self.shell.addline('-B bootloader mode confirmed')
        else:
            self.shell.addline('-B bootloader mode NOT confirmed')

    def handler(self, shell, command):
        cmdname = command.split(' ')[0]
        if cmdname in self.commands:
            self.commands[cmdname](shell, command)
        else:
            shell.addline(f"-B Unknown command '{cmdname}'. Print 'quit' for stop")

    def getid(self, shell, command):
        if not self.line.send_command(sbup.SBUP_CMD_GETID):
            shell.addline('-B No ACK for ID command')
            return
        data = self.line.read_data()
        if data == None:
            shell.addline('-B No data receiver for ID command')
            return
        shell.addline(f"{datetime.datetime.now():%Y-%m-%d %H-%M-%S}-B: ID {int.from_bytes(data, 'little'):X}")

class Manager:
    def __init__(self, line, shell):
        self.line = line
        self.shell = shell
        self.reader = slpx.Reader()
        self.commands = {'quit': lambda s,c: s.stop(), 'reset': self.reset, 'bootloader': self.bootloader}
        self.onshutdown = self.start
        self.bootloader = None

    def handler(self, shell, command):
        cmdname = command.split(' ')[0]
        if cmdname in self.commands:
            self.commands[cmdname](shell, command)
        else:
            shell.addline(f"-- Unknown command '{cmdname}'. Print 'quit' for stop")

    def msghandler(self, msg):
        self.shell.addline(f'{datetime.datetime.now():%Y-%m-%d %H-%M-%S} {msg}')
        if msg.funcid == slpx.SLPX_SHUTDOWN:
            self.onshutdown()

    def start(self):
        self.shell.addline('-- Start system mode')
        self.shell.handler = self.handler
        self.reader.read(self.line, self.msghandler)
        self.line.open()

    def startbl(self):
        self.onshutdown = self.start
        self.line.close()
        self.bootloader.start()

    def reset(self, shell, command):
        self.shell.addline('-- Sending REBOOT command')
        self.line.send(slpx.SLPX_REBOOT, b'')

    def bootloader(self, shell, command):
        self.shell.addline('-- Sending BOOTLOADER command')
        self.onshutdown = self.startbl
        self.line.send(slpx.SLPX_BOOTLOADER, b'')

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Produces heartbeat")
    parser.add_argument("--chtype", default='serial', help="Channel type (*serial, pipe)", required=False)
    parser.add_argument("channel", type=str, help="Channel name")
    args = parser.parse_args()

    with channel.open(args) as port:
        line = slpx.open(port)
        shell = CursesInput()
        manager = Manager(line, shell)
        manager.bootloader = Bootloader(line, shell, manager)
        manager.start()
        shell.run()

if __name__ == "__main__":
    main()
