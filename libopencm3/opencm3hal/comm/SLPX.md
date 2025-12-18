# Serial Line Packet xEchange protocol

The **SLPX** protocol is based on SLIP and contains no routing and addressing information. There are no sessions, only datagrams.

There are special values:
```
#define SLPX_START      0xF0
#define SLPX_ESCAPE     0xF1
#define SLPX_ESC_START  0xF2
#define SLPX_ESC_ESC    0xF3

```

The receiver should wait for the 0xF0 byte for synchronization. Then goes the packet byte by byte in the "escaped" format.
If a data byte is the same code as SLPX_START byte, a two byte sequence of SLPX_ESCAPE and SLPX_ESC_START is sent. If a data
byte is the same code as SLPX_ESCAPE byte, a two byte sequence of SLPX_ESCAPE and SLPX_ESC_ESC is sent. The receiver should
strip the escaped bytes back: if a receiver encounters SLPX_ESCAPE, it should decode SLPX_ESC_START to SLPX_START and SLPX_ESC_ESC
to SLPX_ESCAPE. In case of an other value received, the receiver should indicate error and wait for a next packet.

The packet has the following format:

|Byte number|Size|Comments|
|---|---|---|
|0|1|Start byte for synchronization (0xF0)|
|1|2|Payload function ID (little endian)|
|3|2|Payload size N (little endian)|
|5|N|Data|
|5+N|1|XOR CRC - complement to 0XFF|

Total size of a packet is 6+N, Function ID, Size, Data and CRC should be 0xFF while continously XORed (Full packet except of the heading 0xF0 byte).

The Function ID has predefined values for common functions. Other project-specific functions could be any. It is assumed that
this serial protocol connects host and MCU. A host is more flexible and could serve many MCUs with different Function ID schemes and versions.
A MCU is straightforward and could not adapt to another version.

The list of predefined Function ID (lower byte comes first):

|Function ID|Name|Size|Comments|
|---|---|---|---|
|0x0001|Information|-|**Information functions**|
|0x0101|Version|16|Firmware UUID little endian|
|0x0201|Ready|0|The firmware just started in a normal mode|
|0x0301|Bootloader|0|The firmware restarted and is preparing to enter bootloader mode|
|0x0401|Shutdown|0|The firmware is going to poweroff|
|0x0002|Telemetry|-|**Telemetry functions**|
|0x0102|Open|0|The serial channel starts communication|
|0x0202|Close|0|The serial channel stops communication|
|0x0302|Message|N|The string messages without ending zero|
|0x0402|Heart Beat|4|4-byte integer with steady increments|
|0x0003|Command|-|**Command functions**|
|0x0103|Reboot|0|Rebbot MCU|
|0x0203|Bootloader|0|Switch to a bootloader mode (maybe via reboot)|


