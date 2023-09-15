from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l


class JournalUploadForm(FlaskForm):
    """
        The form for uploading journals
    """
    title = StringField(_l("Give a title for your journal"), validators=[DataRequired(), Length(1, 128)])
    text = TextAreaField(_l("Write down your journal here"), validators=[DataRequired(), Length(1, 5120)])
    submit = SubmitField(_l("Broadcast"))


class JournalEditForm(FlaskForm):
    """
        The form for modifying journals
    """
    title = StringField(_l("Modify title here"), validators=[DataRequired(), Length(1, 128)])
    text = TextAreaField(_l("Modify your journal body here"), validators=[DataRequired(), Length(1, 5120)])
    submit = SubmitField(_l("Submit"))
