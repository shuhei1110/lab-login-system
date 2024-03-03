"""database control
"""
import os
import argparse
import sqlite3
from datetime import datetime

db_path = os.environ.get("LLS_PATH") + "/db/user_database.db"

def create_data(name:str, bd_addr:str, notion_id:str):
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO user_table (name, bd_addr, notion_page_id) VALUES (?, ?, ?)', (name, bd_addr, notion_id))

    conn.commit()
    conn.close()

def read_data(table:str):
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM "{table}"')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

def delete_data(id:int):
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM user_table WHERE id = ?', (id,))

    conn.commit()
    conn.close()

def update_data(id, new_name, new_bd_addr, new_notion_id):
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE user_table
        SET name = ?, bd_addr = ?, notion_page_id = ?
        WHERE id = ?
    ''', (new_name, new_bd_addr, new_notion_id, id))

    conn.commit()
    conn.close()


def search_notion_page_id(bd_addr:str) -> str:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT notion_page_id FROM user_table WHERE bd_addr = ?", (bd_addr,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None

def search_all_bd_addr():
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT bd_addr FROM user_table")
    result = cursor.fetchall()

    if result:
        return result
    else:
        return None

def create_activity_table(bd_addr:str, status:str):
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """ 
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user_table WHERE bd_addr = ?", (bd_addr,))
    result = cursor.fetchone()
    user_id = result[0]

    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    cursor.execute('INSERT INTO activity_table (user_id, status, day, time) VALUES (?, ?, ?, ?)', (user_id, status, current_date, current_time))

    conn.commit()
    conn.close()

def main():
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    parser = argparse.ArgumentParser(description='データベースのCRUD操作スクリプト')
    parser.add_argument('operation', choices=['create', 'read', 'update', 'delete'], help='操作の種類')

    args = parser.parse_args()

    if args.operation == 'create':
        name = input('名前: ')
        bd_addr = input('BD_ADDR: ')
        notion_id = input('Notion Page ID: ')
        create_data(name, bd_addr, notion_id)
    elif args.operation == 'read':
        table = input('Table: ')
        read_data(table=table)
    elif args.operation == 'update':
        id_to_update = input('更新するデータのID: ')
        new_name = input('新しい名前: ')
        new_bd_addr = input('新しいBD_ADDR: ')
        new_notion_id = input('新しいNotion Page ID: ')
        update_data(id_to_update, new_name, new_bd_addr, new_notion_id)
    elif args.operation == 'delete':
        id_to_delete = input('削除するデータのID: ')
        delete_data(id_to_delete)


if __name__ == "__main__":
    main()


