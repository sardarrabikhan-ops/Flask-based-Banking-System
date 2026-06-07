from flask import Blueprint, redirect, url_for, render_template, session
from app.repositories import customer_repo

customer_bp = Blueprint("customer", __name__)


#dashboard page
@customer_bp.route("/")
def dashboard():
    if "customer_id" in session:
        return render_template("dashboard.html", username=session["firstname"])
    return redirect(url_for("auth.login"))