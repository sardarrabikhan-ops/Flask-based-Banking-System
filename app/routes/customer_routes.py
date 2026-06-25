from flask import Blueprint, render_template, session
from app.services import auth_service
from app.utils.decorators import login_required
from constants import CUSTOMER_ID, FULL_NAME

customer_bp = Blueprint("customer", __name__)


#dashboard page
@customer_bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session[FULL_NAME])

#profile page
@customer_bp.route("/profile")
@login_required
def profile():
    customer_id = session.get(CUSTOMER_ID)
    result = auth_service.profile(customer_id)

    if not result["success"]:
        return render_template("profile.html", errors=result["errors"])
    return render_template("profile.html", data=result["data"])