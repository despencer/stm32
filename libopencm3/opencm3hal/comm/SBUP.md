# STM32 Bootloader USART Protocol

After entering the bootloader mode before the communication starts the channel should be confirmed. The host sends `0x7F` and the MCU should respond
with acknowledge byte `0x79`.

During the bootloader sessions all data sent is ended with checksum byte: all bytes sent with the checksum byte should be sequentially XORed and final
result should be `0xFF`.

The usual device response is:

|Byte number|Size|Comments|
|---|---|---|
|0|1|Payload size - 1|
|1|N|Data|
|1+N|1|ACK (0x79)|

The payload size is 0 for one byte, 1 for two bytes, and up to 255 for 256 bytes.

# Commands

## 0x02: GetID

The host sends `0x02` with checksum (`0x02 0xFD`).

The devices replies with `ACK` followed by ID payload.


