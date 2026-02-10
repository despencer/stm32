import time

SBUP_START = 0x7F
SBUP_ACK = 0x79
SBUP_CHECKSUM = 0xFF

SBUP_CMD_GET = 0x00
SBUP_CMD_GETID = 0x02

class SBUP:
    def __init__(self, channel):
        self.channel = channel

    def check_ack(self):
        if self.channel.read_byte() != SBUP_ACK:
            return False
        return True

    def start(self):
        for i in range(10):
            time.sleep(1)
            self.channel.send_byte(SBUP_START)
            for j in range(10):
                if self.channel.rx_waiting_bytes() > 0:
                    if self.check_ack():
                        return True
                time.sleep(0.2)
        return False

    def read_data(self):
        size = self.channel.read_byte() + 1
        data = self.channel.read(size)
        if self.check_ack():
            return data
        return None

    def send_command(self, cmdid):
        self.channel.send_byte(cmdid)
        self.channel.send_byte(cmdid ^ SBUP_CHECKSUM)
        return self.check_ack()

    def close(self):
        pass

def open(channel):
    return SBUP(channel)
