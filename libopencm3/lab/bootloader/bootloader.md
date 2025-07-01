# The bootloader calling demo program

The firmware accepts two commands: RESET and BOOTLOADER. Both are quite identic, but the BOOTLOADER sets 1 in the backup register.
During the reset if the firmware sees the 1 in the backup register it jumps to bootloader.

## Control programs

### resetcc

It runs in the interactive mode and demonstrates both simple rebooting and rebooting in the bootloader mode

### bootloader

It runs in the command mode and demonstrates rebooting in bootloader mode and presenting bootloader version.

### read

It reads flash data from the MCU by serial port **without** pressing BOOT0 button on the board.

