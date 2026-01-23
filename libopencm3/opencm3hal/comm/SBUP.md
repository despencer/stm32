# STM32 Bootloader USART Protocol

After entering the bootloader mode before the communication starts the channel should be confirmed. The host sends `0x7F` and the MCU should respond
with acknowledge byte `0x79`.


