import port

class Mapper:
    def __init__(self):
        self.name = 'output'
        self.ports = []
        self.templates = [ "opencm3output.c", "opencm3output.h", "opencm3outputres.h" ]

    def addconfig(self, jmap, board):
        self.board = board
        p = port.Port()
        p.reference = jmap['name']
        p.name = jmap['port']
        p.pin = jmap['pin']
        self.ports.append(p)
        board.hal.resheaders.append("opencm3outputres.h")
        board.hal.resources.append("opencm3output.c")
