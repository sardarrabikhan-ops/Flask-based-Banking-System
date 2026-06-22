# constants.py

from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    BLOCKED = "blocked"

class AccountType(Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    BUSINESS = "business"

class TransactionType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"


CURRENT_ACCOUNT_ID = "current_account_id"
CUSTOMER_ID = "customer_id"
FULL_NAME = "fullname"