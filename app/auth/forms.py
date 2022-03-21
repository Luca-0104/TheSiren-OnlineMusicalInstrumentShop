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

    def validate_email(self, field):
        """
            Determine whether the serial_number already exists.
            :param field: email
        """
        user_found = User.query.filter_by(email=field.data, is_deleted=False).first()
        if user_found is None:
            raise ValidationError('No such user!')

    def validate_password(self, field):
        """
            Determine whether the password is correct or not
            :param field: password
        """
        # find out the user by email
        user_found = User.query.filter_by(email=self.email.data, is_deleted=False).first()
        if user_found is not None:
            # check the password of this user
            if not user_found.verify_password(field.data):
                raise ValidationError('Incorrect password!')


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