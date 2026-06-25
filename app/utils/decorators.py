from flask import session, redirect, url_for, abort
from functools import wraps
from constants import CUSTOMER_ID, CURRENT_ACCOUNT_ID
from app.services.account_service import get_account_by_id

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get(CUSTOMER_ID):
            return redirect(url_for("auth.login"))
        
        return func(*args, **kwargs)
    
    return wrapper

def active_account_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get(CURRENT_ACCOUNT_ID):
            return redirect(url_for("account.accounts"))
        
        return func(*args, **kwargs)
    
    return wrapper

def account_owner_required(func):
    @wraps(func)
    def wrapper(acc_id, *args, **kwargs):
        customer_id = session[CUSTOMER_ID]
        result = get_account_by_id(acc_id)

        if not result["success"]:
            abort(403)
        
        account = result["data"]["account"]
        
        if account.customer_id != customer_id:
            abort(403)
        
        return func(acc_id, *args, **kwargs)
    
    return wrapper