import subprocess
from datetime import datetime

from utils import notion_api_ctl
from config import config

def print_datetime(f):
    def wrapper(*args, **kwargs):
        print(f'--- Start process: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---')
        f(*args, **kwargs)
        print(f'--- End process: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---')
    return wrapper

@print_datetime
def main():
    APP_PATH = config.APP_PATH

    # 現在の日時を取得
    current_date = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    log_date = datetime.now().strftime('%Y%m%d')

    log_file_path = APP_PATH + "/logs/" + log_date + ".log"

    # ログファイルに日時を書き込み，ファイルがなければ作成
    with open(log_file_path, 'a') as log_file:
        log_file.write(current_date)

    # ペアリングされているデバイスを取得
    def paired_devices():
        command_output = subprocess.check_output(['bluetoothctl', 'devices', 'Paired']).decode('utf-8')
        devices = [line.split()[1] for line in command_output.splitlines() if 'Device' in line]
        return devices

    # デバイスごとに処理
    for device in paired_devices():

        # デバイスへの接続を試みる
        try:
            result = subprocess.run(['sudo', 'l2ping', '-c', '1', '-t', '5', device], check=True, capture_output=True)
            stdout_txt = result.stdout.decode('utf-8')
            # print(stdout_txt)

            if "received" in stdout_txt:
                print(f'{device}を検出')
                # 接続成功時にログにデバイスを書き込み
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f', {device}')

            else:
                print(f'{device}は検出不可')
            
        except subprocess.CalledProcessError as e:
            print(f'{device}検出不可')

    with open(f'{APP_PATH}/logs/{log_date}.log', 'a') as log_file:
        log_file.write('\n')

    notion_api_ctl.notion_api()

if __name__ == "__main__":
    main()