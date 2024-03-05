import os
import subprocess
from datetime import datetime

LLS_PATH = os.environ.get("LLS_PATH")

# 現在の日時を取得
current_date = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
log_date = datetime.now().strftime('%Y%m%d')

# ログファイルに日時を書き込み
with open(f'{LLS_PATH}/logs/{log_date}.log', 'a') as log_file:
    log_file.write(current_date)

# ペアリングされているデバイスを取得
def paired_devices():
    command_output = subprocess.check_output(['bluetoothctl', 'paired-devices']).decode('utf-8')
    devices = [line.split()[1] for line in command_output.splitlines() if 'Device' in line]
    return devices

# デバイスごとに処理
for device in paired_devices():
    print(device)

    # デバイスへの接続を試みる
    try:
        result = subprocess.run(['bluetoothctl', '--timeout', '10', 'connect', device], check=True, capture_output=True)
        stdout_txt = result.stdout.decode('utf-8')
        print(stdout_txt)
        #print(result.stderr.decode('utf-8'))

        if "yes" in stdout_txt:
            print("successful")
            # 接続成功時にログにデバイスを書き込み
            with open(f'{LLS_PATH}/logs/{log_date}.log', 'a') as log_file:
                log_file.write(f', {device}')
            
            subprocess.run(['bluetoothctl', 'disconnect'], check=True, capture_output=True)

        else:
            print("failed")
        
    except subprocess.CalledProcessError as e:
        print("error")
        print(e.stdout.decode('utf-8'))
        print(e.stderr.decode('utf-8'))

with open(f'{LLS_PATH}/logs/{log_date}.log', 'a') as log_file:
    log_file.write('\n')