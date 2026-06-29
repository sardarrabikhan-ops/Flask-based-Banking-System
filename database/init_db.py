#database/init_db.py

import os
from .connection import get_db_connection

def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        failed_attempts INTEGER DEFAULT 0,
        lock_until INTEGER,
        timestamp INTEGER NOT NULL DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
        status TEXT NOT NULL DEFAULT 'active'
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        account_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        balance Decimal DEFAULT 0.0,
        timestamp INTEGER NOT NULL DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
        
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL,
        balance_after REAL NOT NULL,
        timestamp INTEGER NOT NULL DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
        
        FOREIGN KEY (account_id)
        REFERENCES accounts (account_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
    )
    ''')

    conn.commit()

    conn.close()