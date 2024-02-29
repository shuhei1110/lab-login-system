#!/bin/bash

function paired_devices() {
  {
    printf "paired-devices\n\n"
  } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}

function is_connected(){
    {
        printf "connect $line"
    } | bluetoothctl | grep "Connected: "
}

paired_devices | while read line
do
    echo $line
    echo $is_connected
done