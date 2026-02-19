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
