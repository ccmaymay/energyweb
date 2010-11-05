#!/bin/sh

pkill energygraph
pkill energystats
#pkill energymon
sleep 0.2
./just_connect.py
sleep 0.2
#energymon &
energygraph &
energystats &
