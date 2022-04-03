import os
from urllib import parse

from flask import request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user

from app import db
from app.models import Order
from app.payment import payment

from alipay import AliPay, AliPayConfig


@payment.route('/pay-for-order', methods=['POST'])
@login_required
def pay_for_order():
    """
        Firstly, update the order info according to the order confirm page.
        Then call the Alipay API to pay for this order.
    """
    if request.method == 'POST':
        """ get order """
        # get the order id
        order_id = int(request.form.get('order_id'))
        # get order obj from db
        order = Order.query.get(order_id)

        """ order validations """
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

        """ update order information """
        order_type = request.form.get('order_type')
        address_id = int(request.form.get('address_id'))
        order.order_type = order_type
        order.address_id = address_id
        db.session.add(order)
        db.session.commit()

        """ call Alipay API """
        pay_order(order_obj=order)

        """ update order status """


def pay_order(order_obj):
    """
    This function calls the Alipay API, to finish the payment
    :param order_obj: A obj of order from db
    """

    # create a alipay obj
    alipay = get_alipay_instance()

    subject = "Musical Instruments"

    # For web on PC (production), we need to redirect to：https://openapi.alipay.com/gateway.do? + order_string
    # For sandbox environment (development): https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_obj.out_trade_no,    # trade number, which should be unique inside a same retailer
        total_amount=order_obj.gross_payment,  # total amount of the order (unit:'yuan (RMB)')
        subject=subject,    # subject of this order
        return_url=url_for('payment.payment_finished', _external=True),   # where to go after the payment
        notify_url=None  # not usable, so I used another method to replace this
    )

    # redirect to the page of alipay
    payment_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

    return redirect(payment_url)


def get_alipay_instance():
    """
    This function return an instance of the Alipay.
    :return: An instance of Alipay
    """
    # initialize the files of keys
    dir_app_private_key_string = os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem")
    dir_alipay_public_key_string = os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem")

    app_private_key_string = open(dir_app_private_key_string).read()
    alipay_public_key_string = open(dir_alipay_public_key_string).read()

    # create an object of Alipay sdk (initialize the Alipay)
    alipay = AliPay(
        appid="2021000119628595",
        app_notify_url=None,  # not usable, so I used another method to replace this
        app_private_key_string=app_private_key_string,  # This is the private key of our app
        alipay_public_key_string=alipay_public_key_string,  # This is the public key from Alipay, used for call back notification
        sign_type="RSA2",  # we can choose from RSA and RSA2, and RSA2 is more secure
        debug=True,  # When using sandbox environment, I can turn this on
        verbose=False,  # Should we print out the debug msg in the terminal
        config=AliPayConfig(timeout=15)  # The expire time length of requesting
    )

    return alipay


@payment.route('/payment-finished', methods=['GET'])
def payment_finished():
    """
    Render the page of 'payment finished',
    everytime the payment finished, user will be redirected to there.
    """
    return render_template('backend-test/payment/payment-finished.html')


@payment.route('/api/payment-notify', methods=['POST'])
def payment_notify():
    """
    (Using Ajax)
    Everytime after paying, there is a GET request sent by Alipay carrying the notification data to the 'return_url',
    this data should be sent back to backend using Ajax.
    This function is for receiving the notification data and then update the status of the order.
    """
    print("---------------> here in notify")
    if request.method == 'POST':
        # get notification data from Ajax
        alipay_notify_data = request.form.get('notify_data')

        alipay_notify_data = dict(parse.parse_qsl(parse.urlsplit(alipay_notify_data).query))
        print(alipay_notify_data)

        # extract the data we need
        signature = alipay_notify_data.pop("sign")

        # create a alipay instance with the same parameters
        alipay = get_alipay_instance()

        # check if the data comes from Alipay
        is_success = alipay.verify(alipay_notify_data, signature)
        if is_success:
            print("---------------> trade succeed")

            # get the data we need
            out_trade_no = alipay_notify_data.get('out_trade_no')
            trade_no = alipay_notify_data.get('trade_no')  # trade number generated by alipay, which could be used for refund etc.

            # get the db order id from out_trade_no
            # we have stored it in the first position in out_trade_no
            order_id = int(out_trade_no[:out_trade_no.find('_')])

            # update the order
            try:
                order = Order.query.get(order_id)
                order.out_trade_no = out_trade_no
                order.trade_no = trade_no
                order.status_code = 1
                db.session.add(order)
                db.session.commit()

            except Exception as e:
                # record error into log file
                current_user.logger.error(e)
                # rollback the db operation
                db.session.rollback()

            return 'success'
        else:
            return 'failure'



