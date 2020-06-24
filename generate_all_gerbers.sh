#!/usr/bin/env bash

for pcb in $(find . -name "*.kicad_pcb"); do
  ./scripts/generate_gerber.py "${pcb}"
done

for zip in $(find . -mindepth 2 -name "*.zip"); do
  mv "${zip}" .
done
