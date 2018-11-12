#!/bin/bash

for pcb in $(find . -name "*.kicad_pcb"); do
  ./scripts/generate_gerber.py "${pcb}"
done

for zip in $(find . -name "*.zip"); do
  mv "${zip}" .
done
