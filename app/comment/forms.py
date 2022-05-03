from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, HiddenField
from wtforms.validators import DataRequired, Length

from app.models import User


class CommentForm(FlaskForm):
    """
        The form to upload comment for a product
    """
    content = TextAreaField("Leave your comment here", validators=[DataRequired(), Length(1, 500)])  # comment text
    pictures = MultipleFileField('Upload some pictures', validators=[DataRequired(), Length(2, 5, 'You must give 2-5 pictures')])  # pictures of this product
    rate = StringField(validators=[DataRequired()])   # the rate (star num) should be put into the "value" of this field
    submit = SubmitField("Confirm")
