import slpx
import sbup

def enter_bootloader(line):
    print('Sending request to reset to bootloader mode')
    line.send(slpx.SLPX_BOOTLOADER, b'')
    while True:
        msg = slpx.read(line)
        if msg.funcid == slpx.SLPX_SHUTDOWN:
            line.close()
            print('Jumping to bootloader mode')
            break
    bline = sbup.open(line.channel)
    if not bline.start():
        print('Bootloader mode rejected')
        return None
    print('Bootloader mode confirmed')
    if not bline.send_command(sbup.SBUP_CMD_GETID):
        print('Failed to execute Chip ID command')
        return None
    chipid = int.from_bytes(bline.read_data(), 'little')
    if chipid == None:
        print('Failed to get Chip ID data')
        return None
    print(f'Chip id {chipid:04X}')
    return bline

def read_chunk(bline, start, size):
    if not bline.send_command(sbup.SBUP_CMD_READMEMORY):
        print('Failed to execute Read Memory command')
        return None
    if not bline.send_data(start.to_bytes(4, 'big')):
        print(f'Failed to send address {start:08X} for read')
        return None
    if not bline.send_command(size-1):
        print(f'Failed to send size {size}')
        return None
    return bline.read(size)

def exit_bootloader(bline):
    data = read_chunk(bline, sbup.startpointer, 4)
    if data == None:
        return
    jumpaddress = int.from_bytes(data, 'little')
    print(f'Detected jump address {jumpaddress:08X}')
    if not bline.send_command(sbup.SBUP_CMD_GO):
        print('Failed to execute Go command')
        return
    if not bline.send_data(jumpaddress.to_bytes(4, 'big')):
        print('Failed to send jump address')
        return
    line = slpx.open(bline.channel)
    print('Waiting for app to start')
    while True:
        msg = slpx.read(line)
        if msg.funcid == slpx.SLPX_HEARTBEAT:
            break
    print('MCU is running in app mode')

