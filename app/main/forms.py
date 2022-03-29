from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp

from app.models import User, Address


class AddAddressForm(FlaskForm):
    recipient_name = StringField('Recipient Name: ', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('Phone: ', validators=[DataRequired(), Length(1, 24)])
    country = StringField('Country: ', validators=[DataRequired(), Length(1, 128)])
    province_or_state = StringField('Province or State:', validators=[DataRequired(), Length(1, 128)])
    city = StringField('City:', validators=[DataRequired(), Length(1, 128)])
    district = StringField('District: ', validators=[DataRequired(), Length(1, 128)])
































