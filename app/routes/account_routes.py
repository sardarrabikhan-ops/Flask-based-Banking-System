#routes/account routes

from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from app.services import transaction_service, account_service
from constants import CURRENT_ACCOUNT_ID, CUSTOMER_ID

account_bp = Blueprint("account", __name__)


#View Accounts
@account_bp.route("/accounts-dashboard")
def accounts():
    customer_id = session.get(CUSTOMER_ID)
    result = account_service.get_accounts_for_customer(customer_id)

    if not result["success"]:
        return render_template("accounts.html", errors=result["data"], accounts=accounts)

    accounts = result["data"]["accounts"]

    return render_template(
        "accounts.html",
        accounts=accounts,
        errors={}
        )

#use account
@account_bp.route("/use-account/<int:acc_id>")
def use_account(acc_id):
    session[CURRENT_ACCOUNT_ID] = acc_id
    return redirect(url_for("customer.dashboard"))

# close account
@account_bp.route("/close-account/<int:acc_id>")
def close_account(acc_id):
    result = account_service.close_account(acc_id)
    
    if not result["success"]:
        for error in result["data"].values():
            flash(error)

        return redirect(url_for("account.accounts"))
    return redirect(url_for("customer.dashboard")) 


#open account
@account_bp.route("/open-account", methods=["GET", "POST"])
def open_account():
    if request.method == "POST":
        customer_id = session.get(CUSTOMER_ID)
        acc_type = request.form.get("acc_type")
        account = account_service.open_account(customer_id, acc_type)
        if not account:
            return 500
        return redirect(url_for("customer.dashboard"))
    return render_template("open_account.html")

#transfer
@account_bp.route("/transfer", methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        
        source_account_id = session.get(CURRENT_ACCOUNT_ID)
        target_account_id = request.form.get("target_account_id")
        amount = float(request.form.get("amount"))
        
        result = transaction_service.transfer(source_account_id, target_account_id, amount)
        
        if result["success"]:
            flash(result["data"]["msg"])
            flash(f"Your new balance is {result["data"]["new_balance"]}")
            return redirect(url_for("customer.dashboard"))
        
        else:
            return render_template("transfer.html", errors=result["data"])
    return render_template("transfer.html", errors={})

#deposit
@account_bp.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":

        target_account_id = session.get(CURRENT_ACCOUNT_ID)
        amount = float(request.form.get("amount"))

        result = transaction_service.deposit(target_account_id, amount)

        if result["success"]:
            flash(result["data"]["msg"])
            flash(f"Your new balance is {result["data"]["new_balance"]}")
            return redirect(url_for("customer.dashboard"))
        
        else:
            return render_template("deposit.html", errors=result["data"])
    return render_template("deposit.html", errors={})

#withdraw
@account_bp.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if request.method == "POST":

        source_account_id = session.get(CURRENT_ACCOUNT_ID)
        amount = float(request.form.get("amount"))

        result = transaction_service.withdraw(source_account_id, amount)

        if result["success"]:
            flash(result["data"]["msg"])
            flash(f"Your new balance is {result["data"]["new_balance"]}")
            return redirect(url_for("customer.dashboard"))
        
        else:
            return render_template("withdraw.html", errors=result["data"])
    return render_template("withdraw.html", errors={})