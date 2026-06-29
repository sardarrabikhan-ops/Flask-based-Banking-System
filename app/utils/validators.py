#utils/validators.py

import re

def valid_password(password):
    allowed = "!@#$%^&*()-_=+"

    if not 8 <= len(password) <= 18:
        return False, {"field": "password", "msg":"Password must be 8-18 characters long!"}
    if not any(c in allowed for c in password):
        return False, {"field": "password", "msg":"Password must include at least one special character!"}
    if not any(c.isdigit() for c in password):
        return False, {"field": "password", "msg":"Password must include at least one number!"}
    if not any(c.isalpha() for c in password):
        return False, {"field": "password", "msg":"Password must include at least one letter!"}
    if len(set(password)) < 3:
        return False, {"field": "password", "msg":"Password must use more varied characters!"}
    return True, None

def valid_confirm_password(password, confirm_password):
    if password != confirm_password:
        return False, {"field": "confirm_password", "msg": "Passwords do not match!"}
    else:
        return True, None

def valid_username(firstname, lastname):

    if not 3 <= len(firstname) <= 15:
        return False, {"field": "firstname", "msg": "First name must be 3-15 characters long!"}
    if not 3 <= len(lastname) <= 15:
        return False, {"field": "lastname", "msg": "Last name must be 3-15 characters long!"}
    if not all(c.isalpha() or c.isspace() for c in firstname):
        return False, {"field": "firstname", "msg": "First name must contain only letters and spaces!"}
    if not all(c.isalpha() or c.isspace() for c in lastname):
        return False, {"field": "lastname", "msg": "Last name must contain only letters and spaces!"}
    return True, None


def valid_email(email):
    pattern = r'^[a-zA-Z0-9_.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True, None
    else:
        return False, {"field": "email", "msg":'Please enter a valid email address!'}

def valid_phone(phone):

    pattern = r'^\+92\d{10}$'

    if re.match(pattern, phone):
        return True, None
    else:
        return False, {"field": "phone", "msg": 'Please enter a valid Pakistani phone number in +92XXXXXXXXXX format.'}

def valid_amount(amount, source_balance):
    try:
        amount = float(amount)
        
        if amount < 0.01:
            return False, {"field": "amount", "msg": "Amount must be more than 0.01."}
        
        if amount > source_balance:
            return False, {"field": "amount", "msg": "Insufficient funds."}
        return True, None
    
    except ValueError:
        return False, {"field": "amount", "msg": "Please enter a valid number for the amount."}