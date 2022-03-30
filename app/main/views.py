from flask import render_template, request, redirect, url_for, session, jsonify, flash, json
from flask_login import login_required, current_user
from sqlalchemy import and_

from . import main
from .. import db
from ..models import Product, ModelType, Category, Brand


@main.route('/index')
def index():
    """
        The function is for rendering the real index page
    """

    """  """
    return render_template('main/index_new.html')


@main.route('/')
@main.route('/index_test', methods=['GET', 'POST'])
def index_test():
    """
        The function for rendering the fake index page
    """
    return render_template('main/index_test.html')


@main.route('/')
def go_all():
    """
        The function for going to see all the products (model types).
        (Namely, a see-all-function without any filters)
    """
    # order the models by their popularity
    all_model_type = ModelType.query.filter_by(is_deleted=False) \
        .order_by(ModelType.sales.desc(), ModelType.views.desc()) \
        .all()
    return render_template('', mt_list=all_model_type)  # see-all page


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
        mt_list = search_models_by_keyword(keyword=key_word)\
            .order_by(ModelType.sales.desc(), ModelType.views.desc())\
            .all()
        return render_template('', mt_list=mt_list)  # see-all page

    return redirect(url_for('main.index'))


def search_models_by_keyword(keyword):
    """
    This function searches a list of model which contains given keyword in their name
    :param keyword: A string of key word
    :return: A BaseQuery object that contains a list of models found
    """
    mt_bq_lst = ModelType.query.filter(and_(ModelType.name.contains(keyword),
                                          ModelType.is_deleted == False))
    return mt_bq_lst


@main.route('/user_profile/<username>')
def user_profile(username):
    pass


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    pass


@main.route('/products-in-category/<category_name>')
def products_in_category(category_name):
    """
        Go to the see-all page with the constrain of a specific category
    """
    # get the category obj by its name
    cate = Category.query.filter_by(name=category_name).first()
    # get products under this cate
    product_lst = cate.products.filter_by(is_deleted=False).all()
    # put all the models into a list
    mt_list = []
    for product in product_lst:
        mt_list += product.get_exist_model_types()
    # sort these models by their sale
    sort_db_models(mt_list, sort_key=take_sales, reverse=True)
    return render_template('', mt_list=mt_list)  # see-all page


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


@main.route('/products-in-brand/<brand_name>')
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
    return render_template('', mt_list=mt_list)  # see-all page


@main.route('/product-details/<int:mt_id>')
def model_type_details(mt_id):
    """
    Rendering the page of 'Mode Type details'
    :param mt_id: The id of the selected model type
    """
    # get the model type by id
    mt = ModelType.query.get(mt_id)
    # check if the model type exists
    if mt is not None:
        return render_template('', model_type=mt)
    else:
        flash('No such commodity!')
        return redirect(url_for('main.index_new'))


@main.route('/change_language', methods=['GET', 'POST'])
def change_language():
    # if the user already logged in, we change language setting both in db and session
    if current_user.is_authenticated:
        # change setting in db
        if current_user.language == 'en':
            current_user.language = 'zh'
        elif current_user.language == 'zh':
            current_user.language = 'en'

        db.session.add(current_user)
        db.session.commit()

        # change setting in session
        session["language"] = current_user.language

    else:
        # if the user is anonymous, we only change the language setting in session

        # if the first time access the website, we should init the session of language first
        if session.get("language") is None:
            session["language"] = 'en'

        # change setting in the session
        if session["language"] == 'zh':
            session["language"] = 'en'
        elif session["language"] == 'en':
            session["language"] = 'zh'

    return render_template('main/index_new.html')


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------


@main.route('/api/change-theme', methods=['POST'])
def change_theme():
    pass


@main.route('/api/cart/purchase_cart', methods=['POST'])
def purchase_cart():
    """
        get a list of id of cart relations that should be purchased.
        we should remove them from database - Cart table and add the records
        into the History table.
    """
    pass


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
        mt_lst = []     # for collecting the result mt
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
        model_id = int(request.form['model_id'])
        new_count = int(request.form['new_count'])

        # new_count should larger than 0
        if new_count > 0:
            # get the model obj form db
            model = ModelType.query.get(model_id)

            if model:
                if new_count < model.stock:
                    return jsonify({'returnValue': 0, 'countStatus': 'less'})
                elif new_count == model.stock:
                    return jsonify({'returnValue': 0, 'countStatus': 'equal'})
                elif new_count > model.stock:
                    return jsonify({'returnValue': 0, 'countStatus': 'exceed'})

    return jsonify({'returnValue': 1})
