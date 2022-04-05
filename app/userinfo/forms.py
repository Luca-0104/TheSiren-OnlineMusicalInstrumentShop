from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp

from app.models import User, Address


class AddAddressForm(FlaskForm):
    add_recipient_name = StringField('Recipient Name: ', validators=[DataRequired(), Length(1, 64)])
    add_phone = StringField('Phone: ', validators=[DataRequired(), Length(1, 24)])
    add_country = StringField('Country: ', validators=[DataRequired(), Length(1, 128)])
    add_province_or_state = StringField('Province or State:', validators=[DataRequired(), Length(1, 128)])
    add_city = StringField('City:', validators=[DataRequired(), Length(1, 128)])
    add_district = StringField('District: ', validators=[DataRequired(), Length(1, 128)])
    add_address_submit = SubmitField('Add Address')


class EditAddressForm(FlaskForm):
    edit_address_id = StringField()
    edit_recipient_name = StringField('Recipient Name: ', validators=[DataRequired(), Length(1, 64)])
    edit_phone = StringField('Phone: ', validators=[DataRequired(), Length(1, 24)])
    edit_country = StringField('Country: ', validators=[DataRequired(), Length(1, 128)])
    edit_province_or_state = StringField('Province or State:', validators=[DataRequired(), Length(1, 128)])
    edit_city = StringField('City:', validators=[DataRequired(), Length(1, 128)])
    edit_district = StringField('District: ', validators=[DataRequired(), Length(1, 128)])
    edit_address_submit = SubmitField('Update Address')


class EditProfileForm(FlaskForm):
    edit_profile_email = StringField('Email: ', validators=[DataRequired(), Length(1, 64), Email()])
    edit_profile_username = StringField('Username: ', validators=[DataRequired(), Length(1, 64), Regexp('^[0-9a-zA-Z_.]{1,}$', 0, "Username must contain only letters, numbers, dots or underscores")])
    # new_password = PasswordField('Password: ', validators=[DataRequired()])
    edit_profile_about_me = StringField('About Me: ', validators=[Length(0, 300)])
    edit_profile_gender = RadioField('Gender: ', choices=[(0, 'Male'), (1, 'Female'), (2, 'Unknown')], coerce=int, validators=[DataRequired()])
    edit_profile_submit = SubmitField('Update Profile')

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
    update_avatar = FileField('Avatar: ', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng'])])
    update_avatar_submit = SubmitField("Update Avatar")

