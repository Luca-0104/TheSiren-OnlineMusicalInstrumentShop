from flask import session, flash, current_app, redirect, url_for, render_template, request
from flask_login import login_user

from . import auth
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User


@auth.route('/logout')
def logout():
    """
    The function to log the user out
    :return: redirect back to the home page
    """
    # pop out related sessions
    session.pop("username", None)
    session.pop("uid", None)
    session.pop("role_id", None)
    session.pop("avatar", None)
    session.pop("theme", None)

    # logout using the flask-login
    login_user()

    flash('You have been logged out')

    # logger
    current_app.logger.info("user logged out")

    return redirect(url_for("main.index"))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # logger
    current_app.logger.info("come in /register")

    form = RegisterForm()

    # when the form is submitted legally (POST method)
    if form.validate_on_submit():
        # create a new user object
        user = User(email=form.email.data, username=form.username.data, password=form.password1.data,
                    role_id=1)
        db.session.add(user)
        db.session.commit()
        flash("Register Successfully! You can go for login now!")

        # logger
        current_app.logger.info("a new user registered")

        return redirect(url_for('auth.login'))

    # (GET method)
    return render_template('auth/register_new.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # logger
    current_app.logger.info("come in /login")

    form = LoginForm()

    # when the form is submitted legally (POST method)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            # record the user in session, init the info in the session
            session["username"] = user.username
            session["uid"] = user.id
            session["role_id"] = user.role_id
            session["avatar"] = user.avatar
            session["theme"] = user.theme

            # use flask-login to login the user
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')

            flash("Login success!")

            # logger
            current_app.logger.info("a user logs in successfully: @" + user.username)

            # redirect back to the original url or the index page
            return redirect(next)

        # logger
        current_app.logger.info("a user logs in failed")

        # if we get here, this means the user give the wrong data and login failed
        flash("Login Failed! Check your username or password.")

    # (GET method)
    return render_template('auth/login_new.html', form=form)

