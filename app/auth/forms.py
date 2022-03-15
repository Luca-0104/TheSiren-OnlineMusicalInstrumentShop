from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp

from app.models import User


class LoginForm(FlaskForm):
    """
        The form class for login
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('keep me login')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """
        The Form class for register
    """
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[0-9a-zA-Z_.]{1,}$', 0, "Username must contain only letters, numbers, dots or underscores")])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password1: PasswordField = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match!')])
    password2 = PasswordField('Confirm your password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        """
        validate whether the email address is already used
        This function will be called on email field automatically
        :param field: email
        :return:
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists!')

    # def validate_username(self, field):
    #     """
    #     validate whether the username has already been used
    #     This function will be called on username field automatically
    #     :param field: username
    #     :return:
    #     """
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username already exists!')