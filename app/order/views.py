from flask import render_template

from . import order


@order.route('/order_confirm')
def order_confirm():
    """
        The function is for test the real index
    """
    return render_template('order/order-confirm.html')