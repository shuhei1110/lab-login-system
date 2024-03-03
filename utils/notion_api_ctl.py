"""notionAPI


"""

import os
import requests
from datetime import datetime

import log_file_ctl
import database_ctl
from config import settings

DATABASE_ID = settings.DATABASE_ID
API_URL = settings.API_URL
headers = settings.headers

log_path = os.environ.get("LLS_PATH") + "logs/" + datetime.now().strftime('%Y%m%d') + ".log"
check_bool, *addresses = log_file_ctl.analyze_log(log_path)

def print_datetime(f):
    def wrapper(*args, **kwargs):
        print(f'Start process: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        f(*args, **kwargs)
        print(f'End process: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    return wrapper

def load_json_data(entered:bool, query:bool=False) -> dict:
    """config/settings.pyからHTTPリクエスト用のJSONをロード

        Args:
            entered(bool): 入室or退室
            query(bool): ページIDを取得

        Responses
            settings.json_data_entered_filter(dict): 入室になっているユーザーのIDを取得
            settings.json_data_entered(dict): 入室に変更
            settings.json_data_notentered_filter(dict): 退室になっているユーザーのIDを取得
            settings.json_data_notentered(dict): 退室に変更

        Notes:

    """
    if entered:
        if query:
            return settings.json_data_entered_filter
        else:
            return settings.json_data_entered
    else:
        if query:
            return settings.json_data_notentered_filter
        else:
            return settings.json_data_notentered


def get_page_ids(entered:bool) -> list:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    url = API_URL + 'databases/' + DATABASE_ID + '/query'
    json_data = load_json_data(entered=entered, query=True)
    response = requests.post(url, headers=headers, json=json_data)
    page_ids = [result['id'] for result in response.json()['results']]
    print("NotionPageIDを取得")
    return page_ids

def change_status(notion_page_id:str, entered:bool) -> dict:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    json_data = load_json_data(entered)
    url = API_URL + "pages/" + str(notion_page_id)
    response = requests.patch(url, headers=headers, json=json_data)
    
    return response

def reset_status():
    page_ids = get_page_ids(entered=True)
    for page_id in page_ids:
        response = change_status(notion_page_id=page_id, entered=False)

@print_datetime
def main():
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    if check_bool:
        if addresses[0]:
            for bd_addr in addresses[0]:
                print("change status: " + bd_addr)
                notion_page_id = database_ctl.search_notion_page_id(bd_addr)
                if notion_page_id:
                    response = change_status(notion_page_id=notion_page_id, entered=True)
                    print("入室記録完了")
                else:
                    print("データベースにユーザーが登録されていません")
        else:
            print("新しく入室したユーザーはいません")

        if addresses[1]:
            for bd_addr in addresses[1]:
                print("change status: " + bd_addr)
                notion_page_id = database_ctl.search_notion_page_id(bd_addr)
                if notion_page_id:
                    response = change_status(notion_page_id=notion_page_id, entered=False)
                    print("退室記録完了")
                else:
                    print("データベースにユーザーが登録されていません")
        else:
            print("新しく退室したユーザーはいません")

    else:
        print("logファイルが正しくありません")

if __name__ == "__main__":
    main()