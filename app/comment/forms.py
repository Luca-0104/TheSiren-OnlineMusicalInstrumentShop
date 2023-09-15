from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, HiddenField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l

from app.models import User


class CommentForm(FlaskForm):
    """
        The form to upload comment for a product
    """
    content = TextAreaField(_l("Leave your comment here"), validators=[DataRequired(_l("You must give some text comment.")), Length(1, 500)])  # comment text
    pictures = MultipleFileField(_l('Upload some pictures'), validators=[DataRequired(), Length(2, 5, _l('You must give 2-5 pictures'))])  # pictures of this product
    rate = StringField(_l("Rate"), validators=[DataRequired(_l("You should rate it."))])   # the rate (star num) should be put into the "value" of this field
    submit = SubmitField(_l("Confirm"))
