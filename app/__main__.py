import subprocess
from datetime import datetime

from utils import notion_api_ctl
from config import config

def print_datetime(f):
    """実行時間を出力するためのデコレーター

        Args:
            f(): 実行する関数

        Notes:
            - 別に必要ない
            - ロガーのデコレーターを作った時に必要なので作った

    """
    def wrapper(*args, **kwargs):
        print(f'\033[34m--- Start process: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---\033[0m')
        f(*args, **kwargs)
        print(f'\033[34m--- End process: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---\033[0m')
    return wrapper

@print_datetime
def main():
    """BDアドレススキャン

        Notes:
            - bluetoothctlのコマンドはバージョンによって多少異なるので注意

    """
    APP_PATH = config.APP_PATH

    current_date = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    log_date = datetime.now().strftime('%Y%m%d')

    log_file_path = APP_PATH + "/logs/" + log_date + ".log"

    with open(log_file_path, 'a') as log_file:
        log_file.write(current_date)

    command_output = subprocess.check_output(['bluetoothctl', 'devices', 'Paired']).decode('utf-8')
    devices = [line.split()[1] for line in command_output.splitlines() if 'Device' in line]

    for device in devices:

        try:
            result = subprocess.run(['sudo', 'l2ping', '-c', '1', '-t', '5', device], check=True, capture_output=True)
            stdout_txt = result.stdout.decode('utf-8')

            if "received" in stdout_txt:
                print(f'{device}を検出')
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f', {device}')

            else:
                print(f'{device}検出不可')
            
        except subprocess.CalledProcessError as e:
            print(f'{device}検出不可')

    with open(f'{APP_PATH}/logs/{log_date}.log', 'a') as log_file:
        log_file.write('\n')

    notion_api_ctl.notion_api()

if __name__ == "__main__":
    main()