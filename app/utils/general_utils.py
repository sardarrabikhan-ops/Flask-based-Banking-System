#utils/id_generator.py

from app.repositories.customer_repo import update_lock_until
from datetime import datetime


def sec_min_hour(value):
    if value < 60:
        return f"{value} seconds"
    elif value < 3600:
        minutes = value // 60
        return f"{minutes} minutes"
    else:
        hours = value // 3600
        return f"{hours} hours"

def lock_customer(conn, user, duration):
    lock_until = int((datetime.now() + duration).timestamp())
    user.lock_until = lock_until
    update_lock_until(conn, user.customer_id, lock_until)