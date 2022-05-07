from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class JournalUploadForm(FlaskForm):
    """
        The form for uploading journals
    """
    title = StringField("Give a title for your journal", validators=[DataRequired(), Length(1, 20)])
    text = TextAreaField("Write down your journal here", validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField("Broadcast")


class JournalEditForm(FlaskForm):
    """
        The form for modifying journals
    """
    title = StringField("Modify title here", validators=[DataRequired(), Length(1, 20)])
    text = TextAreaField("Modify your journal body here", validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField("Submit")
