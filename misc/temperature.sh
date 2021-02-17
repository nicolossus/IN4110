#!/bin/bash

curl -s https://www.yr.no/place/Norway/Oslo/Oslo/Oslo/ | \
grep "temperature" | \
head -n 1 | \
cut -d"\"" -f4 | \
cowsay
