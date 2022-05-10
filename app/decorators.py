from functools import wraps
from flask import abort, flash
from flask_login import current_user


def staff_only():
    """ This is the decorator to limit the functions that can only be used by staffs """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if this is a customer, we reject them
            if current_user.role_id == 1:
                flash("Permission Denied! This function is only provided for Siren staffs!")
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def customer_only():
    """ This is the decorator to limit the functions that can only be used by customers """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if this is a staff, we reject them
            if current_user.role_id == 2:
                flash("Permission Denied! This function is only provided for customers!")
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
