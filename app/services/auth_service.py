#service/auth_service.py

from datetime import datetime, timedelta

from database import get_db_connection
from app.repositories import (
    email_exists, 
    phone_exists, 
    get_customer_by_email, 
    change_customer_status, 
    change_account_status,
    get_accounts_by_customer_id, 
    update_failed_attempts,
    reset_failed_attempts_and_lock_until,
    create_customer, 
    create_account
    )
from app.utils.security import check_password
from app.utils.general_utils import sec_min_hour, lock_customer
from app.utils.validators import (
    valid_email, 
    valid_password, 
    valid_phone, 
    valid_username, 
    valid_confirm_password)

def register(firstname, lastname, email, phone, password, confirm_password):
    conn =  None
    try:
        conn = get_db_connection()

        errors = {}
        
        if email_exists(conn, email):
            errors["email"] = """An account with this email already exists.
            Please log in to continue or use a different email."""
        
        if phone_exists(conn, phone):
            errors["phone"] = """An account with this phone number already exists.
            Please log in to continue or use a different phone number."""
        
        ok, result = valid_username(firstname, lastname)
        if not ok:
            errors[result["field"]] = result["msg"]
        
        ok, result = valid_email(email)
        if not ok:
            errors[result["field"]] = result["msg"]
        
        ok, result = valid_phone(phone)
        if not ok:
            errors[result["field"]] = result["msg"]

        ok, result = valid_password(password)
        if not ok:
            errors[result["field"]] = result["msg"]
        
        ok, result = valid_confirm_password(password, confirm_password)
        if not ok:
            errors[result["field"]] = result["msg"]
        
        if errors:
            return {"success": False, "data": errors}
        
        customer = create_customer(conn, firstname, lastname, email, password, phone)
        account = create_account(conn, customer.customer_id)
        conn.commit()

        return {"success": True, "data": {"customer": customer, "account": account}}
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()

def login(email, password):
    conn = None
    try:
        conn = get_db_connection()

        errors = {}
        user = get_customer_by_email(conn, email)
        
        if user is None:
            errors["user_existance"] = "User Not Found!"
            return {"success": False, "data": errors}
        
        if user.status == "blocked":
            errors["account_locked"] = "User is blocked!"
            return {"success": False, "data": errors}
        
        current_time = datetime.now()
        if user.lock_until:
            lock_time = datetime.fromtimestamp(user.lock_until)
            
            if current_time < lock_time:
                free_time = lock_time - current_time
                time = sec_min_hour(int(free_time.total_seconds()))
                errors["account_locked"] = f"User is locked temporarily! Try again after {time}"
                return {"success": False, "data": errors}
        
        if not check_password(user.password_hash, password):
            new_failed_attempts = update_failed_attempts(conn, user.customer_id, 1)
            user.failed_attempts = new_failed_attempts
            LOCKS = {
                3: timedelta(seconds=30),
                5: timedelta(minutes=5),
                7: timedelta(minutes=30),
                10: timedelta(hours=1)
            }

            if user.failed_attempts in LOCKS:
                lock_customer(conn, user, LOCKS[new_failed_attempts])
                errors["account_locked"] = f"Account is locked for {LOCKS[new_failed_attempts]}!"
            
            elif user.failed_attempts == 15:
                
                user.status = "blocked"
                errors["account_locked"] = "User is blocked!"
                
                change_customer_status(conn, user.customer_id, "blocked")
                for account in get_accounts_by_customer_id(conn, user.customer_id):
                    change_account_status(conn, account.account_id, "blocked")
            
            elif user.failed_attempts > 7:
                errors["account_locked"] = "Warning! Too many failed attempts! You can be blocked after too many(15) failed attempts!"
            
            conn.commit()
            
            errors["password"] = "Incorrect password!"
            return {"success": False, "data": errors}
        
        user.failed_attempts = 0
        user.lock_until = None
        reset_failed_attempts_and_lock_until(conn, user.customer_id)
        conn.commit()
        return {"success" : True, "data": {"user": user}}
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()