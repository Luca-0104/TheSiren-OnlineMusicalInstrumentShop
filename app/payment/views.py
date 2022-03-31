from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import Order
from app.payment import payment


@payment.route('/pay-for-order', methods=['POST'])
@login_required
def pay_for_order():
    """
        Firstly, update the order info according to the order confirm page.
        Then call the Alipay API to pay for this order.
    """
    if request.method == 'POST':
        # get the order id
        order_id = int(request.form.get('order_id'))
        # get order obj from db
        order = Order.query.get(order_id)

        # check if the order exists
        if order is not None:
            # check the status of this order (only "waiting for payment" is acceptable)
            if order.status_code != 0:
                flash("You cannot pay for the same order second time!")
                return redirect(url_for('main.index'))

            # check is that order belongs to current user
            if order not in current_user.orders:
                flash("This is not your order, you cannot pay for it!")
                return redirect(url_for('main.index'))
        else:
            flash("Order does not exist!")
            return redirect(url_for('main.index'))

        # update the order information
        request.form.get('')

        pass





