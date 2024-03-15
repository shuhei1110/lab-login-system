"""settings

    - 変更しない設定
"""

from config import config

API_URL = 'https://api.notion.com/v1/'

headers =  {
        'Notion-Version': '2022-06-28',
        'Authorization': 'Bearer ' + config.NOTION_API_KEY,
        'Content-Type': 'application/json',
    }

json_data_in = {
    'properties': {
        'status': {
            'select': {
                'name': '入室'
            }
        }
    }
}

json_data_out = {
    'properties': {
        'status': {
            'select': {
                'name': '退室'
            }
        }
    }
}

json_data_in_filter = {
    'filter': {
        'property': 'status', 
            'select': {
                'equals': '入室'
            }
        }
    }

json_data_out_filter = {
    'filter': {
        'property': 'status', 
            'select': {
                'equals': '退室'
            }
        }
    }

def make_json_data_point(point:int) -> dict:
    """朝活ポイントを変更するためのJSONを作成

        Args:
            point(int): 新しい朝活ポイント

        Responses
            json_data(dict): HTTPリクエストを行うためのJSONデータ 

        Notes:

    """
    json_data = {
        'properties': {
            'point': {
                'number': point 
            }
        }
    }

    return json_data