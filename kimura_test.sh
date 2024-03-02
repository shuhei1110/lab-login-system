#!/bin/bash

# ペアリングされているデバイスを標準出力
function paired_devices() {
    {
    printf "paired-devices\n\n"
    } | bluetoothctl | grep "Device " | sed -r 's/^.*(([0-9A-F]{2}:){5}[0-9A-F]{2}).*$/\1/'
}
# 時間をテキストに出力
current_date=$(date "+%Y-%m-%d %H:%M:%S")
echo -n $current_date >> log.txt
# 10秒以内に検知されなければTimeoutを標準出力
timeout=10
paired_devices | while read line
do
    echo $line
    output=$(bluetoothctl connect $line & sleep $timeout; kill $! 2>/dev/null)
    time_flag=$?
    if [ $time_flag = 1 ]; then
        bluetoothctl disconnect > /dev/null
        bluetoothctl connect $line | grep "yes" > /dev/null
        grep_flag=$?
        if [ $grep_flag = 0 ]; then
            echo -n ", ${line}" >> log.txt
            echo "Success!"
        else
            echo "Failure!"
        fi
    else
        echo "Time over!"
    fi
    bluetoothctl disconnect > /dev/null
done

echo "\n" >> log.txt