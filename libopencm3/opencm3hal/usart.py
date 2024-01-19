import port

class Usart:
    def __init__(self):
        self.reference = None

class Mapper:
    def __init__(self):
        self.name = 'usart'
        self.templates = [ "opencm3usart.c", "opencm3usart.h", "opencm3usartres.h", "opencm3output.h" ]
        self.usarts = []

    def addconfig(self, jmap, board):
        self.board = board
        u = Usart()
        u.reference = jmap['name']
        self.usarts.append(u)
        if "opencm3usartres.h" not in board.hal.resheaders:
            board.hal.resheaders.append("opencm3usartres.h")
        if "opencm3usart.c" not in board.hal.resources:
            board.hal.resources.append("opencm3usart.c")
