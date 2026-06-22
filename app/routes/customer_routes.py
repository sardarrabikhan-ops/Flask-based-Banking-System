from flask import Blueprint, redirect, url_for, render_template, session
from app.services import auth_service
from constants import CUSTOMER_ID, FULL_NAME

customer_bp = Blueprint("customer", __name__)


#dashboard page
@customer_bp.route("/")
def dashboard():
    if CUSTOMER_ID in session:
        return render_template("dashboard.html", username=session[FULL_NAME])
    return redirect(url_for("auth.login"))


@customer_bp.route("/profile")
def profile():
    customer_id = session.get(CUSTOMER_ID)
    result = auth_service.profile(customer_id)

    if not result["success"]:
        return render_template("profile.html", errors=result["errors"])
    return render_template("profile.html", data=result["data"])