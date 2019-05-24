#!/usr/bin/env bash

cat $0

## To connect:
# arm-none-eabi-gdb --eval-command="target remote ip:3333"

## To flash:
# arm-none-eabi-gdb \
#   -ex="target remote 192.168.4.1:3333" \
#   -ex "load 500.elf" \
#   -ex "monitor reset" \
#   -ex "set confirm off" \
#   -ex "quit"

# To debug:
# arm-none-eabi-gdb \
#   -ex="target remote 192.168.4.1:3333" \
#   -ex "monitor reset halt" \
#   -ex "set confirm off" 500.elf
