from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp

from app.models import User


class AForm(FlaskForm):
    texta = StringField()
    submita = SubmitField()

class BForm(FlaskForm):
    textb = StringField()
    submitb = SubmitField()