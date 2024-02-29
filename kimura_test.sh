#!/bin/bash

function paired_devices() {
    {
    printf "paired-devices\n\n"
    } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}
timeout=5
paired_devices | while read line
do
    echo $line
    output=$(bluetoothctl connect $line & sleep $timeout; kill $! 2>/dev/null)
    if [ "$?" -eq 1 ]; then
        bluetoothctl disconnect
        bluetoothctl connect $line | grep "yes"
        if [ "$?" -eq 0 ]; then
            echo "Success!"
        else
            echo "Failure!"
        fi
    else
        echo "Time over!"
    fi
    bluetoothctl disconnect
done