from flask import render_template, request, redirect, url_for
from sqlalchemy import and_

from . import main
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
    all_products = Product.query.all()
    return render_template('', is_plist=True, all_products=all_products)   # see-all page


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
        return render_template('',  is_plist=False, mt_list=mt_list)  # see-all page

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
    product_lst = cate.products.all()
    return render_template('', is_plist=True, product_lst=product_lst)  # see-all page



@main.route('/products-in-brand/<brand_name>')
def products_in_brand(brand_name):
    """
        Go to the see-all page with the constrain of a specific brand
    """
    # get the brand obj by its name
    brand = Brand.query.filter_by(name=brand_name).first()
    product_lst = brand.products.all()
    return render_template('', is_plist=True, product_lst=product_lst)  # see-all page


@main.route('/my-cart')
def my_cart():
    """
        showing the page of "my shopping cart" of current user
    """
    pass


@main.route('/my-orders')
def my_orders():
    """
        showing the page of "my orders" of current user
    """
    pass


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------
@main.route('/api/change-theme', methods=['POST'])
def change_theme():
    pass


@main.route('/api/cart/update-product-count', methods=['POST'])
def update_product_count():
    """
            update the product account of a specific cart relation, which is about
            current user and the given product
    """
    pass


@main.route('/api/cart/remove-cart-relation', methods=['POST'])
def remove_cart_relation():
    """
        remove a specific cart relation according to the cart_id
        (remove a product from shopping cart)
    """
    pass


@main.route('/api/cart/purchase_cart', methods=['POST'])
def purchase_cart():
    """
        get a list of id of cart relations that should be purchased.
        we should remove them from database - Cart table and add the records
        into the History table.
    """
    pass


