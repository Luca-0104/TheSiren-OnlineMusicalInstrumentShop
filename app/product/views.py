"""
    Here are the functions for product management (for staff user to use)
"""
from flask import jsonify, request, flash, render_template, redirect, url_for, json
from flask_login import login_required
from flask_babel import _
from sqlalchemy import and_
from collections import defaultdict

from config import Config
from . import product
from .forms import ModelUploadForm, ModelModifyForm, ProductModifyForm
from .. import db

from ..models import Product, ModelType, Category, Brand
from ..public_tools import upload_picture


# ------------------------------------------------ render the page  of stock management ------------------------------------------------
@product.route('/staff-index')
@login_required
def show_page_staff_index():
    """
        This function renders the page of DashBoard
    """
    # get the best selling (top 6) model types
    best_sell_mt_lst = ModelType.query.filter_by(is_deleted=False).order_by(ModelType.sales.desc()).limit(6).all()
    return render_template('staff/staff-index.html', best_sell_mt_lst=best_sell_mt_lst)


@product.route('/stock-management', methods=['GET', 'POST'])
@login_required
def show_page_stock_management():
    """
    This function has integrated the function of searching and rendering the stock management page
    About the search function:
        Search the model types whose serial_number contains the content
        key_word: the string in the searching blank
        search_type: 1: by name; 2: by serial_number
    """

    """ if the search form is submitted """
    if request.method == 'POST':
        key_word = request.form.get('key_word')
        search_type = int(request.form.get('search_type'))

        is_search = True
        previous_key = key_word

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
        model_dict = dict()
        if len(mt_list) != 0:
            # key: product (obj), value: a list of model types (obj)
            # loop through all the mt found and classify them by their product
            for mt in mt_list:
                if mt.product in model_dict:
                    model_dict[mt.product].append(mt)
                else:
                    model_dict[mt.product] = [mt]

    else:
        """ if the this is the init access of this page (no search now) """
        is_search = False
        previous_key = None

        # get all the products from the database
        product_list = Product.query.filter_by(is_deleted=False).all()
        # turn product list into a model_dict
        model_dict = {p: p.model_types.all() for p in product_list}

    print(is_search)

    # render this page
    return render_template('staff/page-list-product.html', model_dict=model_dict, is_search=is_search, previous_key=previous_key)


# ------------------------------------------------ Search functions for staffs to manage the stock ------------------------------------------------

'''
######## Abandoned!
######## The search function is consolidated into the show_page_stock_management() function
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
'''

# ------------------------------------------------ CUD operations on 'product' ------------------------------------------------


@product.route('/upload-product', methods=['GET', 'POST'])
@login_required
def upload_product():
    """
        This method uses the frontend form
    """
    # if the form is submitted
    if request.method == 'POST':
        p_name = request.form.get('product_name')
        cate_lst = request.values.getlist('categories[]')
        brand_name = request.form.get('product_brand')
        # get the brand object by its name
        brand = Brand.query.filter_by(name=brand_name).first()

        # 'get' requests
        # the number count of init model types
        mt_count = int(request.args.get('counter'))
        serial_prefix = request.args.get('serial_prefix')
        serial_rank = request.args.get('serial_rank')

        # print('---------------------------------- product ----------------------------------')
        # print('p_name: ', p_name)
        # print('serial_prefix: ', serial_prefix)
        # print('serial_rank: ', serial_rank)
        # print('cate_lst: ', cate_lst)
        # print('brand_name: ', brand_name)
        # print('mt_count: ', mt_count)

        """ 
            store the Product obj into the db 
        """
        # create an object of this new product
        new_product = Product(name=p_name, serial_prefix=serial_prefix, serial_rank=serial_rank, brand=brand)
        db.session.add(new_product)

        # add categories to this product
        for cate_name in cate_lst:
            # get the cate obj
            c = Category.query.filter_by(name=cate_name).first()
            # append it to the product
            new_product.categories.append(c)

        db.session.commit()

        """
            store all the following model types of this product into db
        """
        # loop through all the init model types
        for i in range(1, mt_count + 1):
            # the 'name' attribute of <input/>s of this model
            key_name = str(i) + '_model_name'
            key_description = str(i) + '_model_description'
            key_price = str(i) + '_model_price'
            key_stock = str(i) + '_model_stock'
            key_serial_number = str(i) + '_model_num'
            key_pics = str(i) + '_model_pic'
            key_pics_intro = str(i) + '_model_intro_pic'

            # get the information of this model from frontend form
            m_name = request.form.get(key_name)
            m_description = request.form.get(key_description)
            m_price = request.form.get(key_price)
            m_stock = request.form.get(key_stock)
            m_serial_number = request.form.get(key_serial_number)
            m_pics_lst = request.files.getlist(key_pics)
            m_pics_intro_lst = request.files.getlist(key_pics_intro)

            # print('---------------------------------- models ----------------------------------')
            # print('m_name: ', m_name)
            # print('m_description: ', m_description)
            # print('m_price', m_price)
            # print('m_stock', m_stock)
            # print('m_serial_number', m_serial_number)
            # print('m_pics_lst', m_pics_lst)
            # print('m_pics_intro_lst', m_pics_intro_lst)

            # create an obj of this new model type
            new_model_type = ModelType(name=m_name, description=m_description, price=m_price, stock=m_stock, serial_number=m_serial_number, product=new_product)
            db.session.add(new_model_type)
            db.session.commit()

            """ add pictures """
            result = upload_picture(m_pics_lst, new_model_type.id, Config.PIC_TYPE_MODEL)
            # get the status code
            status = result[0]
            if status == 0:
                # success
                pass
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

            """ add introduction pictures """
            result_intro = upload_picture(m_pics_intro_lst, new_model_type.id, Config.PIC_TYPE_MODEL_INTRO)
            # get the status code
            status2 = result_intro[0]
            if status2 == 0:
                # success
                pass
            elif status2 == 1:
                # failed
                flash(result_intro[1])
            elif status2 == 2:
                # partial success
                failed_list = result_intro[1]
                flash_str = 'Picture '
                for name in failed_list:
                    flash_str += name
                    flash_str += ', '
                flash_str += ' are failed to be uploaded! Check the suffix'
                flash(flash_str)

            # go back to the management page after adding the new product (not matter are there any failures about pictures)
            flash(_('New product and its models are uploaded successfully!'))
            return redirect(url_for('product.show_page_stock_management'))

    return render_template('staff/page-add-product.html')


@product.route('/api/stock-management/upload-product/validate-serial-p', methods=['POST'])
def validate_product_serial():
    """
        (Using Ajax)
        Get a serial prefix of product, then append a proper serial rank to it.
        e.g. b1-c1-t1-a1 >> b1-c1-t1-a1-2
        :return a string of serial number (product)
    """
    if request.method == 'POST':
        # get serial prefix
        serial_prefix = request.form["serial_prefix"]
        # get a list of product with this serial prefix
        p_list = Product.query.filter_by(serial_prefix=serial_prefix, is_deleted=False).order_by(Product.serial_rank.desc()).all()
        # if no product in list, the rank should be 1
        if len(p_list) == 0:
            rank = 1
        else:
            # the rank should greater than the largest existing onn by 1
            rank = p_list[0].serial_rank + 1
        # concatenate the serial prefix with serial rank
        serial_number = '{}-{}'.format(serial_prefix, rank)
        return jsonify({"serial_number": serial_number, "returnValue": 0})
    return jsonify({"returnValue": 1})


@product.route('/api/stock-management/upload-product/validate-serial-m', methods=['POST'])
def validate_model_serial():
    """
        (Using Ajax)
        Get a list of sting of model serial number (not include the product part),
        check if they are different from each other.
        We do not need to check the them with the serial numbers in db.
        extra data example:
            e.g. [1, 2, 3, 2, 4, 1] >> {1: [0, 5], 2: [1, 3], 3: [2], 4: [4], 'returnValue': 2}
        :return: 0: ok, 1: not ok, 2: not ok and some extra data
    """
    if request.method == 'POST':
        # get a JSON list of serial number from Ajax
        json_serial_lst = request.form['JSON_serial_lst']
        # check if the json is gotten
        if json_serial_lst is not None:
            # unpack the json into the python list
            serial_lst = json.loads(json_serial_lst)
            # check if every element is unique in the list
            if len(serial_lst) > len(set(serial_lst)):
                # check the overlapped element and their index
                dd = defaultdict(list)
                for k, value in [(v, index) for index, v in enumerate(serial_lst)]:
                    dd[k].append(value)
                # e.g. [1, 2, 3, 2, 4, 1] >> {1: [0, 5], 2: [1, 3], 3: [2], 4: [4]}
                result_dic = dict(dd)
                # add the returnValue into the result_dic
                result_dic['returnValue'] = 2
                # returnValue=2 means not ok and there are some other extra data
                return jsonify(result_dic)
            else:
                return jsonify({'returnValue': 0})
        else:
            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})


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


@product.route('/modify-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
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
        # p.serial_number = form.serial_number.data
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

        flash(_('The product information updated!'))

        # back to the stock management page
        return redirect(url_for('product.show_page_stock_management'))

    # before submit, fill the table with former values
    form.name.data = p.name
    # form.serial_number.data = p.serial_number
    form.brand_id.data = p.brand_id
    # the product modify page
    return render_template('staff/page-modify-product.html', form=form, all_cate_list=all_cate_list)


# ------------------------------------------------ CUD operations on 'model_type' ------------------------------------------------


@product.route('/upload-model-type/<int:product_id>', methods=['GET', 'POST'])
@login_required
def upload_model_type(product_id):
    """
        (Backend forms needed)
        :param product_id: Which product this model belongs to
    """
    form = ModelUploadForm(product_id)
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
                                       product=p)
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
            flash(_('Error! The product does not exist! Try it again!'))

        # back to the stock management page
        # return redirect(url_for('product.show_page_stock_management'))
        return redirect(url_for('product.show_page_stock_management'))

    # render the page of upload form
    return render_template('staff/page-upload-modeltype.html', form=form)


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
            if len(mt_list) == 1 and mt_list[0].id == mt.id:
                # remove the product and all its model types
                mt.product.delete()
                # returnValue=2 means the last product is removed
                return jsonify({'returnValue': 2})
            # remove this model type
            mt.delete()
            return jsonify({'returnValue': 0})
        else:
            return jsonify({'returnValue': 1})
    return jsonify({'returnValue': 1})


@product.route('/modify-model-type/<int:model_id>', methods=['GET', 'POST'])
@login_required
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
        flash(_('Model updated!'))
        # back to the stock management page
        return redirect(url_for('product.show_page_stock_management'))

    # before submit, fill the table with former values
    form.name.data = model.name
    form.description.data = model.description
    form.price.data = model.price
    form.stock.data = model.stock
    form.serial_number.data = model.serial_number
    return render_template('staff/page-modify-modeltype.html', form=form)
