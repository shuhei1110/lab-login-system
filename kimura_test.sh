#!/bin/bash

bluetoothctl
echo "hello1"
devices_stdout = $(paired-device)
echo "hello2"
for item "${devices_stdout}";do
    connect_stdout = $(connect "${item:7:24}")
    if $?;do
        exit
    echo "hello3"
#    if [[${connect_stdout:0:5} == *[CHG]*]];then
#        curl
#        echo "hello4"
#    else
#        curl
#    
    disconnect "${item:7:24}"
    echo "hello4"