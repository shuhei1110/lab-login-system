#!/bin/bash

function paired_devices() {
  {
    printf "paired-devices\n\n"
  } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}

paired_devices

#devices_stdout = $(paired-devices)
#echo "${devices_stdout}"

for item "${paired_devices}";do
    bluetoothctl connect "${item:7:24}" | grep "[CHG]" | 
    echo $?

    bluetoothctl disconnect "${item:7:24}"
    exit
    
