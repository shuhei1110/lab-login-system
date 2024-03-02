import os
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = '1907f7fa7a2a4fafb0bc56044edaabc6'

PAGE_ID_DIR = {'01':'e0e19dea51ff4146a7aacf43273ba28f',
                '02':'299a4bcf86194af1a91d89eaba6a1b23',
                '03':'a26173f755e44a4e93d0011b4c173ad5'}

# url = 'https://api.notion.com/v1/pages'
# url = 'https://api.notion.com/v1/databases/' + DATABASE_ID + '/query'
url_head = 'https://api.notion.com/v1/pages/'

headers =  {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer ' + NOTION_API_KEY,
    'Content-Type': 'application/json',
}

change_page_list = ["01", "02", "03"]

for user_id in change_page_list:
    print("start: " + user_id)
    url = url_head + PAGE_ID_DIR[user_id]

    login_status = '入室'

    json_data = {
        'properties': {
            'status': {
                'select': {
                    'name': login_status
                }
            }
        }
    }
    response = requests.patch(url, headers=headers, json=json_data)
    print(response)



# response = requests.post(url, headers=headers, json=json_data)



# _json_data = {
#     'parent': { 'database_id': DATABASE_ID },
#     'properties': {
#         'name': {
#             'title': [
#                         {
#                             'text': {
#                                 'content': 'Pythonで追加'
#                             }
#                         }
#                     ]  
#                 },
# 		'status': {
#             'select':{
#                 'name': '退室'
#                 }
#                 },
#     },
# }

# _json_data = {
#     'filter': {
#         'property': 'status',
#         'select': {
#             'equals': '退室'
#         }
#     }
# }
