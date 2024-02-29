#!/bin/bash

function paired_devices() {
  {
    printf "paired-devices\n\n"
  } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}

paired_devices
device_list=(${paired_devices//\n/ })
#devices_stdout = $(paired-devices)
#echo "${devices_stdout}"

for item in "${paired_devices}";do
    echo "${item}"
    done