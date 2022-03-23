from flask import render_template

from . import main


@main.route('/index-real')
def index_real():
    """
        The function is for test the real index
    """
    return render_template('main/index_new.html')


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    """
        The function for rendering the main page
    """
    return render_template('main/index_test.html')


@main.route('/search/<keywords>')
def search(keywords):
    """
    Search the specific product model types according to the user input
    :param keywords: The keywords that the users inputted for searching
    """
    pass


@main.route('/user_profile/<username>')
def user_profile(username):
    pass


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    pass


@main.route('/products-in-category/<category_name>')
def products_in_category(category_name):
    pass


@main.route('/products-in-brand/<brand_name>')
def products_in_brand(brand_name):
    pass


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


@main.route('/api/cart/purchase', methods=['POST'])
def purchase():
    """
        get a list of id of cart relations that should be purchased.
        we should remove them from database - Cart table and add the records
        into the History table.
    """
    pass

