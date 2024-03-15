"""notionAPI


"""

import requests
from datetime import datetime

from utils import log_file_ctl
from utils import database_ctl
from config import settings, config

DATABASE_ID = config.DATABASE_ID
API_URL = settings.API_URL
headers = settings.headers

log_path = config.APP_PATH + "/logs/" + datetime.now().strftime('%Y%m%d') + ".log"

time_threshold = config.time_threshold

def load_json_data(entered:bool, query:bool=False) -> dict:
    """config/settings.pyからHTTPリクエスト用のJSONをロード

        Args:
            entered(bool): 入室or退室
            query(bool): ページIDを取得

        Responses
            settings.json_data_in_filter(dict): 入室になっているユーザーのIDを取得
            settings.json_data_in(dict): 入室に変更
            settings.json_data_out_filter(dict): 退室になっているユーザーのIDを取得
            settings.json_data_out(dict): 退室に変更

        Notes:

    """
    if entered:
        if query:
            return settings.json_data_in_filter
        else:
            return settings.json_data_in
    else:
        if query:
            return settings.json_data_out_filter
        else:
            return settings.json_data_out


def get_page_ids(entered:bool) -> list:
    """Notionの各ページIDを取得する

        Args:
            ennterd(bool): Trueなら入室しているページID,Falseなら退室しているページID

        Responses
            page_ids(list): ページIDのリスト 

        Notes:

    """
    url = API_URL + 'databases/' + DATABASE_ID + '/query'
    json_data = load_json_data(entered=entered, query=True)
    response = requests.post(url, headers=headers, json=json_data)
    page_ids = [result['id'] for result in response.json()['results']]
    print("NotionPageIDを取得")
    return page_ids

def change_status(notion_page_id:str, entered:bool) -> dict:
    """ページのステータス（入退室）を変更する

        Args:
            notion_page_id(str): ページID
            entered(bool): Trueで入室,Falseで退室

        Responses
            response(dict): HTTPステータスコード 

        Notes:

    """
    json_data = load_json_data(entered)
    url = API_URL + "pages/" + str(notion_page_id)
    response = requests.patch(url, headers=headers, json=json_data)
    
    return response

def change_point(notion_page_id:str, point:int) -> dict:
    """各ページの朝活ポイントを変更する

        Args:
            notion_page_id(str): ページID
            point(int): 変更後の朝活ポイント

        Responses
            response(dict): HTTPステータスコード 

        Notes:

    """
    json_data = settings.make_json_data_point(point=point)
    url = API_URL + "pages/" + str(notion_page_id)
    response = requests.patch(url, headers=headers, json=json_data)
    
    return response

def reset_status():
    """ステータスをすべて退室にする

        Notes:

    """
    page_ids = get_page_ids(entered=True)
    for page_id in page_ids:
        response = change_status(notion_page_id=page_id, entered=False)

def notion_api():
    """logファイルを参照して入退室とポイントを変更するためにAPIを叩きに行く

        Notes:

    """
    addresses = log_file_ctl.analyze_log(log_path)
    if addresses[0] != None:
        for bd_addr in addresses[0]:
            print("change status: " + bd_addr)
            notion_page_id = database_ctl.search_notion_page_id(bd_addr)
            if notion_page_id:
                response = change_status(notion_page_id=notion_page_id, entered=True)
                database_ctl.create_activity_table(bd_addr=bd_addr, status='in')
                print("入室記録完了")

                user_id = database_ctl.search_user_id(bd_addr=bd_addr)
                result = database_ctl.check_asakatu(user_id=user_id)
                if result == 1:
                    exists = database_ctl.check_activity_exists(user_id=user_id, time_threshold=time_threshold)
                    if exists == 0:
                        point = database_ctl.update_asakatu_point(user_id=user_id)
                        change_point(notion_page_id=notion_page_id, point=point)
                
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
                database_ctl.create_activity_table(bd_addr=bd_addr, status='out')
                print("退室記録完了")
            else:
                print("データベースにユーザーが登録されていません")
    else:
        print("新しく退室したユーザーはいません")

def main():
    notion_api()

if __name__ == "__main__":
    main()
