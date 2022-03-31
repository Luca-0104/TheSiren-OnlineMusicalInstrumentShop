from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp

from app.models import User, Address


class AddAddressForm(FlaskForm):
    recipient_name = StringField('Recipient Name: ', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('Phone: ', validators=[DataRequired(), Length(1, 24)])
    country = StringField('Country: ', validators=[DataRequired(), Length(1, 128)])
    province_or_state = StringField('Province or State:', validators=[DataRequired(), Length(1, 128)])
    city = StringField('City:', validators=[DataRequired(), Length(1, 128)])
    district = StringField('District: ', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Add Address')


class EditAddressForm(FlaskForm):
    recipient_name = StringField('Recipient Name: ', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('Phone: ', validators=[DataRequired(), Length(1, 24)])
    country = StringField('Country: ', validators=[DataRequired(), Length(1, 128)])
    province_or_state = StringField('Province or State:', validators=[DataRequired(), Length(1, 128)])
    city = StringField('City:', validators=[DataRequired(), Length(1, 128)])
    district = StringField('District: ', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Update Address')


class EditProfileForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username: ', validators=[DataRequired(), Length(1, 64), Regexp('^[0-9a-zA-Z_.]{1,}$', 0, "Username must contain only letters, numbers, dots or underscores")])
    # new_password = PasswordField('Password: ', validators=[DataRequired()])
    about_me = StringField('About Me: ', validators=[Length(0, 300)])
    gender = RadioField('Gender: ', choices=[(0, 'Male'), (1, 'Female'), (2, 'Unknown')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Profile')

    def __init__(self, user):
        super(EditProfileForm, self).__init__()
        self.user = user

    def validate_username(self, field):
        user_found = User.query.filter_by(username=field.data).first()
        if user_found is not None and user_found.id != self.user.id:
            raise ValidationError('New username already used.')

    def validate_email(self, field):
        user_found = User.query.filter_by(email=field.data).first()
        if user_found is not None and user_found.id != self.user.id:
            raise ValidationError('New email address already used.')


class UpdateAvatarForm(FlaskForm):
    avatar = FileField('Avatar: ', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng'])])
    submit = SubmitField("Update Avatar")

