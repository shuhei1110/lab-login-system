#!/bin/bash

function paired_devices() {
    {
    printf "paired-devices\n\n"
    } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}

paired_devices | while read line
do
    echo $line
    con_log='bluetoothctl connect $line'
    echo ${con_log}
    bluetoothctl disconnect $line
done