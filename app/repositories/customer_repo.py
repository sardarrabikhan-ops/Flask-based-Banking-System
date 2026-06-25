#repositories/customer_repo.py

from app.models import Customer
from app.models import Account
from app.models import Transaction
from app.utils.security import hash_password

def create_customer(conn, first_name, last_name, email, password, phone):
    cursor = conn.cursor()

    password_hash = hash_password(password)
    clean_email = email.strip().lower()
    clean_phone = phone.strip()

    cursor.execute('''
        INSERT INTO customers (first_name, last_name, email, password, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, clean_email, password_hash, clean_phone))
    
    customer_id = cursor.lastrowid
    row = cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    
    customer = Customer.from_row(row) if row else None
    
    return customer

def change_customer_status(conn, customer_id, customer_state):
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE customers
        SET status = ?
        WHERE customer_id = ?
    ''', (customer_state, customer_id))
    
    
    row = cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    
    return Customer.from_row(row)

def get_customer_by_email(conn, email):
    cursor = conn.cursor()

    clean_email = email.strip().lower()
    
    row = cursor.execute('SELECT * FROM customers WHERE email = ?', (clean_email,)).fetchone()
    
    return Customer.from_row(row)

def get_customer_by_customer_id(conn, customer_id):
    cursor = conn.cursor()
    
    row = cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    
    return Customer.from_row(row)

def email_exists(conn, email):
    cursor = conn.cursor()
    
    clean_email = email.strip().lower()
    row = cursor.execute('SELECT * FROM customers WHERE email = ?', (clean_email,)).fetchone()
    
    return row is not None

def phone_exists(conn, phone):
    cursor = conn.cursor()
    
    clean_phone = phone.strip()
    row = cursor.execute('SELECT * FROM customers WHERE phone = ?', (clean_phone,)).fetchone()
    
    return row is not None

def update_failed_attempts(conn, customer_id, failed_attempts):
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE customers
        SET failed_attempts = failed_attempts + ?
        WHERE customer_id = ?
    ''', (failed_attempts, customer_id))
    
    row = cursor.execute('SELECT failed_attempts FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    
    return row["failed_attempts"] if row else None

def update_lock_until(conn, customer_id, lock_until):
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE customers
        SET lock_until = ?
        WHERE customer_id = ?
    ''', (lock_until, customer_id))
    
    row = cursor.execute('SELECT lock_until FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    
    return row["lock_until"] if row else None

def reset_failed_attempts_and_lock_until(conn, customer_id):
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE customers
        SET failed_attempts = 0, lock_until = NULL
        WHERE customer_id = ?
    ''', (customer_id,))
    
    row = cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    
    return Customer.from_row(row) if row else None

def profile_info(conn, customer_id):
    cursor = conn.cursor()

    row1 = cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()

    customer = Customer.from_row(row1) if row1 else None

    row2 = cursor.execute("SELECT * FROM accounts WHERE customer_id = ?", (customer_id,)).fetchall()

    accounts = [Account.from_row(row) for row in row2]

    row3 = cursor.execute('''
        SELECT *
        FROM transactions t
        JOIN accounts a ON t.account_id = a.account_id
        WHERE a.customer_id = ?
        ORDER BY t.transaction_id DESC
        LIMIT 5
    ''', (customer_id,)).fetchall()

    transactions = [Transaction.from_row(row) for row in row3]

    return {
        "customer": customer,
        "accounts": accounts,
        "transactions": transactions
    }