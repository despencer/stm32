import port
import config

class Usart:
    def __init__(self):
        self.reference = None
        self.tx = None

class Mapper:
    def __init__(self):
        self.name = 'usart'
        self.templates = [ "opencm3usart.c", "opencm3usart.h", "opencm3usartres.h", "opencm3output.h" ]
        self.usarts = []

    def addconfig(self, jmap, board):
        self.board = board
        u = Usart()
        u.reference = jmap['name']
        u.index = jmap['index']
        self.addport(u, jmap, 'tx', board)
        self.usarts.append(u)
        if "opencm3usartres.h" not in board.hal.resheaders:
            board.hal.resheaders.append("opencm3usartres.h")
        if "opencm3usart.c" not in board.hal.resources:
            board.hal.resources.append("opencm3usart.c")

    def addport(self, usart, jmap, ptype, board):
        if ptype not in jmap:
            return
        p = port.Port()
        p.name = jmap[ptype]['port']
        p.pin = jmap[ptype]['pin']
        p.function = config.getfunc(board.mcu, 'usart', usart.index, ptype, p.name, p.pin)
        setattr(usart, ptype, p)


