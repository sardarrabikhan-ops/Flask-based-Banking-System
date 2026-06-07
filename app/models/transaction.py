# models/transaction.py

class Transaction:
    def __init__(self, transaction_type, account_id, amount, balance_after=None, timestamp=None, transaction_id=None):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.account_id = account_id
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = timestamp
    
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        
        return cls(
            transaction_id=row["transaction_id"],
            transaction_type=row["transaction_type"],
            account_id=row["account_id"],
            amount=row["amount"],
            balance_after=row["balance_after"],
            timestamp=row["timestamp"]
        )