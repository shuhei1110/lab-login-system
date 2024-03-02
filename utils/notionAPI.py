"""notionAPI


"""

import os
import requests
from datetime import datetime

import log_file_ctl
import operate_database

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = '1907f7fa7a2a4fafb0bc56044edaabc6'
                
url_head = 'https://api.notion.com/v1/pages/'

headers =  {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer ' + NOTION_API_KEY,
    'Content-Type': 'application/json',
}

log_path = os.environ.get("LLS_PATH") + "logs/" + datetime.now().strftime('%Y%m%d') + ".log"
check_bool, *addresses = log_file_ctl.show_addresses(log_path)
print(addresses)

def create_json_data(entered:bool):
    if entered:
        login_status = '入室'
    else:
        login_status = '退室'
    json_data = {
        'properties': {
            'status': {
                'select': {
                    'name': login_status
                }
            }
        }
    }

    return json_data

if check_bool:

    if addresses[0]:
        json_data = create_json_data(True)

        for bd_addr in addresses[0]:
            print("start: " + bd_addr)
            notion_page_id = operate_database.search_notion_page_id(bd_addr)
            if notion_page_id:
                url = url_head + str(notion_page_id)
                response = requests.patch(url, headers=headers, json=json_data)
                print(response)
            else:
                print("nn")

    else:
        print("add[0]")

    if addresses[1]:
        json_data = create_json_data(False)

        for bd_addr in addresses[1]:
            print("start: " + bd_addr)
            notion_page_id = operate_database.search_notion_page_id(bd_addr)
            if notion_page_id:
                url = url_head + str(notion_page_id)
                response = requests.patch(url, headers=headers, json=json_data)
                print(response)
    else:
        print("add[1]")

else:
    print("false")