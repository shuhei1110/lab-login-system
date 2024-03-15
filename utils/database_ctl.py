"""database control
"""
import argparse
import sqlite3

from datetime import datetime
from config import config

db_path = config.APP_PATH + "/db/user_database.db"

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

def search_user_id(bd_addr:str) -> str:
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

    if result:
        return result[0]
    else:
        return None

def check_asakatu(user_id:str) -> str:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    week = datetime.now().strftime('%a').lower()

    cursor.execute("SELECT {} FROM asakatu_table WHERE user_id = ?".format(week), (user_id,))
    result = cursor.fetchone()

    if result:
        return result[0]
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

def create_asataku_data(user_id:str, sun:str, mon:str, tue:str, wed:str, thu:str, fri:str, sat:str, point:int):
    """

        Args:
            ():

        Responses
            (): 

        Notes:
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO asakatu_table (user_id, sun, mon, tue, wed, thu, fri, sat, point) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, sun, mon, tue, wed, thu, fri, sat, point))

    conn.commit()
    conn.close()

def update_asakatu_data(user_id:str, sun:str, mon:str, tue:str, wed:str, thu:str, fri:str, sat:str, point:int):
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
        UPDATE asakatu_table
        SET sun = ?, mon = ?, tue = ?, wed = ?, thu = ?, fri = ?, sat = ?, point = ?,
        WHERE user_id = ?
    ''', (sun, mon, tue, wed, thu, fri, sat, point, user_id))

    conn.commit()
    conn.close()

def delete_asakatu_data(user_id:str):
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM asakatu_table WHERE user_id = ?', (user_id,))

    conn.commit()
    conn.close()

def check_activity_exists(user_id:str, time_threshold:str):
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    _day = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT EXISTS(SELECT * FROM activity_table WHERE user_id = ? AND day = ? AND time >= ?)", (user_id, _day, time_threshold))
    exists = cursor.fetchone()[0]
    conn.close()

    return exists

def check_input(prompt:str):
    while True:
        user_input = input(prompt)
        if user_input in {"0", "1"}:
            return user_input
        print("0か1で入力してください")

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
        table = input('選択するTable: ')
        if table == "user_table":
            name = input('名前: ')
            bd_addr = input('BD_ADDR: ')
            notion_id = input('Notion Page ID: ')
            create_data(name, bd_addr, notion_id)
        elif table == "asakatu_table":
            user_id = input("ユーザーID: ")
            sun = check_input("日曜日: ")
            mon = check_input("月曜日: ")
            tue = check_input("火曜日: ")
            wed = check_input("水曜日: ")
            thu = check_input("木曜日: ")
            fri = check_input("金曜日: ")
            sat = check_input("土曜日: ")
            point = int(input("朝活ポイント: "))
            create_asataku_data(user_id, sun, mon, tue, wed, thu, fri, sat, point)
        else:
            print("存在するTableを指定してください")
    elif args.operation == 'read':
        table = input('選択するTable: ')
        read_data(table=table)
    elif args.operation == 'update':
        table = input('選択するTable: ')
        if table == "user_table":
            id_to_update = input('更新するデータのID: ')
            new_name = input('新しい名前: ')
            new_bd_addr = input('新しいBD_ADDR: ')
            new_notion_id = input('新しいNotion Page ID: ')
            update_data(id_to_update, new_name, new_bd_addr, new_notion_id)
        elif table == "asakatu_table":
            id_to_update = input('更新するユーザーのID: ')
            sun = check_input("日曜日: ")
            mon = check_input("月曜日: ")
            tue = check_input("火曜日: ")
            wed = check_input("水曜日: ")
            thu = check_input("木曜日: ")
            fri = check_input("金曜日: ")
            sat = check_input("土曜日: ")
        else:
            print("存在するTableを指定してください")
    elif args.operation == 'delete':
        table = input('選択するTable: ')
        if table == "user_table":
            id_to_delete = input('削除するデータのID: ')
            delete_data(id_to_delete)
        elif table == "asakatu_table":
            user_id = input("削除するユーザーID: ")
            delete_asakatu_data(user_id)
        else:
            print("存在するTableを指定してください")


if __name__ == "__main__":
    main()


