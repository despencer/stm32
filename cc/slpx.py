import threading

# message functions
SLPX_INFORMATION = 0x01
SLPX_TELEMETRY   = 0x02
SLPX_START       = 0x0102
SLPX_SHUTDOWN    = 0x0202
SLPX_HEARTBEAT   = 0x0402
SLPX_REBOOT      = 0x0103
SLPX_BOOTLOADER  = 0x0203

# protocol bytes
SLPX_BYTE_START     = 0xF0    # a start byte
SLPX_BYTE_ESCAPE    = 0xF1    # an escape byte
SLPX_BYTE_ESC_START = 0xF2    # a substitute for a start byte
SLPX_BYTE_ESC_ESC   = 0xF3    # a substitute for an escape byte

class SLPX:
    def __init__(self, channel):
        self.channel = channel
        self.xor_tx = 0
        self.xor_rx = 0
        self.lock_tx = threading.Lock()

    def open(self):
        self.send(SLPX_START, b'')

    def close(self):
        self.send(SLPX_SHUTDOWN, b'')

    def send_byte(self, data):
        if data == SLPX_BYTE_START:
            self.channel.send_byte(SLPX_BYTE_ESCAPE)
            self.channel.send_byte(SLPX_BYTE_ESC_START)
        elif data == SLPX_BYTE_ESCAPE:
            self.channel.send_byte(SLPX_BYTE_ESCAPE)
            self.channel.send_byte(SLPX_BYTE_ESC_ESC)
        else:
            self.channel.send_byte(data)
        self.xor_tx ^= data

    def read_byte(self):
        data = self.channel.read_byte()
        if data == SLPX_BYTE_ESCAPE:
            data = self.channel.read_byte()
            if data == SLPX_BYTE_ESC_START:
                data = SLPX_BYTE_START
            elif data == SLPX_BYTE_ESC_ESC:
                data = SLPX_BYTE_ESCAPE
            else:
                data = 0
        self.xor_rx ^= data
        return data

    def send(self, funcid, data):
        with self.lock_tx:
            self.xor_tx = 0
            buflen = len(data)
            self.channel.send_byte(SLPX_BYTE_START)
            self.send_byte( funcid & 0xFF )
            self.send_byte( (funcid>>8) & 0xFF )
            self.send_byte( buflen & 0xFF )
            self.send_byte( (buflen>>8) & 0xFF )
            for i in range(0, buflen):
                self.send_byte( data[i] )
            self.send_byte(self.xor_tx)
            self.channel.flush()

    def read(self):
        while True:
            self.xor_rx = 0
            while self.channel.read_byte() != SLPX_BYTE_START:
                pass
            funcid = self.read_byte()
            funcid += self.read_byte() << 8
            buflen = self.read_byte()
            buflen += self.read_byte() << 8
            data = []
            for i in range(0, buflen):
                data.append( self.read_byte() )
            self.read_byte()
            if self.xor_rx == 0:
                return (funcid, bytes(data) )

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, extype, exvalue, extrace):
        self.close()

def open(channel):
    return SLPX(channel)

class EmptyMessage:
    messages = {SLPX_START: "The firmare has started", SLPX_SHUTDOWN: "The firmware is going down"}
    def __init__(self, funcid, data):
        self.funcid = funcid
        self.message = self.messages[self.funcid]

    def __repr__(self):
        return f'{self.funcid:04X} {self.message}'

class HeartBeatMessage:
    def __init__(self, funcid, data):
        self.funcid = funcid
        self.counter = int.from_bytes(data, 'little')

    def __repr__(self):
        return f'{self.funcid:04X} HeartBeat #{self.counter:X}'

class Message:
    def __init__(self, funcid, data):
        self.funcid = funcid
        self.data = data

    def __repr__(self):
        return f'{self.funcid:04X} {self.data}'

messages = {SLPX_START: EmptyMessage, SLPX_SHUTDOWN:EmptyMessage, SLPX_HEARTBEAT:HeartBeatMessage}

def read(line):
    (funcid, msg) = line.read()
    if funcid in messages:
        return (messages[funcid])(funcid, msg)
    return Message(funcid, msg)

class Reader():
    ''' Runs in a separate thread '''
    def __init__(self):
        self.thread = None
        self.keeprunning = False

    def read(self, line, handler):
        self.thread = threading.Thread(target = self.loop, args=(line, handler), daemon=True )
        self.thread.start()

    def loop(self, line, handler):
        self.keeprunning = True
        while self.keeprunning:
            msg = read(line)
            handler(msg)
            if msg.funcid == SLPX_SHUTDOWN:
                return

    def stop(self):
        self.keeprunning = False
