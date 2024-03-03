#!/bin/bash

sudo apt -y install bluetooth bluez

export LLS_PATH=$(pwd)

crontab -l > mycron 2>/dev/null
echo "LANG=ja_JP.UTF-8" >> mycron
echo "PATH=$PATH" >> mycron
echo "*/10 * * * * $LLS_PATH/scan.sh" >> mycron
crontab mycron
rm mycron

sudo systemctl restart cron