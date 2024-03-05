import subprocess
from datetime import datetime

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
        subprocess.run(['bluetoothctl', '--timeout', '10', 'connect', device], check=True, capture_output=True)
        print("yes")
        # 接続成功時にログにデバイスを書き込み
        with open(f'{LLS_PATH}/logs/{log_date}.log', 'a') as log_file:
            log_file.write(f', {device}')
    except subprocess.CalledProcessError:
        print("Failure!")
    finally:
        # デバイスへの接続を解除
        subprocess.run(['bluetoothctl', 'disconnect'], check=True, capture_output=True)
