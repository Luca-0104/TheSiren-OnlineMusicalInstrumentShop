from flask_login import login_required

from app.order import order


@order.route('/generate-order-from-cart')
@login_required
def generate_order_from_cart():
    """
        Get a list of cart relation objs from frontend.
        Generate a new order obj first.
        Then generate several OrderModelType objs according to the cart objs.
        Then link those OrderModelType objs in to that order obj
    """
    pass


@order.route('/generate-order-from-single')
@login_required
def generate_order_from_single():
    """
        Get the id of model type, get the count of this model.
        Generate a order obj and its OrderModelType obj
    """
    pass
from flask import render_template

from . import order


@order.route('/order_confirm')
def order_confirm():
    """
        The function is for test the real index
    """
    return render_template('order/order-confirm.html')