import time

SBUP_START = 0x7F
SBUP_ACK = 0x79

class SBUP:
    def __init__(self, channel):
        self.channel = channel

    def check_ack(self):
        if self.channel.read_byte() != SBUP_ACK:
            return False
        return True

    def start(self):
        for i in range(3):
            time.sleep(0.5)
            self.channel.send_byte(SBUP_START)
            if self.channel.rx_waiting_bytes() > 0:
                if self.check_ack():
                    return True
        return False

    def close(self):
        pass

def open(channel):
    return SBUP(channel)
