from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, MultipleFileField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, number_range, ValidationError
from app.models import ModelType, Brand


class ProductModifyForm(FlaskForm):
    """
        The form for staffs to modify product info
    """
    name = StringField('Name', validators=[DataRequired(), Length(1, 128)])
    serial_number = StringField('Serial Number', validators=[DataRequired(), Length(1, 128)])
    # choices should be defined in views.py
    brand_id = SelectField('Brand', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit')


class ModelUploadForm(FlaskForm):
    """
        The form for staffs to upload a new model type of a specific product
    """
    name = StringField('Name', validators=[DataRequired(), Length(1, 128)])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), number_range(0, 999999999999)])
    stock = IntegerField('Stock', validators=[DataRequired(), number_range(0, 9999999)])
    serial_number = StringField('Serial Number', validators=[DataRequired(), Length(1, 128)])
    pictures = MultipleFileField('Pictures for exhibition', validators=[DataRequired(), Length(1, 10, 'You must give 1-10 pictures of this commodity')])
    intro_pictures = MultipleFileField('Introduction Pictures', validators=[DataRequired(), Length(1, 10, 'You must give 1-10 introduction pictures')])
    submit = SubmitField('Submit')

    def validate_serial_number(self, field):
        """
        Determine whether the serial_number already exists.
        :param field: serial_number
        """
        if ModelType.query.filter_by(serial_number=field.data, is_deleted=False).first():
            raise ValidationError('Serial Number already used.')

    def validate_pictures(self, field):
        """
        validate whether the length of the names of pictures are out of bound
        This function will be called on picture field automatically
        :param field: pictures
        """
        for pic in field.data:
            if len(pic.filename) > 214:
                raise ValidationError('Picture name cannot longer than 216 chars!')

    def validate_intro_pictures(self, field):
        """
        validate whether the length of the names of intro pictures are out of bound
        This function will be called on picture field automatically
        :param field: intro_pictures
        """
        for pic in field.data:
            if len(pic.filename) > 214:
                raise ValidationError('Picture name cannot longer than 216 chars!')


class ModelModifyForm(FlaskForm):
    """
        The form for staffs to modify the info of a model type
    """
    name = StringField('Name', validators=[DataRequired(), Length(1, 128)])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), number_range(0, 999999999999)])
    stock = IntegerField('Stock', validators=[DataRequired(), number_range(0, 9999999)])
    serial_number = StringField('Serial Number', validators=[DataRequired(), Length(1, 128)])
    # pictures = MultipleFileField('Pictures for exhibition', validators=[DataRequired(), Length(1, 10, 'You must give 1-10 pictures of this commodity')])
    # intro_pictures = MultipleFileField('Introduction Pictures', validators=[DataRequired(), Length(1, 10, 'You must give 1-10 introduction pictures')])
    submit = SubmitField('Submit')


    # def validate_pictures(self, field):
    #     """
    #     validate whether the length of the names of pictures are out of bound
    #     This function will be called on picture field automatically
    #     :param field: pictures
    #     """
    #     for pic in field.data:
    #         if len(pic.filename) > 214:
    #             raise ValidationError('Picture name cannot longer than 216 chars!')
    #
    # def validate_intro_pictures(self, field):
    #     """
    #     validate whether the length of the names of intro pictures are out of bound
    #     This function will be called on picture field automatically
    #     :param field: intro_pictures
    #     """
    #     for pic in field.data:
    #         if len(pic.filename) > 214:
    #             raise ValidationError('Picture name cannot longer than 216 chars!')

