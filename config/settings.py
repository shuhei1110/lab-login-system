"""settings
"""

import os

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = '1907f7fa7a2a4fafb0bc56044edaabc6'
API_URL = 'https://api.notion.com/v1/'

headers =  {
        'Notion-Version': '2022-06-28',
        'Authorization': 'Bearer ' + NOTION_API_KEY,
        'Content-Type': 'application/json',
    }

json_data_entered = {
    'properties': {
        'status': {
            'select': {
                'name': '入室'
            }
        }
    }
}

json_data_notentered = {
    'properties': {
        'status': {
            'select': {
                'name': '退室'
            }
        }
    }
}

json_data_entered_filter = {
    'filter': {
        'property': 'status', 
            'select': {
                'equals': '入室'
            }
        }
    }

json_data_notentered_filter = {
    'filter': {
        'property': 'status', 
            'select': {
                'equals': '退室'
            }
        }
    }
