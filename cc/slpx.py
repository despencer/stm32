# message functions
SLPX_INFORMATION = 0x01
SLPX_TELEMETRY   = 0x02
SLPX_START       = 0x0102
SLPX_STOP        = 0x0302
SLPX_HEARTBEAT   = 0x0502

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

    def open(self):
        self.send(SLPX_START, b'')

    def close(self):
        self.send(SLPX_STOP, b'')

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
