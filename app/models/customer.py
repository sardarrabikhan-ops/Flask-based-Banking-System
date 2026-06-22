#models/customer.py

from constants import Status

class Customer:
    def __init__(
            self, 
            firstname, 
            lastname, 
            email, 
            password_hash, 
            phone, 
            status=Status.ACTIVE.value,
            failed_attempts=0, 
            lock_until=None, 
            timestamp=None, 
            customer_id=None
            ):
        
        self.customer_id = customer_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.status = status
        self.timestamp = timestamp
        self.password_hash = password_hash
        self.failed_attempts = failed_attempts
        self.lock_until = lock_until
    
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        
        return cls(
            customer_id=row["customer_id"],
            firstname=row["first_name"],
            lastname=row["last_name"],
            email=row["email"],
            phone=row["phone"],
            password_hash=row["password"],
            failed_attempts=row["failed_attempts"],
            lock_until=row["lock_until"],
            timestamp=row["timestamp"],
            status=row["status"]
        )