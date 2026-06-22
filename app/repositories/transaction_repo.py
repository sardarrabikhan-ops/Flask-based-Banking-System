#repositories/transaction_repo.py

from app.models import Transaction
from constants import TransactionType

def create_transaction(conn, account_id, transaction_type, amount):
        cursor = conn.cursor()

        old_balance = cursor.execute('SELECT balance FROM accounts WHERE account_id = ?', (account_id,)).fetchone()["balance"]
        
        if transaction_type.lower() == TransactionType.DEBIT.value:
            balance_after = old_balance - amount
        elif transaction_type.lower() == TransactionType.CREDIT.value:
            balance_after = old_balance + amount
        else:
            raise ValueError("Invalid transaction type. Use 'Debit' or 'Credit'.")

        cursor.execute('''
            INSERT INTO transactions (account_id, transaction_type, amount, balance_after)
            VALUES (?, ?, ?, ?)
        ''', (account_id, transaction_type, amount, balance_after))
        
        transaction_id = cursor.lastrowid

        cursor.execute('''
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
        ''', (balance_after, account_id))
        
        row = cursor.execute('SELECT * FROM transactions WHERE transaction_id = ?', (transaction_id,)).fetchone()
        
        return Transaction.from_row(row)

def get_transaction_history(conn, account_id):
        cursor = conn.cursor()

        rows = cursor.execute('SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC', (account_id,)).fetchall()
        
        transactions = [Transaction.from_row(row) for row in rows]
        return transactions