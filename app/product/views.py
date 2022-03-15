"""
    Here are the functions for product management (for staff user to use)
"""
from flask import jsonify, request, flash, render_template, redirect, url_for
from flask_login import login_required
from sqlalchemy import and_

from config import Config
from . import product
from .forms import ModelUploadForm, ModelModifyForm, ProductModifyForm
from .. import db

from ..models import Product, ModelType, Category, Brand
from ..public_tools import upload_picture


# ------------------------------------------------ render the page  of stock management ------------------------------------------------


@product.route('/stock-management')
def show_page_stock_management():
    # get all the products from the database
    product_list = Product.query.filter_by(is_deleted=False).all()
    # render this page
    return render_template('', product_list=product_list)


# ------------------------------------------------ Search functions for staffs to manage the stock ------------------------------------------------


@product.route('/search-stock/<string:key_word>/<int:search_type>')
def search_stock(key_word, search_type):
    """
    Search the model types whose serial_number contains the content
    key_word: the string in the searching blank
    search_type: 1: by name; 2: by serial_number
    """

    """ search the model type using different search_type """
    mt_list = []
    if search_type == 1:
        # search model types by name
        mt_list = ModelType.query.filter(and_(ModelType.name.contains(key_word),
                                              ModelType.is_deleted == False)).order_by(ModelType.product_id).all()
    elif search_type == 2:
        # search model types by serial number
        mt_list = ModelType.query.filter(and_(ModelType.serial_number.contains(key_word),
                                              ModelType.is_deleted == False)).order_by(ModelType.product_id).all()

    """ classify the found model types by their product_id """
    if len(mt_list) != 0:
        # key: product_id, value: a list of model types
        model_dict = {mt_list[0].product_id: [mt_list[0]]}
        # loop through all the mt found and classify them by their product_id
        for mt in mt_list:
            if mt.product_id in model_dict:
                model_dict[mt.product_id].append(mt)
            else:
                model_dict[mt.product_id] = [mt]
    else:
        model_dict = {}

    """ render the page """
    return render_template('', model_dict=model_dict)


# ------------------------------------------------ CUD operations on 'product' ------------------------------------------------


@product.route('/upload-product')
@login_required
def upload_product():
    pass


@product.route('/api/stock-management/remove-product', methods=['POST'])
@login_required
def remove_product():
    """
    (Using Ajax)
    Remove the product and all its model types
    """
    if request.method == 'POST':
        # get product id from Ajax
        product_id = request.form["product_id"]
        # get the instance of the product from db
        p = Product.query.get(product_id)
        if p is not None:
            p.delete()
            return jsonify({'returnValue': 0})
        return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})


@product.route('/upload-model-type/<int:product_id>', methods=['GET', 'POST'])
#@login_required
def upload_model_type(product_id):
    """
        (Backend forms needed)
        :param product_id: Which product this model belongs to
    """
    form = ModelUploadForm()
    if form.validate_on_submit():
        """
            Check if the related product exists.
        """
        p = Product.query.get(product_id)
        if p is not None and not p.is_deleted:  # The product exists
            # get a list of categories of this model type
            cate_lst = request.values.getlist('categories[]')

            """
                create a new instance of model type object 
            """
            new_model_type = ModelType(name=form.name.data,
                                       description=form.description.data,
                                       price=form.price.data,
                                       stock=form.stock.data,
                                       serial_number=form.serial_number.data,
                                       )
            db.session.add(new_model_type)

            # append the selected categories to this model type
            for cate_id in cate_lst:
                new_model_type.categories.append(Category.query.get(cate_id))

            db.session.commit()

            """
                Dealing with the uploaded pictures (The model type pictures)
            """
            pic_list = form.pictures.data
            result = upload_picture(pic_list, new_model_type.id, Config.PIC_TYPE_MODEL)
            # get the status code
            status = result[0]
            if status == 0:
                # success
                flash(result[1])
            elif status == 1:
                # failed
                flash(result[1])
            elif status == 2:
                # partial success
                failed_list = result[1]
                flash_str = 'Picture '
                for name in failed_list:
                    flash_str += name
                    flash_str += ', '
                flash_str += ' are failed to be uploaded! Check the suffix'
                flash(flash_str)

            """
                Dealing with the uploaded pictures (Introduction pictures)
            """
            intro_pic_list = form.intro_pictures.data
            result = upload_picture(intro_pic_list, new_model_type.id, Config.PIC_TYPE_MODEL_INTRO)
            # get the status code
            status = result[0]
            if status == 0:
                # success
                flash(result[1])
            elif status == 1:
                # failed
                flash(result[1])
            elif status == 2:
                # partial success
                failed_list = result[1]
                flash_str = 'Picture '
                for name in failed_list:
                    flash_str += name
                    flash_str += ', '
                flash_str += ' are failed to be uploaded! Check the suffix.'
                flash(flash_str)

        else:  # The product does not exist
            flash('Error! The product does not exist! Try it again!')

        # back to the stock management page
        # return redirect(url_for('product.show_page_stock_management'))
        return redirect(url_for('main.index'))

    # render the page of upload form
    return render_template('staff/page-upload-modeltype.html', form=form)


# ------------------------------------------------ CUD operations on 'model_type' ------------------------------------------------


@product.route('/modify-product/<int:product_id>', methods=['GET', 'POST'])
#@login_required
def modify_product(product_id):
    """
        (Backend forms needed, 'categories' are not in backend form)
    """
    form = ProductModifyForm(product_id)
    form.brand_id.choices = [(b.id, b.name) for b in Brand.query.all()]  # initialize the choices of the SelectField
    # get the product object by id
    p = Product.query.get(product_id)
    # get all the categories from database (give this to frontend)
    all_cate_list = Category.query.all()
    if form.validate_on_submit():
        # get a list of categories of this product
        cate_lst = request.values.getlist('categories[]')

        # update values in this product (except the cate)
        p.name = form.name.data
        p.serial_number = form.serial_number.data
        p.brand_id = form.brand_id.data

        # update the categories of this product
        # step1: clear the cate of this product
        for cate in p.categories.all():
            p.categories.remove(cate)
        # step2: append the new categories
        for cate in cate_lst:
            c = Category.query.filter_by(name=cate.strip()).first()
            p.categories.append(c)

        db.session.add(p)
        db.session.commit()

        flash('The product information updated!')

        # back to the stock management page
        return redirect(url_for('product.show_page_stock_management'))

    # before submit, fill the table with former values
    form.name.data = p.name
    form.serial_number.data = p.serial_number
    form.brand_id.data = p.brand_id
    # the product modify page
    return render_template('staff/page-modify-product.html', form=form, all_cate_list=all_cate_list)


@product.route('/api/stock-management/remove-model-type', methods=['POST'])
@login_required
def remove_model_type():
    """
        (Using Ajax)
        Remove the model type, if this is the last model type
        in its product, the product should be removed as well.
    """
    if request.method == 'POST':
        # get the database id of the model type from Ajax
        model_type_id = request.form['model_type_id']
        # get the instance of the model type from database
        mt = ModelType.query.get(model_type_id)
        if mt is not None and not mt.is_deleted:
            # check if the model type is the last one in its product
            mt_list = mt.product.get_exist_model_types()
            if len(mt_list) == 1 and mt_list.first().id == mt.id:
                # remove the product and all its model types
                mt.product.delete()
                return jsonify({'returnValue': 0})
            # remove this model type
            mt.delete()
            return jsonify({'returnValue': 0})
        else:
            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})


@product.route('/modify-model-type/<int:model_id>', methods=['GET', 'POST'])
#@login_required
def modify_model_type(model_id):
    """
        (Backend forms needed)
        (This modification does not include modifying pictures)
        :param model_id: The id of the model type that should be modified
    """
    # get the instance of the model by id
    model = ModelType.query.get(model_id)
    form = ModelModifyForm(model_id)
    if form.validate_on_submit():
        # serial_number is okay
        model.name = form.name.data
        model.description = form.description.data
        model.price = form.price.data
        model.stock = form.stock.data
        model.serial_number = form.serial_number.data
        # commit to database
        db.session.add(model)

        """
            Dealing with the uploaded pictures (The model type pictures)
        """
        pic_list = form.pictures.data
        if len(pic_list) != 0:
            result = upload_picture(pic_list, model.id, Config.PIC_TYPE_MODEL)
            # get the status code
            status = result[0]
            if status == 0:
                # success
                flash(result[1])
            elif status == 1:
                # failed
                flash(result[1])
                return redirect(url_for('product.modify_model_type'))
            elif status == 2:
                # partial success
                failed_list = result[1]
                flash_str = 'Picture '
                for name in failed_list:
                    flash_str += name
                    flash_str += ', '
                flash_str += ' are failed to be uploaded! Check the suffix'
                flash(flash_str)

        """
            Dealing with the uploaded pictures (Introduction pictures)
        """
        intro_pic_list = form.intro_pictures.data
        if len(intro_pic_list) != 0:
            result = upload_picture(intro_pic_list, model.id, Config.PIC_TYPE_MODEL_INTRO)
            # get the status code
            status = result[0]
            if status == 0:
                # success
                flash(result[1])
            elif status == 1:
                # failed
                flash(result[1])
                return redirect(url_for('product.modify_model_type'))
            elif status == 2:
                # partial success
                failed_list = result[1]
                flash_str = 'Picture '
                for name in failed_list:
                    flash_str += name
                    flash_str += ', '
                flash_str += ' are failed to be uploaded! Check the suffix.'
                flash(flash_str)
        # --------------------------------------------------
        db.session.commit()
        flash('Model updated!')
        # back to the stock management page
        return redirect(url_for('product.show_page_stock_management'))

    # before submit, fill the table with former values
    form.name.data = model.name
    form.description.data = model.description
    form.price.data = model.price
    form.stock.data = model.stock
    form.serial_number.data = model.serial_number
    return render_template('staff/page-modify-modeltype.html', form=form)
