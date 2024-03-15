"""settings
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
    """

        Args:
            ():

        Responses
            (): 

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