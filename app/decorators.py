from functools import wraps
from flask import abort, flash, jsonify, url_for
from flask_login import current_user
from flask_babel import _


def staff_only(is_ajax=False):
    """
    This is the decorator to limit the functions that can only be used by staffs
    :param is_ajax: Whether this decorator is used on a function uses Ajax
    :return: abort 403 OR a jsonify to ajax request
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if this is a customer, we reject them
            if current_user.role_id == 1:
                flash(_("Permission Denied! This function is only provided for Siren staffs!"))

                # if this decorator is used on a function that uses Ajax
                if is_ajax:
                    return jsonify({"returnValue": 318, "redirectURL": url_for("errors.abort_403")})
                # if this decorator is used on a function that does not use Ajax
                else:
                    abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def customer_only(is_ajax=False):
    """
    This is the decorator to limit the functions that can only be used by customers
    :param is_ajax: Whether this decorator is used on a function uses Ajax
    :return: abort 403 OR a jsonify to ajax request
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if this is a staff, we reject them
            if current_user.role_id == 2:
                flash(_("Permission Denied! This function is only provided for customers!"))

                # if this decorator is used on a function that uses Ajax
                if is_ajax:
                    return jsonify({"returnValue": 318, "redirectURL": url_for("errors.abort_403")})
                # if this decorator is used on a function that does not use Ajax
                else:
                    abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def login_required_for_ajax():
    """
    This decorator has the same functionalities as "flask - login_required",
    BUT,  this is the decorator used for the functions using ajax, cuz we cannot abort request in an ajax backend function.
    This is the decorator to limit the functions that can only be used by authenticated users.
    If the user does not log in, they will be redirect to the login page.
    :return: a jsonify to ajax request
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # if the user does not login, we let them log in first
            if not current_user.is_authenticated:
                return jsonify({"returnValue": 318, "redirectURL": url_for("auth.login")})
            return f(*args, **kwargs)
        return decorated_function
    return decorator
