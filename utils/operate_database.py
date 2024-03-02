import os
import argparse
import sqlite3

parser = argparse.ArgumentParser(description='データベースの操作を行うファイル')
db_path = os.environ.get("LLS_PATH") + "db/user_database.db"

def create_data(name, bd_addr, notion_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO user_table (name, bd_addr, notion_page_id) VALUES (?, ?, ?)', (name, bd_addr, notion_id))

    conn.commit()
    conn.close()

def read_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM user_table')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

def delete_data(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM user_table WHERE id = ?', (id,))

    conn.commit()
    conn.close()

def search_notion_page_id(bd_addr:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT notion_page_id FROM user_table WHERE bd_addr = ?", (bd_addr,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None


def update_data(id, new_name, new_bd_addr, new_notion_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE user_table
        SET name = ?, bd_addr = ?, notion_page_id = ?
        WHERE id = ?
    ''', (new_name, new_bd_addr, new_notion_id, id))

    conn.commit()
    conn.close()



def main():
    parser = argparse.ArgumentParser(description='データベースのCRUD操作スクリプト')
    parser.add_argument('operation', choices=['create', 'read', 'update', 'delete'], help='操作の種類')

    args = parser.parse_args()

    if args.operation == 'create':
        name = input('名前: ')
        bd_addr = input('BD_ADDR: ')
        notion_id = input('Notion Page ID: ')
        create_data(name, bd_addr, notion_id)
    elif args.operation == 'read':
        read_data()
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


