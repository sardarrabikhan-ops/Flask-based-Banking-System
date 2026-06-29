#service/account_service.py

from app.repositories import create_account, get_account_by_account_id, get_customer_by_customer_id, get_accounts_by_customer_id, change_account_status
from database import get_db_connection
from constants import Status, AccountType

def open_account(customer_id, acc_type=AccountType.SAVINGS.value):
    conn = None
    try:
        conn = get_db_connection()
        account = create_account(conn, customer_id, acc_type)
        conn.commit()
        return account
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e

    finally:
        if conn:
            conn.close()


def close_account(account_id):
    conn = None
    try:
        conn = get_db_connection()

        errors = {}

        account = get_account_by_account_id(conn, account_id)

        if not account:
            errors["account_existence"] = "Account Not found."
        elif account.balance != 0:
            errors["balance_existence"] = "The account contain some balance, tansfer/withdraw money to close this account."

        if errors:
            return {"success": False, "data": errors}

        
        account = change_account_status(conn, account_id, Status.CLOSED.value)
        conn.commit()
        return {"success": True, "data": {"account": account}}
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_accounts_for_customer(customer_id):
    conn = None
    try:
        conn = get_db_connection()
        
        accounts =  get_accounts_by_customer_id(conn, customer_id)
        customer = get_customer_by_customer_id(conn, customer_id)
        
        errors = {}

        if customer is None:
            errors["customer"] = "Customer not found."
            return {"success": False, "data": errors}
        
        if not accounts:
            errors["accounts"] = "No accounts found for this customer."
            return {"success": False, "data": errors}
        
        if customer.status != Status.ACTIVE.value:
            errors["customer"] = "Customer account is currently not active."
            return {"success": False, "data": errors}
        
        return {"success": True, "data": {"accounts": accounts}}
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()

def get_account_by_id(account_id):

    conn = None
    try:
        conn = get_db_connection()
        account = get_account_by_account_id(conn, account_id)

        errors = {}

        if account is None:
            errors["account"] = "Account not found."
            return {"success": False, "data": errors}
        
        if account.status != Status.ACTIVE.value:
            errors["account"] = "This account is currently not active."
            return {"success": False, "data": errors}
        
        return {"success": True, "data": {"account": account}}
    
    except Exception as e:
        raise e
    
    finally:
        if conn:
            conn.close()