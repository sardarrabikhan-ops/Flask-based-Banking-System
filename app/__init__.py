#app/__init__.py

from flask import Flask
from datetime import datetime, timedelta
import os


#creating app
def create_app():

    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="../templates"
    )
    
    secret = os.getenv("SECRET_KEY")
    if not secret:
        raise ValueError("SECRET_KEY is missing")
    
    app.secret_key = secret

    app.permanent_session_lifetime = timedelta(days=7)

        
    #jinja filter to format time
    @app.template_filter("format_time")
    def format_time(value):
        if not value:
            return ""
        dt = datetime.fromtimestamp(value)
        return dt.strftime("%d %b %Y, %I:%M:%S %p")
    
    from app.routes import auth_bp, account_bp, transaction_bp, customer_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(customer_bp)

    return app