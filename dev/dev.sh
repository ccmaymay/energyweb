#!/bin/bash


# Convenience script:  Starts, stops, or restarts all fake Rhizome 
# servers and all monitors (assuming sensor IDs are 1, 2, ..., 13).
# Expects the command (start, stop, restart) as an argument.


for i in {1..13} ; do
    bin/energymon $i "$1"
    bin/energyfaker $i "$1"
done
