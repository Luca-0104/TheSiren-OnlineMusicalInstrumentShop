import os
import traceback

from flask import render_template, request, redirect, url_for, session, jsonify, flash, json, current_app, abort
from flask_login import login_required, current_user
from flask_babel import _
from sqlalchemy import and_, or_

from config import Config
from . import main
from .. import db
from ..decorators import customer_only, staff_only, login_required_for_ajax
from ..models import Product, ModelType, Category, Brand, BrowsingHistory, Journal, Customization
from ..public_tools import get_unique_shop_instance, generate_safe_pic_name

import random
from datetime import datetime


@main.route('/')
def index():
    """
        The function is for rendering the real index page
    """

    """ top 3 of 'views' number """
    rec_views = ModelType.query.filter_by(is_deleted=False).order_by(ModelType.views.desc()).limit(3).all()

    """ (if logged in) top 3 recommendation according to viewing history """
    rec_preference = None
    if current_user.is_authenticated:
        rec_preference = []
        # find out user preference from their histories
        cate_dic = dict()
        for history in current_user.browsing_histories:
            # filter out the 'type' cate
            for cate in history.model_type.product.categories.filter(Category.id > 6).filter(Category.id < 53):
                if cate.id in cate_dic:
                    cate_dic[cate.id] += history.count
                else:
                    cate_dic[cate.id] = 1
        # sort the dict and get top 3 preferred 'type' cate
        sorted_id = sorted(cate_dic, key=cate_dic.get, reverse=True)[:3]

        # get 3 models randomly from top 3 cates
        if len(sorted_id) == 3:
            # for each cate type, we randomly get a model type
            for cate_id in sorted_id:
                cate = Category.query.get(cate_id)
                p_lst = cate.products.all()
                if len(p_lst) > 0:
                    # get a product randomly
                    p = p_lst[random.randint(0, len(p_lst) - 1)]
                    # get a model from this product randomly
                    mt = p.model_types.all()[random.randint(0, p.model_types.count() - 1)]
                    rec_preference.append(mt)

        elif len(sorted_id) == 2:
            # we give two models from cate1 and 1 model from cate2
            cate1 = Category.query.get(sorted_id[0])
            cate2 = Category.query.get(sorted_id[1])

            # get 2 models from cate1
            p_lst1 = cate1.products.all()
            m_lst1 = []
            for p in p_lst1:
                m_lst1 += p.model_types.all()

            if len(m_lst1) >= 2:
                for i in range(2):
                    mt = m_lst1[random.randint(0, len(m_lst1) - 1)]
                    while mt in rec_preference:
                        mt = m_lst1[random.randint(0, len(m_lst1) - 1)]
                    rec_preference.append(mt)
            elif len(m_lst1) == 1:
                rec_preference.append(m_lst1[0])

            # get 1 model from cate2
            p_lst2 = cate2.products.all()
            m_lst2 = []
            for p in p_lst2:
                m_lst2 += p.model_types.all()

            if len(m_lst2) > 0:
                mt = m_lst2[random.randint(0, len(m_lst2) - 1)]

        elif len(sorted_id) == 1:
            # get 3 models from this cate
            cate = Category.query.get(sorted_id[0])
            p_lst = cate.products.all()
            m_lst = []
            for p in p_lst:
                m_lst += p.model_types.all()

            if len(m_lst) >= 3:
                for i in range(3):
                    mt = m_lst[random.randint(0, len(m_lst) - 1)]
                    while mt in rec_preference:
                        mt = m_lst[random.randint(0, len(m_lst) - 1)]
                    rec_preference.append(mt)
            else:
                rec_preference += m_lst

        # check if the number of model is not enough (3 models)
        if len(rec_preference) < 3:
            diff = 3 - len(rec_preference)
            # fill up the blank randomly
            for i in range(diff):
                mt = ModelType.query.get(random.randint(1, ModelType.query.count()))
                rec_preference.append(mt)

    """ 'just arrive' (top 4 according to datetime) """
    rec_time = ModelType.query.filter_by(is_deleted=False).order_by(ModelType.release_time.desc()).limit(4).all()

    return render_template('main/index_new.html', rec_time=rec_time, rec_views=rec_views, rec_preference=rec_preference, is_index=True)


@main.route('/index-test')
@main.route('/index_test', methods=['GET', 'POST'])
def index_test():
    """
        The function for rendering the fake index page
    """

    return render_template('main/index_test.html')


@main.route('/premium-intro')
def premium_intro():
    """
    This function renders the page of the advertisement of premium membership
    """
    return render_template('main/premium.html')


@main.route('/brand-intro/<int:brand_id>')
def brand_intro(brand_id):
    """
    This function renders the introduction page of the specific brand
    """
    # get the brand obj
    brand = Brand.query.get(brand_id)
    # concatenate the prefix with brand name to get the template name
    template_name = "main/brand_intro/{}.html".format(brand.name.lower())
    try:
        flash(_("Welcome to learn more about The " + brand.name))
        return render_template(template_name)
    except Exception as e:
        # traceback.print_exc()
        return render_template("main/brand_intro/coming-soon.html", brand_name=brand.name)


@main.route('/about-us')
def about_us():
    """
    This function renders the page of "about us"
    """
    # get all the journals form db
    journal_lst = Journal.query.order_by(Journal.timestamp.desc())

    flash(_("Here, you can learn more about The Siren~"))
    return render_template('main/about_siren.html', journal_lst=journal_lst)


@main.route('/all-models')
def go_all():
    """
        The function for going to see all the products (model types).
        (Namely, a see-all-function without any filters)
    """
    # order the models by their popularity
    all_model_type = ModelType.query.filter_by(is_deleted=False) \
        .order_by(ModelType.sales.desc(), ModelType.views.desc()) \
        .all()
    return render_template('main/page_all_commodities.html', mt_list=all_model_type)  # see-all page


@main.route('/search', methods=['POST'])
def search():
    """
    Search the specific product model types according to the user input
    keywords: The keywords that the users inputted for searching
    (Namely, a see-all-function with filters)
    """
    if request.method == 'POST':
        key_word = request.form.get('key_word')

        # search model types by name
        mt_list = search_models_by_keyword(keyword=key_word) \
            .order_by(ModelType.sales.desc(), ModelType.views.desc()) \
            .all()

        # search model type by brand name
        brand_lst = Brand.query.filter(Brand.name.contains(key_word)).all()

        # merge the search results
        for brand in brand_lst:
            for p in brand.products:
                for mt in p.model_types:
                    if mt not in set(mt_list):
                        mt_list.append(mt)

        flash(_("Following are the searching results about '{}'.".format(key_word)))
        return render_template('main/page_all_commodities.html', mt_list=mt_list, key_word=key_word)  # see-all page

    return redirect(url_for('main.index'))


def search_models_by_keyword(keyword):
    """
    This function searches a list of model which contains given keyword in their name
    :param keyword: A string of key word
    :return: A BaseQuery object that contains a list of models found
    """
    mt_bq_lst = ModelType.query.filter(and_(ModelType.name.contains(keyword), ModelType.is_deleted == False))
    return mt_bq_lst


# ----------------- sorting tools > ------------------


def take_sales(model_type):
    """ for generating the sorting key """
    return model_type.sales


def take_id(db_model):
    """ for generating the sorting key """
    return db_model.id


def sort_db_models(model_list: list, sort_key, reverse: bool):
    """
    For sorting a list of db model objs
    :param model_list: a list of db models
    :param sort_key: can be a function that return an attribute of these models
    :param reverse: True means in descending order
    """
    model_list.sort(key=sort_key, reverse=reverse)


# ----------------- < sorting tools ------------------


@main.route('/products-in-brand/<string:brand_name>')
def products_in_brand(brand_name):
    """
        Go to the see-all page with the constrain of a specific brand
    """
    # get the brand obj by its name
    brand = Brand.query.filter_by(name=brand_name).first()
    # get products of this brand
    product_lst = brand.products.filter_by(is_deleted=False).all()
    # put all the models into a list
    mt_list = []
    for product in product_lst:
        mt_list += product.get_exist_model_types()
    # sort the model list by the sale numbers
    sort_db_models(mt_list, sort_key=take_sales, reverse=True)

    flash(_("Following are the commodities of the brand - {}".format(brand_name)))
    return render_template('main/page_all_commodities.html', mt_list=mt_list)  # see-all page


@main.route('/products-in-category/<string:cate_name>')
def products_in_category(cate_name):
    """
    Go to the see-all page with the constrain of a specific category
    :param cate_name: The name of the category
    """
    # get the category obj from db
    cate = Category.query.filter_by(name=cate_name).first()

    if cate is None:
        current_app.logger.error("No such category with this name")
        return redirect(url_for("main.go_all"))

    # get all products in this category
    product_lst = cate.products.filter_by(is_deleted=False).all()
    # put all the models into a list
    mt_list = []
    for product in product_lst:
        mt_list += product.get_exist_model_types()
    # sort the model list by the sale numbers
    sort_db_models(mt_list, sort_key=take_sales, reverse=True)

    flash(_("Below are the products in category of '{}'.".format(cate_name)))
    return render_template('main/page_all_commodities.html', mt_list=mt_list, cate_name=cate_name)  # see-all page


@main.route('/product-details/<int:mt_id>')
def model_type_details(mt_id):
    """
    Rendering the page of 'Mode Type details'
    :param mt_id: The id of the selected model type
    """
    # get the model type by id
    try:
        mt = ModelType.query.get(mt_id)
    except Exception as e:
        current_app.logger.error(e)
        flash(_('No such commodity!'))
        return redirect(url_for('main.index'))

    # check if the model type exists
    if mt is None:
        flash(_('No such commodity!'))
        current_app.logger.error("No such model type with this id")
        return redirect(url_for('main.index'))

    # increase the views number
    mt.views = mt.views + 1
    db.session.add(mt)
    db.session.commit()

    # record the user browsing history
    if current_user.is_authenticated:
        # check if the user has viewed this model before
        bh = BrowsingHistory.query.filter_by(user=current_user, model_type=mt).first()
        if bh:
            # update the count and time
            bh.count = bh.count + 1
            bh.timestamp = datetime.utcnow()
            db.session.add(bh)
        else:
            # record this new history
            new_bh = BrowsingHistory(user=current_user, model_type=mt)
            db.session.add(new_bh)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()

    """ get the recommended related models (models in same cate with high popularity) """
    related_mt_lst = []
    for cate in mt.product.categories:
        # do not use "additional requirements" for recommendation
        if cate.id not in range(53, 57):
            for p in cate.products:
                related_mt_lst += p.get_exist_model_types()
    # sort the related list
    sort_db_models(related_mt_lst, sort_key=take_sales, reverse=True)
    # limit the number of mt in related list
    related_mt_lst = related_mt_lst[:12]

    """ get the recommendation of 'more from this brand' """
    more_mt_this_brand = []
    brand = mt.product.brand
    if brand is None:
        current_app.logger.error(e)
    else:
        # loop through all the products in this brand
        for p in brand.products:
            # put all the model types into the lst
            more_mt_this_brand += p.get_exist_model_types()
        # sort the lst
        sort_db_models(more_mt_this_brand, sort_key=take_sales, reverse=True)
        # limit the number of mt in lst
        more_mt_this_brand = more_mt_this_brand[:12]

    return render_template('main/page-commodity-details.html', model=mt, related_mt_lst=related_mt_lst, more_mt_this_brand=more_mt_this_brand)



@main.route('/model-listing/<string:search_content>')
def model_listing(search_content):
    """
    This function is used to render the page of "model-listing"
    :param search_content: The content of the "search", if this is "", this means the used did not get to here by searching
    """
    # search the models by search_content
    if search_content != "":
        # search by name
        mt_bq_lst = search_models_by_keyword(keyword=search_content)
        mt_lst = mt_bq_lst.all()

        # search model type by brand name
        brand_lst = Brand.query.filter(Brand.name.contains(search_content)).all()

        # merge the search results
        for brand in brand_lst:
            for p in brand.products:
                for mt in p.model_types:
                    if mt not in set(mt_lst):
                        mt_lst.append(mt)

        flash(_("Following are the searching results of '{}'.".format(search_content)))
    else:
        # if com here by clicking on "go all"
        mt_lst = ModelType.query.all()
    return render_template('main/page_all_commodities.html', search_content=search_content, mt_lst=mt_lst)


@main.route('/change_language', methods=['GET', 'POST'])
def change_language():
    # if the user already logged in, we change language setting both in db and session
    if current_user.is_authenticated:

        # determine the redirect_target of this user according to their role_id
        redirect_to = url_for("main.index")
        if current_user.role_id == 2:   # staff
            redirect_to = url_for("product.show_page_staff_index")

        # change setting in db
        if current_user.language == 'en':
            current_user.language = 'zh'
            flash("已为您切换语言为 [中文]")

        elif current_user.language == 'zh':
            current_user.language = 'en'
            flash("Language has been changed to [English]")

        db.session.add(current_user)
        db.session.commit()

        # change setting in session
        session["language"] = current_user.language

        # redirect the user
        return redirect(redirect_to)

    else:
        # if the user is anonymous, we only change the language setting in session

        # if the first time access the website, we should init the session of language first
        if session.get("language") is None:
            session["language"] = 'en'
            flash("Language has been changed to [English]")
            return redirect(url_for("main.index"))

        # change setting in the session
        if session["language"] == 'zh':
            session["language"] = 'en'
            flash("Language has been changed to [English]")

        elif session["language"] == 'en':
            session["language"] = 'zh'
            flash("已为您切换语言为 [中文]")

    return redirect(url_for("main.index"))


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------


@main.route('/api/filter-model-types', methods=['POST'])
def filter_model_types():
    """
    (Using Ajax)
    Get a group of filters from Ajax (c, t, a, b)
    Each one has and only has a single element.
    Concatenating all the filter elements together can get a serial-prefix for searching the products and models.
    If the User access this page using "search" function, we need to search again before filtering.
    :return:
    """
    if request.method == 'POST':
        # get the filter elements (c, t, a, b)
        filter_c = request.form.get("c", default="%")    # e.g. c1, c2, c3, ...
        filter_t = request.form.get("t", default="%")
        filter_a = request.form.get("a", default="%")
        filter_b = request.form.get("b", default="%")
        # get search content, if it is "", we will get all the models
        search_content = request.form.get('search_content', default="")

        if filter_c == "":
            filter_c = "%"
        if filter_t == "":
            filter_t = "%"
        if filter_a == "":
            filter_a = "%"
        if filter_b == "":
            filter_b = "%"

        # print("c: ", filter_c)
        # print("t: ", filter_t)
        # print("a: ", filter_a)
        # print("b: ", filter_b)
        # print("search_count: ", search_content)

        if search_content != "":
            # if the user has searched something
            # search a BaseQuery obj that contains a list of model types (by name)
            mt_bq_lst = search_models_by_keyword(keyword=search_content)
            # (serial_prefix e.g. b1-c1-t1-a1)
            mt_lst = mt_bq_lst.join(Product).filter(Product.serial_prefix.like("{}-{}-{}-{}".format(filter_b, filter_c, filter_t, filter_a))).all()

            # search model type by brand name
            brand_lst = Brand.query.filter(Brand.name.contains(search_content)).all()

            # merge the search results
            for brand in brand_lst:
                for p in brand.products.filter(Product.serial_prefix.like("{}-{}-{}-{}".format(filter_b, filter_c, filter_t, filter_a))):
                    for mt in p.model_types:
                        if mt not in set(mt_lst):
                            mt_lst.append(mt)

        else:
            # filter all the models according to the filters(check box)
            mt_lst = db.session.query(ModelType).join(Product).filter(Product.serial_prefix.like("{}-{}-{}-{}".format(filter_b, filter_c, filter_t, filter_a))).all()

        # print(mt_lst)

        """ sort the model list by the sale numbers """
        sort_db_models(mt_lst, sort_key=take_sales, reverse=True)

        """ structure the return data into a JSON dict """
        data = [mt.to_dict() for mt in mt_lst]

        # print(data)

        return jsonify({'returnValue': 0, 'data': data})

    return jsonify({'returnValue': 1})


'''
@main.route('/api/filter-model-types', methods=['POST'])
def filter_model_types():
    """
    (Using Ajax)
    filter the model types with their categories, brands, popularity, stock...
    If access_method == 'search', there will be 4 groups of filters
    If access_method == 'see_all', there will be 4 groups of filters
    If access_method == 'brand', there will be 3 groups of filters (except brand group)
    If access_method == 'cate', (! totally same as 'see_all') there will be 4 groups of filters (Initially the cate selected before will be checked automatically,
                                                        other 3 groups are checked as 'all' automatically at the initial stage)
    For the filter logic:
        elements inside a group are in the relation of 'or'
        elements in different groups are in the relation of 'and'
    """
    if request.method == 'POST':
        """ Get data from Ajax """
        # check has the user searched anything to get there, or just get there by 'see all', 'brand' or 'cate'
        access_method = request.form.get('access_method')

        # get JSON lists of filters
        json_list_c = request.form["JSON_list_C"]  # classification
        json_list_t = request.form["JSON_list_T"]  # Type
        json_list_a = request.form["JSON_list_A"]  # Additional
        # unpack json back to list
        c_id_list = json.loads(json_list_c)
        t_id_list = json.loads(json_list_t)
        a_id_list = json.loads(json_list_a)
        if access_method != 'brand':
            json_list_b = request.form["JSON_list_B"]  # Brand
            b_id_list = json.loads(json_list_b)

        """ Filter the models with the date gotten """
        mt_lst = []  # for collecting the result mt
        if access_method == 'search':
            # get the search content
            search_content = request.form.get('search_content')
            # search a BaseQuery obj that contains a list of model types
            mt_bq_lst = search_models_by_keyword(keyword=search_content)

            # loop through all the model types
            product_cache = set()
            for mt in mt_bq_lst:
                # if this mt id under the same product of a former checked mt, we select it directly,
                # because, brand and cate are attributes of products
                if mt.product in product_cache:
                    mt_lst.append(mt)
                    # start to check next mt
                    continue

                # check the brand
                # only the mt of selected brand will be selected
                brand_set = {Brand.query.get(i) for i in b_id_list}
                if mt.product.brand not in brand_set:
                    # start to check next mt
                    continue

                is_collected = False
                for c_id in c_id_list:
                    for t_id in t_id_list:
                        for a_id in a_id_list:
                            # every three of the selected categories will form a group
                            id_lst = [c_id, t_id, a_id]
                            cate_lst = [Category.query.get(i) for i in id_lst]

                            # sort the categories of this product by is in ascending order, this can match the cate_lst
                            mt_cate_lst = mt.product.categories.all()
                            sort_db_models(mt_cate_lst, sort_key=take_id, reverse=False)

                            # check whether the cate list of this model type match this assembly
                            if mt_cate_lst == cate_lst:
                                # add to the result
                                mt_lst.append(mt)
                                # then we can start to check next model type
                                is_collected = True
                                break
                        if is_collected:
                            break
                    if is_collected:
                        break

        elif access_method == 'see_all' or access_method == 'cate':
            # get a list of selected brands
            brand_lst = [Brand.query.get(i) for i in b_id_list]

            # get a list of models of the products, which satisfy this 4 constrain groups (CTAB)
            for brand in brand_lst:
                mt_lst += filter_products_by_cate_groups(brand, c_id_list, t_id_list, a_id_list)

        elif access_method == 'brand':
            # get the brand name
            brand_name = request.form.get('brand_name')

            # get the brand obj by its name
            brand = Brand.query.filter_by(name=brand_name).first()

            # filter the products
            mt_lst = filter_products_by_cate_groups(brand, c_id_list, t_id_list, a_id_list)

        """ sort the model list by the sale numbers """
        sort_db_models(mt_lst, sort_key=take_sales, reverse=True)

        """ structure the return data into a JSON dict """
        data = [mt.to_dict() for mt in mt_lst]

        return jsonify({'returnValue': 0, 'data': data})

    return jsonify({'returnValue': 1})


def filter_products_by_cate_groups(brand, c_id_list, t_id_list, a_id_list) -> list:
    """
    This function filters the products in the given brand,
    which meet any kind of assemble constrains of three kinds of categories (C T A).
    *** e.g. ***
    c: 1, 2
    t: 23, 35
    a: 53, 54
    constrain groups:
        1, 23, 53
        1, 23, 54
        1, 35, 53
        1, 35, 54
        2, ...
        ...
    If one of the constrain groups is meet, the product will be selected!
    :param brand:   A db obj of Brand
    :param c_id_list:   A list of the classification ids (1-6)
    :param t_id_list:   A list of the Type ids (7-52)
    :param a_id_list:   A list of the additional ids (53-56)
    :return:    A list of model types that belong to the selected products
    """
    # get products of this brand
    product_lst = brand.products.filter_by(is_deleted=False)
    # loop through all the products to find the ones meet the constrain
    result_product_lst = []
    for product in product_lst:
        is_collected = False  # whether this product is collected into the result

        for c_id in c_id_list:
            for t_id in t_id_list:
                for a_id in a_id_list:
                    # every three of the selected categories will form a group
                    id_lst = [c_id, t_id, a_id]
                    cate_lst = [Category.query.get(i) for i in id_lst]

                    # sort the categories of this product by is in ascending order, this can match the cate_lst
                    p_cate_lst = product.categories.all()
                    sort_db_models(p_cate_lst, sort_key=take_id, reverse=False)

                    # check whether the cate list of this product match this assembly
                    if p_cate_lst == cate_lst:
                        # add this product to result
                        result_product_lst.append(product)
                        # then we can start to check next product
                        is_collected = True
                        break
                if is_collected:
                    break
            if is_collected:
                break

    # put all the models into a list
    mt_list = []
    for product in result_product_lst:
        mt_list += product.get_exist_model_types()

    return mt_list
'''


@main.route('/api/model-detail/validate-model-count', methods=['POST'])
def validate_model_count():
    """
        (Using Ajax)
        Validate the model account of a specific model in the **detail page** of this model.
        If the count is out of the bound of the stock, response will be send to the frontend by ajax.
        Everytime the count changed, frontend should send a ajax request to this function to validate the count.
    """
    if request.method == 'POST':
        # get the info from Ajax
        model_id = request.form.get('model_id')
        new_count = request.form.get('new_count')

        if model_id is None or new_count is None:
            current_app.logger.error("info are not gotten from Ajax")
            return jsonify({'returnValue': 1})

        model = ModelType.query.get(model_id)
        if model is None:
            current_app.logger.error("No such model with this id")
            return jsonify({'returnValue': 1})

        # check if the model runs out of the stock
        if model.stock <= 1:
            return jsonify({'returnValue': 4, 'countStatus': 'run out of the stock'})

        try:
            new_count = int(new_count)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'returnValue': 1})

        # new_count should larger than 0
        if new_count > 0:

            if new_count < model.stock:
                return jsonify({'returnValue': 0, 'countStatus': 'less'})
            elif new_count == model.stock:
                return jsonify({'returnValue': 2, 'countStatus': 'equal'})
            elif new_count > model.stock:
                return jsonify({'returnValue': 3, 'countStatus': 'exceed'})

    return jsonify({'returnValue': 1})


@main.route('/api/the-siren/switch-epidemic-mode', methods=['POST'])
@login_required_for_ajax()
@staff_only(is_ajax=True)
def switch_epidemic_mode():
    """
    (Using Ajax)
    This functions is for staffs to switch on or off the epidemic mode
    """
    if request.method == "POST":

        # check if the user has logged in
        if not current_user.is_authenticated:
            current_app.logger.warning("Someone attempt to switch the epidemic mode before login")
            return jsonify({'returnValue': 1})

        # check if the user is an staff
        if current_user.role_id == 1:
            current_app.logger.warning("Someone (Customer) attempt to switch the epidemic mode without Permission!")
            return jsonify({'returnValue': 1})

        # get "switch_to" status from Ajax (0 for false, 1 for true)
        switch_to = request.form.get("switch_to")

        if switch_to is None:
            current_app.logger.error("info are not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # get the unique instance of this shop
        siren = get_unique_shop_instance()

        # reverse the current switch of epidemic_mode_on
        if switch_to == '0':
            siren.epidemic_mode_on = False
            flash(_("Epidemic Mode turned off."))
        elif switch_to == '1':
            flash(_("Epidemic Mode turned on."))
            siren.epidemic_mode_on = True
        else:
            current_app.logger.error("wrong value of 'switch_to' from Ajax")
            return jsonify({'returnValue': 1})

        db.session.add(siren)
        db.session.commit()
        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


# customize test
# @main.route("/test-file-upload")
# def render_test_page():
#     return render_template('main/test-upload-file.html')
#
#
# @main.route('/api/test-get-file', methods=['POST'])
# def test_get_file():
#     """
#     (Using Ajax)
#     """
#     if request.method == 'POST':
#         # form_data = request.form.get('formData')
#         form_data = request.files.get('file')
#         print(form_data)
#
#         mt_id = request.form.get('mt_id')
#         print(mt_id)
#
#         return jsonify({'returnValue': 0})
#
#     return jsonify({'returnValue': 1})


@main.route('/api/upload-customization-texture-file', methods=['POST'])
@login_required_for_ajax()
@customer_only(is_ajax=True)
def customize_in_3d():
    """
    (Using Ajax)
    Customer can upload their own ideal texture for customizing the model type
    """
    if request.method == 'POST':
        """ 
            get the model type id 
        """
        mt_id = request.form.get('model_type_id')

        if mt_id is None:
            current_app.logger.error("This model type does not exist!")
            return jsonify({'returnValue': 1})

        try:
            mt_id = int(mt_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'returnValue': 1})

        # get the model type from db
        mt = ModelType.query.get(mt_id)

        if mt is None:
            current_app.logger.error("No such model type with this id!")
            return jsonify({'returnValue': 1})

        """ 
            get the customized texture file 
        """
        customized_tex_file = request.files.get('customized_texture_file')

        if customized_tex_file is None:
            current_app.logger.error("No texture uploaded!")
            return jsonify({'returnValue': 1})

        texture_filename = customized_tex_file.filename
        suffix = texture_filename.rsplit('.')[-1]

        # check the file type
        if suffix not in Config.ALLOWED_3D_MODEL_TEXTURE_SUFFIXES:
            current_app.logger.error("3d texture file type error!")
            # rollback the db
            db.session.rollback()
            return jsonify({'returnValue': 2, 'msg': "Failed! You should use '.png' file only."})  # alert suffix error!

        # make sure the name of 3d texture file is safe
        texture_filename = generate_safe_pic_name(texture_filename)

        # save 3d texture file in local directory
        texture_file_path = os.path.join(Config.threeD_customize_texture_dir, texture_filename).replace('\\', '/')
        customized_tex_file.save(texture_file_path)

        # save the reference in database
        t_path = 'upload/model_type/customization-textures'
        texture_ref_address = os.path.join(t_path, texture_filename).replace('\\', '/')

        """ 
            record into database 
        """
        # check if the current user has the previous customization history with this model type
        cus_history = Customization.query.filter_by(customer_id=current_user.id, model_type_id=mt.id).first()

        # does not have history with this model type
        if cus_history is None:
            new_customization = Customization(customer_id=current_user.id, model_type_id=mt.id, texture_address=texture_ref_address)
            db.session.add(new_customization)
            # recorde the id of the current customization
            customization_id = new_customization.id

        else:
            # has history customization
            # change the texture of this history customization
            cus_history.texture_address = texture_ref_address
            db.session.add(cus_history)
            # recorde the id of the current customization
            customization_id = cus_history.id

        db.session.commit()

        text_address = url_for("static", filename=texture_ref_address)
        return jsonify({'returnValue': 0, 'textureAddress': text_address, 'customizationId': customization_id})

    return jsonify({'returnValue': 1})
