import port

class Mapper:
    def __init__(self):
        self.ports = []
        self.templates = [ "opencm3output.c" ]

    def addconfig(self, jmap, board):
        p = port.Port()
        p.reference = jmap['name']
        p.name = jmap['port']
        p.pin = jmap['pin']
        self.ports.append(p)