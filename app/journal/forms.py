from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class JournalUploadForm(FlaskForm):
    """
        The form for uploading journals
    """
    text = TextAreaField("Write down your journal here", validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField("Broadcast")


class JournalModifyForm(FlaskForm):
    """
        The form for modifying journals
    """
    text = TextAreaField("Modify your journal here", validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField("Submit")
