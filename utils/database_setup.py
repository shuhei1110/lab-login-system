"""Setup system

    ToDo: 
        - python setup.py

    説明:
        - データベースの作成

"""

import os
import sqlite3

def main():
    db_path = os.environ.get("LLS_PATH") + "/db/user_database.db"
    conn = sqlite3.connect(db_path)
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_table (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            status TEXT CHECK(status IN ('in', 'out')),
            day DATE,
            time TIME,
            FOREIGN KEY (user_id) REFERENCES user_table(id)
        )
    ''')

    conn.commit()

    conn.close()

if __name__ == "__main__":
    main()
