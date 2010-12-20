#!/bin/bash

for i in {1..13} ; do
    bin/energyfaker $i "$1"
    sleep 1
    bin/energymon $i "$1"
done
