from flask import render_template, request, redirect, url_for, session, jsonify
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
    all_products = Product.query.filter_by(is_deleted=False).all()
    return render_template('', is_plist=True, all_products=all_products)  # see-all page


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
        mt_list = ModelType.query.filter(and_(ModelType.name.contains(key_word),
                                              ModelType.is_deleted == False)).order_by(ModelType.product_id).all()
        return render_template('', is_plist=False, mt_list=mt_list)  # see-all page

    return redirect(url_for('main.index'))


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
    product_lst = cate.products.filter_by(is_deleted=False).all()
    return render_template('', is_plist=True, product_lst=product_lst)  # see-all page


@main.route('/products-in-brand/<brand_name>')
def products_in_brand(brand_name):
    """
        Go to the see-all page with the constrain of a specific brand
    """
    # get the brand obj by its name
    brand = Brand.query.filter_by(name=brand_name).first()
    product_lst = brand.products.filter_by(is_deleted=False).all()
    return render_template('', is_plist=True, product_lst=product_lst)  # see-all page


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


@main.route('/my-cart')
def my_cart():
    """
        showing the page of "my shopping cart" of current user
    """
    return render_template('')


@main.route('/my-orders')
def my_orders():
    """
        showing the page of "my orders" of current user
    """
    return render_template('')


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
    :return:
    """
    if request.method == 'POST':
        # check has the user searched anything to get there, or just get there by 'see all', 'brand' or 'cate'
        access_method = request.form.get('access_method')

        if access_method == 'search':
            # get the search content
            pass
        elif access_method == 'see_all':
            pass
        elif access_method == 'brand':
            # get the brand name
            pass
        elif access_method == 'cate':
            # get the cate name
            pass



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

