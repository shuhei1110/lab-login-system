#!/bin/bash

bluetoothctl

devices_stdout = $(paired-devices)
echo "${devices_stdout}"

#for item "${devices_stdout}";do
#    connect_stdout = $(connect "${item:7:24}")
#    if $?;do
#        exit
    
#    if [[${connect_stdout:0:5} == *[CHG]*]];then
#        curl
#        echo "hello4"
#    else
#        curl
#    
#    disconnect "${item:7:24}"
    exit
    