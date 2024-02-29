#!/bin/bash

function paired_devices() {
    {
    printf "paired-devices\n\n"
    } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}

paired_devices | while read line
timeout=5
do
    echo $line
    output=$((bluetoothctl connect $line | grep "yes") & sleep $timeout; kill $! 2>/dev/null)
    echo $?
    discon_log=$(bluetoothctl disconnect $line)
done