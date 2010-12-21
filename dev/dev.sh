#!/bin/bash


# Convenience script:  Starts, stops, or restarts all fake Rhizome 
# servers and all monitors (assuming sensor IDs are 1, 2, ..., 13).
# Expects the command (start, stop, restart) as an argument.


USAGE_STR="usage: $0 <start|stop|restart>"


if [ $# -ne 1 ] ; then
    echo $USAGE_STR
    exit 1
elif [ "$1" != "start" ] && [ "$1" != "stop" ] && [ "$1" != "restart" ] ; then
    echo $USAGE_STR
    exit 1
fi

for i in {1..13} ; do
    cmd="bin/energymon $i $1"
    $cmd
    echo $cmd
    cmd="bin/energyfaker $i $1"
    $cmd
    echo $cmd
done
