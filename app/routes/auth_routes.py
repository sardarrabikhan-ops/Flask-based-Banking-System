from flask import Blueprint, request, redirect, url_for, render_template, session
from app.services import auth_service

auth_bp = Blueprint("auth", __name__)

#login page
@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember-me")

        result = auth_service.login(email, password)

        if result["success"]:
            session["customer_id"] = result["data"]["user"].customer_id
            session["firstname"] = result["data"]['user'].firstname
            
            session.permanent = remember_me is not None

            if session.get("current_account_id") is None:
                return redirect(url_for("account.select_account"))
            
            return redirect(url_for("customer.dashboard"))
        
        return render_template(
            "login.html",
            errors=result["data"]
            )
    
    return render_template(
        "login.html",
        errors = {}
        )

#signup page
@auth_bp.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        result = auth_service.register(firstname, lastname, email, phone, password, confirm_password)

        if result["success"]:
            return redirect(url_for("auth.login"))
        else:
            return render_template("signup.html", errors = result["data"])
    return render_template("signup.html", errors = {})

#logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))