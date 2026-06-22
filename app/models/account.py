#models/account.py

from constants import Status, AccountType

class Account:
    def __init__(
            self, 
            customer_id, 
            account_type=AccountType.SAVINGS.value, 
            status=Status.ACTIVE.value, 
            balance=0, 
            timestamp=None, 
            account_id=None
            ):
        
        self._customer_id = customer_id
        self._account_id = account_id
        self._account_type = account_type
        self._status = status
        self._balance = balance
        self.timestamp = timestamp
    
    def __str__(self):
        return f"""Account(
        customer_id={self._customer_id}, 
        account_id={self._account_id}, 
        account_type={self._account_type}, 
        status={self._status}, balance={self._balance}, 
        timestamp={self.timestamp}
        )"""
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def customer_id(self):
        return self._customer_id
    
    @property
    def account_id(self):
        return self._account_id

    @property
    def account_type(self):
        return self._account_type

    @property
    def status(self):
        return self._status
    
    def transfer_to(self, target_account, amount):
        self._balance -= amount
        target_account._balance += amount
    
    def deposit(self, amount):
        self._balance += amount
    
    def withdraw(self, amount):
        self._balance -= amount
    

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        
        return cls(
            customer_id=row["customer_id"],
            account_id=row["account_id"],
            account_type=row["account_type"],
            status=row["status"],
            balance=row["balance"],
            timestamp=row["timestamp"]
        )