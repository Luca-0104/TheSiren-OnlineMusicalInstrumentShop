from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp

from app.models import User
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    """
        The form class for login
    """
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('keep me login'))
    submit = SubmitField(_l('Login'))

    def validate_email(self, field):
        """
            Determine whether the serial_number already exists.
            :param field: email
        """
        user_found = User.query.filter_by(email=field.data, is_deleted=False).first()
        if user_found is None:
            raise ValidationError(_l('No such user!'))

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
                raise ValidationError(_l('Incorrect password!'))


class RegisterForm(FlaskForm):
    """
        The Form class for register
    """
    username = StringField(_l('Username'), validators=[DataRequired(), Length(1, 64), Regexp('^[0-9a-zA-Z_.]{1,}$', 0, message="Username must contain only letters, numbers, dots or underscores")])
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 64), Email()])
    password1: PasswordField = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Confirm your password'), validators=[DataRequired(), EqualTo('password1', message='Passwords must match!')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, field):
        """
        validate whether the email address is already used
        This function will be called on email field automatically
        :param field: email
        :return:
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_l('Email already exists!'))

    # def validate_username(self, field):
    #     """
    #     validate whether the username has already been used
    #     This function will be called on username field automatically
    #     :param field: username
    #     :return:
    #     """
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username already exists!')