from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, FloatField, IntegerField, MultipleFileField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, number_range, ValidationError
from app.models import ModelType, Brand, Product


class ProductModifyForm(FlaskForm):
    """
        The form for staffs to modify product info
    """
    name = StringField(_l('Name'), validators=[DataRequired(), Length(1, 128)],
                       render_kw={"data-errors": 'Please Enter Name.'})
    # serial_number = StringField(_l('Serial Number'), validators=[DataRequired(), Length(1, 128)],
    #                             render_kw={"data-errors": 'Please Enter Serial Number.'})
    # choices should be defined in views.py
    brand_id = SelectField(_l('Brand'), validators=[DataRequired()], coerce=int, render_kw={"data-style": 'py-0'})
    submit = SubmitField(_l('Update'))

    # instance variables (those are not in the form)
    def __init__(self, current_product_id):
        super(ProductModifyForm, self).__init__()
        self.current_product_id = current_product_id

    def validate_serial_number(self, field):
        """
        Determine whether the serial_number already exists.
        :param field: serial_number
        """
        product_found = Product.query.filter_by(serial_number=field.data, is_deleted=False).first()
        # If the product with the same serial number is not the current product itself
        if product_found is not None and product_found.id != self.current_product_id:
            raise ValidationError(_l('Serial Number already used.'))


class ModelUploadForm(FlaskForm):
    """
        The form for staffs to upload a new model type of a specific product
    """
    name = StringField(_l('Name'), validators=[DataRequired(), Length(1, 128)],
                       render_kw={"data-errors": 'Please Enter Name.'})
    description = StringField(_l('Description'), validators=[DataRequired()], render_kw={"row": 4})
    price = FloatField(_l('Price'), validators=[DataRequired(), number_range(0, 999999999999)],
                       render_kw={"data-errors": 'Please Enter Price.'})
    stock = IntegerField(_l('Stock'), validators=[DataRequired(), number_range(0, 9999999)],
                         render_kw={"data-errors": 'Please Enter Stock.'})
    # serial_number = StringField('Serial Number', validators=[DataRequired(), Length(1, 128)],
    #                             render_kw={"data-errors": 'Please Enter Serial Number.'})
    serial_number = StringField(_l('Serial Number'), validators=[DataRequired(), Length(1, 128)])
    pictures = MultipleFileField(_l('Pictures for exhibition'), validators=[DataRequired(), Length(1, 10, 'You must give 1-10 pictures of this commodity')],
                                 render_kw={"accept": 'image/*'})
    # intro_pictures = MultipleFileField(_l('Introduction Pictures'), validators=[DataRequired(), Length(1, 10, 'You must give 1-10 introduction pictures')],
    #                                    render_kw={"accept": 'image/*'})
    submit = SubmitField(_l('Submit'))

    # instance variables (those are not in the form)
    def __init__(self, current_product_id):
        super(ModelUploadForm, self).__init__()
        self.current_product_id = current_product_id

    def validate_serial_number(self, field):
        """
        Determine whether the serial_number already exists.
        :param field: serial_number
        """
        model_found = ModelType.query.filter_by(serial_number=field.data, product_id=self.current_product_id, is_deleted=False).first()
        if model_found is not None:
            raise ValidationError(_l('Serial Number already used in other model of this product!'))

    def validate_pictures(self, field):
        """
        validate whether the length of the names of pictures are out of bound
        This function will be called on picture field automatically
        :param field: pictures
        """
        for pic in field.data:
            if len(pic.filename) > 214:
                raise ValidationError(_l('Picture name cannot longer than 216 chars!'))

    # def validate_intro_pictures(self, field):
    #     """
    #     validate whether the length of the names of intro pictures are out of bound
    #     This function will be called on picture field automatically
    #     :param field: intro_pictures
    #     """
    #     for pic in field.data:
    #         if len(pic.filename) > 214:
    #             raise ValidationError(_l('Picture name cannot longer than 216 chars!'))


class ModelModifyForm(FlaskForm):
    """
        The form for staffs to modify the info of a model type
    """
    name = StringField(_l('Name'), validators=[DataRequired(), Length(1, 128)],
                       render_kw={"data-errors": 'Please Enter Name.'})
    description = StringField(_l('Description'), validators=[DataRequired()], render_kw={"row": 4})
    price = FloatField(_l('Price'), validators=[DataRequired(), number_range(0, 999999999999)],
                       render_kw={"data-errors": 'Please Enter Price.'})
    stock = IntegerField(_l('Stock'), validators=[DataRequired(), number_range(0, 9999999)],
                         render_kw={"data-errors": 'Please Enter Stock.'})
    serial_number = StringField(_l('Serial Number'), validators=[DataRequired(), Length(1, 128)],
                                render_kw={"data-errors": 'Please Enter Serial Number.'})
    pictures = MultipleFileField(_l('Pictures for exhibition'), validators=[Length(0, 10, 'You must give 1-10 pictures of this commodity')])
    # intro_pictures = MultipleFileField(_l('Introduction Pictures'), validators=[Length(0, 10, 'You must give 1-10 introduction pictures')])
    submit = SubmitField(_l('Submit'))

    # get the model_id of the
    def __init__(self, current_model_id):
        super(ModelModifyForm, self).__init__()
        self.current_model_id = current_model_id

    def validate_serial_number(self, field):
        """
        Determine whether the serial_number already exists.
        :param field: serial_number
        """
        model_found = ModelType.query.filter_by(serial_number=field.data, is_deleted=False).first()
        # If the model type with the same serial number is not the current model itself
        if model_found is not None and model_found.id != self.current_model_id:
            raise ValidationError(_l('Serial Number already used.'))

    def validate_pictures(self, field):
        """
        validate whether the length of the names of pictures are out of bound
        This function will be called on picture field automatically
        :param field: pictures
        """
        for pic in field.data:
            if len(pic.filename) > 214:
                raise ValidationError(_l('Picture name cannot longer than 216 chars!'))

    # def validate_intro_pictures(self, field):
    #     """
    #     validate whether the length of the names of intro pictures are out of bound
    #     This function will be called on picture field automatically
    #     :param field: intro_pictures
    #     """
    #     for pic in field.data:
    #         if len(pic.filename) > 214:
    #             raise ValidationError(_l('Picture name cannot longer than 216 chars!'))
