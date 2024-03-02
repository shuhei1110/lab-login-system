#!/bin/bash

function paired_devices() {
    {
    printf "paired-devices\n\n"
    } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}
timeout=10
paired_devices | while read line
do
    echo $line
    output=$(bluetoothctl connect $line & sleep $timeout; kill $! 2>/dev/null)
    time_flag=$?
    if [ $time_flag = 1 ]; then
        bluetoothctl disconnect > /dev/null
        bluetoothctl connect $line | grep "yes"
        grep_flag=$?
        if [ $grep_flag = 0 ]; then
            echo "Success!"
        else
            echo "Failure!"
        fi
    else
        echo "Time over!"
    fi
    bluetoothctl disconnect > /dev/null
done