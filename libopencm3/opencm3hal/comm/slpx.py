''' Config reader and code generator for SLPX protocol '''

class SLPX:
    def __init__(self):
        self.reference = None
        self.port = None

class Mapper:
    def __init__(self):
        self.name = 'slpx'
        self.prefix = ''
        self.templates = [ "comm/slpxres.c", "comm/slpxres.h" ]
        self.ports = []
        self.has_shutdown = True

    def addconfig(self, jmap, board):
        p = SLPX()
        p.reference = jmap['name']
        p.port = jmap['port']
        self.ports.append(p)
        if "slpxres.h" not in board.hal.resheaders:
            board.hal.resheaders.append("slpxres.h")
        if "slpxres.c" not in board.hal.resources:
            board.hal.resources.append("slpxres.c")


