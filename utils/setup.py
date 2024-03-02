"""Setup system

    ToDo: 
        - python setup.py

    説明:
        - データベースの作成

"""

import sqlite3

def main():
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            bd_addr TEXT NOT NULL,
            notion_page_id TEXT NOT NULL
        )
    ''')

    conn.commit()

    conn.close()

if __name__ == "__main__":
    main()
