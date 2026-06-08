#service/transaction_service.py

from app.repositories import get_account_by_account_id, get_accounts_by_customer_id, get_transaction_history, create_transaction
from app.utils.validators import valid_amount
from database import get_db_connection

def record_transaction(conn, transaction_type, account_id, amount):
    transaction = create_transaction(
        conn,
        account_id=account_id,
        transaction_type=transaction_type,
        amount=amount
    )
    return transaction

def record_transfer(conn, source_account_id, target_account_id, amount):

    debit = record_transaction(
        conn,
        transaction_type="Debit",
        account_id=source_account_id,
        amount=amount
    )
    credit = record_transaction(
        conn,
        transaction_type="Credit",
        account_id=target_account_id,
        amount=amount
    )
    return (
        debit, 
        credit
    )

def deposit(source_account_id, amount):
    conn = None

    try:
        conn = get_db_connection()

        source_account = get_account_by_account_id(conn, source_account_id)

        errors = {}
        
        if not source_account:
            errors["source_account"] = "html will handle it."
        
        if amount <= 0:
            errors["amount"] = "Amount must be greater than zero."
        
        elif amount > 100000:
            errors["amount"] = "You cannot deposit more than 100 thousand."
        
        elif source_account.status == "closed":
            errors["account_status"] = "This account was closed so you cannot deposit money."
        
        if errors:
            return {
                "success": False,
                "data": errors
            }
        
        source_account.deposit(amount)
        record_transaction(conn, "Credit", source_account_id, amount)

        conn.commit()

        return {
            "success": True,
            "data": {"new_balance": source_account.balance, "msg": f"Successfully deposited ${amount:.2f} to your account!"}
        }
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()

def withdraw(source_account_id, amount):
    conn = None

    try:
        conn = get_db_connection()

        source_account = get_account_by_account_id(conn, source_account_id)

        errors = {}
        
        if not source_account:
            errors["source_account"] = "html will handle it."
        

        ok, result = valid_amount(amount, source_account.balance)
        if not ok:
            errors[result["field"]] = result["msg"]
        
        if errors:
            return {
                "success": False,
                "data": errors
            }
        
        source_account.withdraw(amount)
        record_transaction(conn, "Debit", source_account_id, amount)

        conn.commit()

        return {
            "success": True,
            "data": {"new_balance": source_account.balance, "msg": f"Successfully withdrwal ${amount:.2f} from your account!"}
        }
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()

def transfer(source_account_id, target_account_id, amount):
    conn = None

    try:
        conn = get_db_connection()

        source_account = get_account_by_account_id(conn, source_account_id)
        target_account = get_account_by_account_id(conn, target_account_id)

        errors = {}
        
        if not source_account:
            errors["source_account"] = "html will handle it."
        
        if not target_account:
            errors["target_account"] = "Target account not found."

        elif target_account_id == source_account_id:
            errors["account_mismatch"] = "You cannot tranfer money to same account."
        
        elif source_account.status != "active":
            errors["source_account_status"] = "Source account is not active!"
        
        elif target_account.status != "active":
            errors["target_account_status"] = "Target account is not active!"
        
        ok, result = valid_amount(amount, source_account.balance)
        if not ok:
            errors[result["field"]] = result["msg"]
        
        if errors:
            return {
                "success": False,
                "data": errors
            }

        source_account.transfer_to(target_account, amount)
        record_transfer(conn, source_account.account_id, target_account.account_id, amount)
        conn.commit()
        return {
            "success": True,
            "data": {"new_balance": source_account.balance, "msg": f"Successfully transferred ${amount:.2f} to target account!"}
        }
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()

def transactions(customer_id):
    conn = None

    try:
        conn = get_db_connection()
        accounts = get_accounts_by_customer_id(conn, customer_id)

        transactions = []
        for acc in accounts:
            transactions.append(get_transaction_history(conn, acc.account_id))
        return transactions
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()