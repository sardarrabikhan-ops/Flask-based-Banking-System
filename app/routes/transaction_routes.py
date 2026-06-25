#routes/transaction.py

from flask import Blueprint, render_template, session
from app.services import transaction_service
from constants import CUSTOMER_ID
from app.utils.decorators import login_required

transaction_bp = Blueprint("transaction", __name__)

#transactions
@transaction_bp.route("/history")
@login_required
def history():
    customer_id = session.get(CUSTOMER_ID)
    transactions = transaction_service.transactions(customer_id)

    return render_template("transactions.html", transactions=transactions)