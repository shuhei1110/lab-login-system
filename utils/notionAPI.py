"""notionAPI


"""

import os
import requests
from datetime import datetime

import log_file_ctl

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = '1907f7fa7a2a4fafb0bc56044edaabc6'

PAGE_ID_DIR = {'01':'e0e19dea51ff4146a7aacf43273ba28f',
                '02':'299a4bcf86194af1a91d89eaba6a1b23',
                '03':'a26173f755e44a4e93d0011b4c173ad5'}
                
url_head = 'https://api.notion.com/v1/pages/'

headers =  {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer ' + NOTION_API_KEY,
    'Content-Type': 'application/json',
}

log_path = os.environ.get("LLS_PATH") + "logs/" + datetime.now().strftime('%Y%m%d') + ".log"
check_bool, *addresses = log_file_ctl.show_addresses(log_path)

if check_bool:

    if addresses[0]:
        print("add[0] ture")
    else:
        print("add[0]")

    if addresses[1]:
        print("add[1] ture")
    else:
        print("add[1]")

    change_page_list = ["01", "02", "03"]

    # for user_id in change_page_list:
    #     print("start: " + user_id)
    #     url = url_head + PAGE_ID_DIR[user_id]

    #     login_status = '入室'

    #     json_data = {
    #         'properties': {
    #             'status': {
    #                 'select': {
    #                     'name': login_status
    #                 }
    #             }
    #         }
    #     }
        # response = requests.patch(url, headers=headers, json=json_data)
        # print(response)

else:
    print("false")