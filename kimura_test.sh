#!/bin/bash

function paired_devices() {
  {
    printf "paired-devices\n\n"
  } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}

function is_connected() {
    {
        printf "connect $line\n\n"
    } | bluetoothctl | grep "Connected: "
}

paired_devices | while read line
do
    echo $line
    is_connected
done