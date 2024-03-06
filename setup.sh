#!/bin/bash

# インストールするパッケージの名前
package_names=("bluetooth" "bluez" "libbluetooth-dev" "libudev-dev" "pulseaudio-module-bluetooth")

# 未インストールのパッケージのリスト
to_install=()

# パッケージごとに確認
for package_name in "${package_names[@]}"; do
    # パッケージがすでにインストールされているかを確認
    if ! dpkg -l | grep -q "^ii  $package_name "; then
        # インストールがされていない場合はリストに追加
        to_install+=("$package_name")
    else
        echo "Package $package_name is already installed."
    fi
done

# 未インストールのパッケージがある場合にのみインストール
if [ ${#to_install[@]} -gt 0 ]; then
    sudo apt-get install "${to_install[@]}"
fi


export LLS_PATH=$(pwd)

crontab -l > mycron 2>/dev/null
echo "LANG=ja_JP.UTF-8" >> mycron
echo "PATH=$PATH" >> mycron
echo "*/1 * * * * /usr/bin/python $LLS_PATH/scan.sh" >> mycron
crontab mycron
rm mycron

sudo systemctl restart cron
