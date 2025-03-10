import sqlite3


DATABASE_NAME = "items.db"


def create_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id TEXT PRIMARY KEY,
            price REAL,
            link TEXT,
            account_balance REAL,
            last_activity TEXT
        )
    ''')
    conn.commit()
    conn.close()


def find_item(item_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE item_id = ?', (item_id,))
    existing_item = cursor.fetchone()
    conn.close()
    return existing_item

def add_item(item_id, price, link, account_balance, last_activity):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (item_id, price, link, account_balance, last_activity)
        VALUES (?, ?, ?, ?, ?)
    ''', (item_id, price, link, account_balance, last_activity))
    conn.commit()
    conn.close()