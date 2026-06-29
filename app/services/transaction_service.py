#service/transaction_service.py

from app.repositories import get_account_by_account_id, get_accounts_by_customer_id, get_transaction_history, create_transaction
from app.utils.validators import valid_amount
from database import get_db_connection
from constants import Status, TransactionType

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
        transaction_type=TransactionType.DEBIT.value,
        account_id=source_account_id,
        amount=amount
    )
    credit = record_transaction(
        conn,
        transaction_type=TransactionType.CREDIT.value,
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

        amount = float(amount)

        source_account = get_account_by_account_id(conn, source_account_id)

        errors = {}
        
        if not source_account:
            errors["source_account"] = "Account not found, Please select an account."
        
        if amount < 0.01:
            errors["amount"] = "Amount must be more than 0.01."
        
        elif amount > 100000:
            errors["amount"] = "You cannot deposit more than 100 thousand."
        
        if source_account:
            
            if source_account.status == Status.CLOSED.value:
                errors["source_account_status"] = "This account was closed so you cannot deposit money."
        
        if errors:
            return {
                "success": False,
                "data": errors
            }
        
        source_account.deposit(amount)
        record_transaction(conn, TransactionType.CREDIT.value, source_account_id, amount)

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

        amount = float(amount)

        source_account = get_account_by_account_id(conn, source_account_id)

        errors = {}
        
        if not source_account:
            errors["source_account"] = "Account not found, Please select an account."
            return {"success": False, "data": errors}
        
        if source_account.status != Status.ACTIVE.value:
            errors["source_account_status"] = "Source account is not active!"
        
        if source_account:
            ok, result = valid_amount(amount, source_account.balance)
            if not ok:
                errors[result["field"]] = result["msg"]
            
        if errors:
            return {
                "success": False,
                "data": errors
            }
        
        source_account.withdraw(amount)
        record_transaction(conn, TransactionType.DEBIT.value, source_account_id, amount)

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

        amount = float(amount)

        source_account = get_account_by_account_id(conn, source_account_id)
        target_account = get_account_by_account_id(conn, target_account_id)

        errors = {}
        
        if not source_account:
            errors["source_account"] = "Account not found, Please select an account."
        
        if not target_account:
            errors["target_account"] = "Target account not found."
        
        if source_account and target_account:

            if int(target_account_id) == int(source_account_id):
                errors["account_mismatch"] = "You cannot tranfer money to same account."
            
            if source_account.status != Status.ACTIVE.value:
                errors["source_account_status"] = "Source account is not active!"
            
            if target_account.status != Status.ACTIVE.value:
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

        total_transactions = []
        for acc in accounts:

            total_transactions.append({
                "account": acc,
                "transactions": get_transaction_history(
                    conn,
                    acc.account_id
                )
            })

        return total_transactions
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            conn.close()