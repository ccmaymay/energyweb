#!/bin/bash


# Convenience script:  Starts, stops, or restarts all fake Rhizome 
# servers and all monitors (assuming sensor IDs are 1, 2, ..., 13).
# Expects the command (start, stop, restart) as an argument.


USAGE_STR="Usage: $0 init|start|stop|restart"


function echo_and_do {
    echo "$1 ..."
    $1
}

if [ $# -ne 1 ] ; then
    echo $USAGE_STR
    exit 1
elif [ "$1" != "init" ] && [ "$1" != "start" ] && [ "$1" != "stop" ] && [ "$1" != "restart" ] ; then
    echo $USAGE_STR
    exit 1
fi

if [ "$1" == "init" ] ; then
    echo_and_do "dropdb energy" \
        && echo_and_do "createdb energy" \
        && echo_and_do "python manage.py syncdb" \
        && echo_and_do "python manage.py develdb"
else
    for i in {1..13} ; do
        echo_and_do "python manage.py energymon $i $1"
        echo_and_do "python manage.py energyfaker $i $1"
    done
fi
