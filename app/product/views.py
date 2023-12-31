"""
    Here are the functions for product management (for staff user to use)
"""
import os

from flask import jsonify, request, flash, render_template, redirect, url_for, json, current_app
from flask_login import login_required
from flask_babel import _
from sqlalchemy import and_
from collections import defaultdict

from config import Config
from . import product
from .forms import ModelUploadForm, ModelModifyForm, ProductModifyForm
from .. import db
from ..decorators import staff_only, login_required_for_ajax

from ..models import Product, ModelType, Category, Brand, Audio, Order
from ..public_tools import upload_picture, get_unique_shop_instance, get_epidemic_mode_status, generate_safe_pic_name


# ------------------------------------------------ render the page  of stock management ------------------------------------------------
@product.route('/staff-index')
@login_required
@staff_only()
def show_page_staff_index():
    """
        This function renders the page of DashBoard
    """
    # get whether the epidemic mode has been turned on
    epidemic_mode_on = get_epidemic_mode_status()

    # get the unique instance of this shop
    unique_shop_instance = get_unique_shop_instance()

    # get the best selling (top 6) model types
    best_sell_mt_lst = ModelType.query.filter_by(is_deleted=False).order_by(ModelType.sales.desc()).limit(6).all()

    # get the total number of paid orders
    paid_order_count = 0
    paid_order_count += Order.query.filter_by(status_code=1).count()
    paid_order_count += Order.query.filter_by(status_code=2).count()
    paid_order_count += Order.query.filter_by(status_code=3).count()
    paid_order_count += Order.query.filter_by(status_code=4).count()

    return render_template('staff/staff-index.html',
                           best_sell_mt_lst=best_sell_mt_lst,
                           epidemic_mode_on=epidemic_mode_on,
                           paid_order_count=paid_order_count,
                           total_sales=unique_shop_instance.total_sales,
                           total_sale_count=unique_shop_instance.total_sale_count)


@product.route('/stock-management', methods=['GET', 'POST'])
@login_required
@staff_only()
def show_page_stock_management():
    """
    This function has integrated the function of searching and rendering the stock management page
    About the search function:
        Search the model types whose serial_number contains the content
        key_word: the string in the searching blank
        search_type: 1: by name; 2: by serial_number
    """
    epidemic_mode_on = get_epidemic_mode_status()

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
        """ if the this is the initial access of this page (no search now) """
        is_search = False
        previous_key = None

        # get all the products from the database
        product_list = Product.query.filter_by(is_deleted=False).all()
        # turn product list into a model_dict
        model_dict = {p: p.model_types.all() for p in product_list}

    # render this page
    return render_template('staff/page-list-product.html', model_dict=model_dict, is_search=is_search,
                           previous_key=previous_key, epidemic_mode_on=epidemic_mode_on)


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
@staff_only()
def upload_product():
    """
        This method uses the frontend form
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

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
            new_model_type = ModelType(name=m_name, description=m_description, price=m_price, stock=m_stock,
                                       serial_number=m_serial_number, product=new_product)
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
                # failed_list = result[1]
                # flash_str = 'Picture '
                # for name in failed_list:
                #     flash_str += name
                #     flash_str += ', '
                # flash_str += ' are failed to be uploaded! Check the suffix'
                # flash(flash_str)
                flash(_("Part of the pictures are failed to be uploaded! Check their suffix!"))

            """ add introduction pictures """
            # result_intro = upload_picture(m_pics_intro_lst, new_model_type.id, Config.PIC_TYPE_MODEL_INTRO)
            # # get the status code
            # status2 = result_intro[0]
            # if status2 == 0:
            #     # success
            #     pass
            # elif status2 == 1:
            #     # failed
            #     flash(result_intro[1])
            # elif status2 == 2:
            #     # partial success
            #     failed_list = result_intro[1]
            #     flash_str = 'Picture '
            #     for name in failed_list:
            #         flash_str += name
            #         flash_str += ', '
            #     flash_str += ' are failed to be uploaded! Check the suffix'
            #     flash(flash_str)

        # go back to the management page after adding the new product (not matter are there any failures about pictures)
        flash(_('New product and its models are uploaded successfully!'))
        return redirect(url_for('product.show_page_stock_management'))

    return render_template('staff/page-add-product.html', epidemic_mode_on=epidemic_mode_on)


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
        p_list = Product.query.filter_by(serial_prefix=serial_prefix, is_deleted=False).order_by(
            Product.serial_rank.desc()).all()
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
@login_required_for_ajax()
@staff_only(is_ajax=True)
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
@staff_only()
def modify_product(product_id):
    """
        (Backend forms needed, 'categories' are not in backend form)
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

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
    return render_template('staff/page-modify-product.html', form=form, all_cate_list=all_cate_list,
                           epidemic_mode_on=epidemic_mode_on)


# ------------------------------------------------ CUD operations on 'model_type' ------------------------------------------------


@product.route('/upload-model-type/<int:product_id>', methods=['GET', 'POST'])
@login_required
@staff_only()
def upload_model_type(product_id):
    """
        (Backend forms needed)
        :param product_id: Which product this model belongs to
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

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
            flash(_("Model Type Uploaded!"))

            """
                Dealing with the uploaded pictures (The model type pictures)
            """
            pic_list = form.pictures.data
            result = upload_picture(pic_list, new_model_type.id, Config.PIC_TYPE_MODEL)
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
                # failed_list = result[1]
                # flash_str = 'Picture '
                # for name in failed_list:
                #     flash_str += name
                #     flash_str += ', '
                # flash_str += ' are failed to be uploaded! Check the suffix'
                # flash(flash_str)
                flash(_("Part of the pictures are failed to be uploaded! Check their suffix!"))

            """
                Dealing with the uploaded pictures (Introduction pictures)
            """
            # intro_pic_list = form.intro_pictures.data
            # result = upload_picture(intro_pic_list, new_model_type.id, Config.PIC_TYPE_MODEL_INTRO)
            # # get the status code
            # status = result[0]
            # if status == 0:
            #     # success
            #     flash(result[1])
            # elif status == 1:
            #     # failed
            #     flash(result[1])
            # elif status == 2:
            #     # partial success
            #     failed_list = result[1]
            #     flash_str = 'Picture '
            #     for name in failed_list:
            #         flash_str += name
            #         flash_str += ', '
            #     flash_str += ' are failed to be uploaded! Check the suffix.'
            #     flash(flash_str)

        else:  # The product does not exist
            flash(_('Error! The product does not exist! Try it again!'))

        # back to the stock management page
        # return redirect(url_for('product.show_page_stock_management'))
        return redirect(url_for('product.show_page_stock_management'))

    # render the page of upload form
    return render_template('staff/page-upload-modeltype.html', form=form, epidemic_mode_on=epidemic_mode_on)


@product.route('/api/stock-management/remove-model-type', methods=['POST'])
@login_required_for_ajax()
@staff_only(is_ajax=True)
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
@staff_only()
def modify_model_type(model_id):
    """
        (Backend forms needed)
        (This modification does not include modifying pictures)
        :param model_id: The id of the model type that should be modified
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

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
                pass
            elif status == 1:
                # failed
                flash(result[1])
                return redirect(url_for('product.modify_model_type'))
            elif status == 2:
                # partial success
                # failed_list = result[1]
                # flash_str = 'Picture '
                # for name in failed_list:
                #     flash_str += name
                #     flash_str += ', '
                # flash_str += ' are failed to be uploaded! Check the suffix'
                # flash(flash_str)
                flash(_("Part of the pictures are failed to be uploaded! Check their suffix!"))

        """
            Dealing with the uploaded pictures (Introduction pictures)
        """
        # intro_pic_list = form.intro_pictures.data
        # if len(intro_pic_list) != 0:
        #     result = upload_picture(intro_pic_list, model.id, Config.PIC_TYPE_MODEL_INTRO)
        #     # get the status code
        #     status = result[0]
        #     if status == 0:
        #         # success
        #         flash(result[1])
        #     elif status == 1:
        #         # failed
        #         flash(result[1])
        #         return redirect(url_for('product.modify_model_type'))
        #     elif status == 2:
        #         # partial success
        #         failed_list = result[1]
        #         flash_str = 'Picture '
        #         for name in failed_list:
        #             flash_str += name
        #             flash_str += ', '
        #         flash_str += ' are failed to be uploaded! Check the suffix.'
        #         flash(flash_str)

        # --------------------------------------------------
        db.session.commit()
        flash(_('Model Type updated!'))
        # back to the stock management page
        return redirect(url_for('product.show_page_stock_management'))

    # before submit, fill the table with former values
    form.name.data = model.name
    form.description.data = model.description
    form.price.data = model.price
    form.stock.data = model.stock
    form.serial_number.data = model.serial_number
    return render_template('staff/page-modify-modeltype.html', form=form, epidemic_mode_on=epidemic_mode_on)


# ------------------------------------------------ Upload Media Files for Model Types  ------------------------------------------------

@product.route('/stock-management/upload-video/<int:mt_id>', methods=['GET', 'POST'])
@login_required
@staff_only()
def upload_video(mt_id):
    """
    This is a function for staffs uploading video file for a specific model type
    :param mt_id: The id of the corresponding model type
    """
    if request.method == 'POST':
        # check the model type
        mt = ModelType.query.get(mt_id)

        if mt is None:
            current_app.logger.error("This model type does not exist!")
            return redirect(url_for('product.show_page_stock_management'))

        if mt.is_deleted:
            flash(_("Failed! You cannot upload video for a deleted model type."))
            current_app.logger.error("This model type has been deleted!")
            return redirect(url_for('product.show_page_stock_management'))

        # get video file from the form
        video = request.files.get("video_file")

        if video is None:
            current_app.logger.error("video not gotten from the request")
            return redirect(url_for('product.show_page_stock_management'))

        filename = video.filename
        suffix = filename.rsplit('.')[-1]

        # check the file type
        if suffix not in Config.ALLOWED_VIDEO_SUFFIXES:
            flash(_("Failed! You should upload .mp4 video only."))
            current_app.logger.error("video file type error!")
            return redirect(url_for('product.show_page_stock_management'))

        # make sure the name of video is safe
        filename = generate_safe_pic_name(filename)

        # save video in local directory
        file_path = os.path.join(Config.video_dir, filename).replace('\\', '/')
        video.save(file_path)

        # save the reference in database
        path = 'upload/model_type/videos'
        ref_address = os.path.join(path, filename).replace('\\', '/')
        mt.video_address = ref_address
        db.session.add(mt)
        db.session.commit()

        flash(_("Video uploaded successfully!"))

    return redirect(url_for('product.show_page_stock_management'))


@product.route('/stock-management/upload-audio/<int:mt_id>', methods=['GET', 'POST'])
@login_required
@staff_only()
def upload_audio(mt_id):
    """
    This is a function for staffs uploading audio file for a specific model type
    :param mt_id: The id of the corresponding model type
    """
    if request.method == 'POST':
        # check the model type
        mt = ModelType.query.get(mt_id)

        if mt is None:
            current_app.logger.error("This model type does not exist!")
            return redirect(url_for('product.show_page_stock_management'))

        if mt.is_deleted:
            flash(_("Failed! You cannot upload video for a deleted model type."))
            current_app.logger.error("This model type has been deleted!")
            return redirect(url_for('product.show_page_stock_management'))

        # get audio file from the form
        audio = request.files.get("audio_file")

        if audio is None:
            current_app.logger.error("audio not gotten from the request")
            return redirect(url_for('product.show_page_stock_management'))

        filename = audio.filename
        suffix = filename.rsplit('.')[-1]

        # check the file type
        if suffix not in Config.ALLOWED_AUDIO_SUFFIXES:
            flash(_("Failed! You should upload .mp3 audio only."))
            current_app.logger.error("audio file type error!")
            return redirect(url_for('product.show_page_stock_management'))

        # make sure the name of audio is safe
        filename = generate_safe_pic_name(filename)

        # save audio in local directory
        file_path = os.path.join(Config.audios_dir, filename).replace('\\', '/')
        audio.save(file_path)

        # save the reference in database
        path = 'upload/model_type/audios'
        ref_address = os.path.join(path, filename).replace('\\', '/')
        new_audio = Audio(address=ref_address, model_type_id=mt_id)
        db.session.add(new_audio)
        db.session.commit()

        flash(_("Audio uploaded successfully!"))

    return redirect(url_for('product.show_page_stock_management'))


@product.route('/stock-management/upload-3d-file/<int:mt_id>', methods=['GET', 'POST'])
@login_required
@staff_only()
def upload_3d_file(mt_id):
    """
    This is a function for staffs uploading 3D model file for a specific model type
    :param mt_id: The id of the corresponding model type
    """
    if request.method == 'POST':
        # check the model type
        mt = ModelType.query.get(mt_id)

        if mt is None:
            current_app.logger.error("This model type does not exist!")
            return redirect(url_for('product.show_page_stock_management'))

        if mt.is_deleted:
            flash(_("Failed! You cannot upload video for a deleted model type."))
            current_app.logger.error("This model type has been deleted!")
            return redirect(url_for('product.show_page_stock_management'))

        # get 3d file from the form
        three_d_file = request.files.get("three_d_file")
        # get texture file from the form
        three_d_texture_file = request.files.get("three_d_texture_file")

        if three_d_file is None:
            current_app.logger.error("3d file not gotten from the request")
            return redirect(url_for('product.show_page_stock_management'))

        # give the default texture if not uploaded one
        is_default_texture = False
        if three_d_texture_file.filename == "":
            is_default_texture = True

        """ 
            Deal with 3D model file 
        """
        filename = three_d_file.filename
        suffix = filename.rsplit('.')[-1]

        # check the file type
        if suffix not in Config.ALLOWED_3D_MODEL_SUFFIXES:
            flash(_("Failed! You should upload .fbx/.obj file only."))
            current_app.logger.error("3d file type error!")
            return redirect(url_for('product.show_page_stock_management'))

        # make sure the name of 3d file is safe
        filename = generate_safe_pic_name(filename)

        # save 3d file in local directory
        file_path = os.path.join(Config.threeD_dir, filename).replace('\\', '/')
        three_d_file.save(file_path)

        # save the reference in database
        path = 'upload/model_type/3d-model-files'
        ref_address = os.path.join(path, filename).replace('\\', '/')
        mt.three_d_model_address = ref_address
        db.session.add(mt)

        """ 
            Deal with texture file
        """
        # if a texture file is uploaded
        if not is_default_texture:
            texture_filename = three_d_texture_file.filename
            suffix = texture_filename.rsplit('.')[-1]

            # check the file type
            if suffix not in Config.ALLOWED_3D_MODEL_TEXTURE_SUFFIXES:
                flash(_("Failed! You should upload '.png' file only."))
                current_app.logger.error("3d texture file type error!")
                # rollback the db
                db.session.rollback()
                return redirect(url_for('product.show_page_stock_management'))

            # make sure the name of 3d texture file is safe
            texture_filename = generate_safe_pic_name(texture_filename)

            # save 3d texture file in local directory
            texture_file_path = os.path.join(Config.threeD_texture_dir, texture_filename).replace('\\', '/')
            three_d_texture_file.save(texture_file_path)

            # save the reference in database
            t_path = 'upload/model_type/3d-model-texture-files'
            texture_ref_address = os.path.join(t_path, texture_filename).replace('\\', '/')
            mt.three_d_model_texture_address = texture_ref_address


        # if no texture uploaded, we should give a default one
        else:
            mt.three_d_model_texture_address = "upload/model_type/3d-model-texture-files/pre-store/cello.png"

        db.session.add(mt)

        # commit to db
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            flash(_("3D model upload failed!"))
            return redirect(url_for('product.show_page_stock_management'))

        flash(_("3D model uploaded successfully!"))

    return redirect(url_for('product.show_page_stock_management'))

# ------------------------------------------------ operations on 'categories' ------------------------------------------------
# ------------------------------------------- may NOT be adopted! ------------------------------------------------------------------------------


@product.route('/api/stock-management/add-category', methods=['POST'])
@login_required_for_ajax()
@staff_only(is_ajax=True)
def add_category():
    """
    (Using Ajax)
    Add and new category into the system
    """
    if request.method == 'POST':
        cate_name = request.form.get('cate_name')

        if cate_name is None:
            current_app.logger.error("info are not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # check if the category already exist
        cate_found = Category.query.filter_by(name=cate_name).first()
        if cate_found is not None:
            current_app.logger.info("A staff attempt to add an existing category")
            return jsonify({'returnValue': 2, 'msg': 'This category already exists.'})

        # create a new category
        new_cate = Category(name=cate_name)
        db.session.add(new_cate)
        db.session.commit()

        return jsonify({'returnValue': 0})
    return jsonify({'returnValue': 1})


@product.route('/api/stock-management/remove-category', methods=['POST'])
@login_required_for_ajax()
@staff_only(is_ajax=True)
def remove_category():
    """
    (Using Ajax)
    Remove a category in this system.
    The products under this category should be assigned to 'others'
    """
    pass


# ------------------------------------------------ operations on 'brands' ------------------------------------------------

@product.route('/api/stock-management/add-brand', methods=['POST'])
@login_required_for_ajax()
@staff_only(is_ajax=True)
def add_brand():
    """
    (Using Ajax)
    Add and new brand into the system
    """
    if request.method == 'POST':
        brand_name = request.form.get('brand_name')

        if brand_name is None:
            current_app.logger.error("info are not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # check if the brand already exist
        brand_found = Brand.query.filter_by(name=brand_name).first()
        if brand_found is not None:
            current_app.logger.info("A staff attempt to add an existing brand")
            return jsonify({'returnValue': 2, 'msg': 'This brand already exists.'})

        # create a new brand
        new_brand = Brand(name=brand_name)
        db.session.add(new_brand)
        db.session.commit()

        return jsonify({'returnValue': 0})
    return jsonify({'returnValue': 1})


@product.route('/api/stock-management/remove-brand', methods=['POST'])
@login_required_for_ajax()
@staff_only(is_ajax=True)
def remove_brand():
    """
    (Using Ajax)
    Remove a brand in this system.
    Only the brand id >= 18 can be removed
    The products under this brand should be assigned to 'others'
    """
    if request.method == 'POST':
        brand_id = request.form.get('brand_id')

        if brand_id is None:
            current_app.logger.error("info are not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # parse id to int
        try:
            brand_id = int(brand_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'returnValue': 1})

        # check if the brand is the pre-stored brand (id<18)
        if brand_id < 18:
            current_app.logger.info('A staff attempt to delete a pre-stored brand')
            return jsonify({'returnValue': 2, 'msg': 'The pre-stored brand can not be deleted'})

        # check if the brand exists
        brand = Brand.query.get(brand_id)
        if brand is None:
            current_app.logger.error("The brand does not exist")
            return jsonify({'returnValue': 1})

        # now we can delete this brand
        # first, we need to assign all the products under this brand to 'other' brand
        for p in brand.products:
            p.brand_id = 17
            db.session.add(p)
        db.session.commit()
        # then, delete the brand from db
        db.session.delete(brand)
        db.session.commit()

        return jsonify({'returnValue': 0})
    return jsonify({'returnValue': 1})
