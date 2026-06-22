#repositories/account_repo.py

from app.models import Account
from constants import AccountType

def create_account(conn, customer_id, account_type=AccountType.SAVINGS.value):
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO accounts (customer_id, account_type) 
        VALUES (?, ?)
    ''', (customer_id, account_type))
    
    account_id = cursor.lastrowid
    row = cursor.execute('SELECT * FROM accounts WHERE account_id = ?', (account_id,)).fetchone()
    
    return Account.from_row(row) if row else None


def change_account_status(conn, account_id, account_state):
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE accounts
        SET status = ?
        WHERE account_id = ?
    ''', (account_state, account_id))
    
    row = cursor.execute('SELECT * FROM accounts WHERE account_id = ?', (account_id,)).fetchone()
    
    return Account.from_row(row) if row else None

def get_account_by_account_id(conn, account_id):
    cursor = conn.cursor()

    row = cursor.execute('SELECT * FROM accounts WHERE account_id = ?', (account_id,)).fetchone()
    
    return Account.from_row(row) if row else None


def get_accounts_by_customer_id(conn, customer_id):
    cursor = conn.cursor()

    rows = cursor.execute('SELECT * FROM accounts WHERE customer_id = ?', (customer_id,)).fetchall()
    
    accounts = [Account.from_row(row) for row in rows]
    
    return accounts if accounts else []

def get_balance(conn, account_id):
    cursor = conn.cursor()

    row = cursor.execute('SELECT balance FROM accounts WHERE account_id = ?', (account_id,)).fetchone()
    
    return row["balance"] if row else None