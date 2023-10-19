In order to flash one has to hold Boot0 button and press Boot1 button for reset.
dfu-util -d 0483:df11 -a 0 -s 0x8000000 -D trafficlights.bin
