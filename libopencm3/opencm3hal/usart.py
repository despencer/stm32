import port
import config

class Usart:
    def __init__(self):
        self.reference = None
        self.ports = []
        self.tx = None
        self.rx = None
        self.baudrate = 38400
        self.databits = 8
        self.stopbits = "1"
        self.parity = "NONE"
        self.rx_bufsize = 256
        self.tx_bufsize = 256

class Mapper:
    def __init__(self):
        self.name = 'usart'
        self.prefix = 'hal_'
        self.templates = [ "opencm3usart.c", "opencm3usart.h", "opencm3usartres.h" ]
        self.usarts = []
        self.ports = []
        self.hastx = False
        self.hasrx = False

    def addconfig(self, jmap, board):
        self.board = board
        u = Usart()
        u.reference = jmap['name']
        u.index = jmap['index']
        if 'parity' in jmap:
            u.parity = jmap['parity']
        if u.parity == 'EVEN':
            u.databits += 1
        self.addport(u, jmap, 'tx', board)
        self.addport(u, jmap, 'rx', board)
        self.usarts.append(u)
        if "opencm3usartres.h" not in board.hal.resheaders:
            board.hal.resheaders.append("opencm3usartres.h")
        if "opencm3usart.c" not in board.hal.resources:
            board.hal.resources.append("opencm3usart.c")
        if u.tx != None:
            self.hastx = True
        if u.rx != None:
            self.hasrx = True

    def addport(self, usart, jmap, ptype, board):
        if ptype not in jmap:
            return
        p = port.Port()
        p.type = ptype
        p.name = jmap[ptype]['port']
        p.pin = jmap[ptype]['pin']
        p.function = config.getfunc(board.mcu, 'usart', usart.index, ptype, p.name, p.pin)
        setattr(usart, ptype, p)
        usart.ports.append(p)
        if p.name not in self.ports:
              self.ports.append(p.name)


