import os
from urllib import parse

from flask import request, redirect, url_for, flash, render_template, current_app, jsonify
from flask_login import login_required, current_user
from flask_babel import _

from app import db
from app.decorators import customer_only, login_required_for_ajax
from app.models import Order, PremiumOrder
from app.payment import payment

from alipay import AliPay, AliPayConfig


@payment.route('/api/pay-for-order/instrument', methods=['POST'])
@login_required_for_ajax()
@customer_only(is_ajax=True)
def pay_for_order_instrument():
    """
        (Using Ajax)
        Pay for the order of instruments.
        Firstly, update the order info according to the order confirm page.
        Then call the Alipay API to pay for this order.
    """
    if request.method == 'POST':
        """ get order """
        # get the order id
        order_id = request.form.get('order_id')

        if order_id is None:
            current_app.logger.error("info are not gotten from Ajax")
            return jsonify({"returnValue": 1})

        # get order obj from db
        order = Order.query.get(order_id)

        """ order validations """
        # check if the order exists
        if order is not None:
            # check the status of this order (only "waiting for payment" is acceptable)
            if order.status_code != 0:
                current_app.logger.warning('Attempt to double pay!')
                flash(_("You cannot pay for the same order second time!"))
                return redirect(url_for('main.index'))

            # check is that order belongs to current user
            if order not in current_user.orders:
                current_app.logger.warning('Attempt to pay for others oder!')
                flash(_("This is not your order, you cannot pay for it!"))
                return redirect(url_for('main.index'))
        else:
            current_app.logger.warning('Order does not exist!')
            flash(_("Order does not exist!"))
            return redirect(url_for('main.index'))

        """ call Alipay API to get the payment_url """
        payment_url = pay_order(order_obj=order)
        return jsonify({"returnValue": 0, "paymentURL": payment_url})


@payment.route('/api/pay-for-order/premium', methods=['POST'])
@login_required_for_ajax()
@customer_only(is_ajax=True)
def pay_for_order_premium():
    """
        (Using Ajax)
        Pay for the order of premium membership.
        No need to update any info here.
    """
    if request.method == 'POST':
        p_order_id = request.form.get('p_order_id')

        if p_order_id is None:
            current_app.logger.error("p_order_id is not gotten from Ajax")
            return jsonify({"returnValue": 1})

        try:
            p_order_id = int(p_order_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({"returnValue": 1})

        """ get order """
        # get premiumOrder obj from db
        p_order = PremiumOrder.query.get(p_order_id)

        """ order validations """
        # check if the p_order exists
        if p_order is not None:
            # check the status of this order (only "waiting for payment" is acceptable)
            if p_order.is_paid:
                current_app.logger.warning('Attempt to double pay!')
                flash(_("You cannot pay for the same order second time!"))
                return redirect(url_for('main.index'))

            # check is that order belongs to current user
            if p_order.user_id != current_user.id:
                current_app.logger.warning('Attempt to pay for others premiumOder!')
                flash(_("This is not your premiumOrder, you cannot pay for it!"))
                return redirect(url_for('main.index'))
        else:
            current_app.logger.warning('premiumOrder does not exist!')
            flash(_("premiumOrder does not exist!"))
            return redirect(url_for('main.index'))

        """ call Alipay API to get the payment_url"""
        payment_url = pay_order(order_obj=p_order)
        return jsonify({"returnValue": 0, "paymentURL": payment_url})
    return jsonify({"returnValue": 1})


def pay_order(order_obj):
    """
    This function calls the Alipay API, get a payment url (for going to alipay)
    :param order_obj: A obj of order from db
    :return: a String of payment url (for going to alipay)
    """

    # create a alipay obj
    alipay = get_alipay_instance()

    # check the type if the payment (P or I)
    if order_obj.out_trade_no[0] == 'I':
        subject = "Musical Instruments"
        # For web on PC (production), we need to redirect to：https://openapi.alipay.com/gateway.do? + order_string
        # For sandbox environment (development): https://openapi.alipaydev.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_obj.out_trade_no,    # trade number, which should be unique inside a same retailer
            total_amount=order_obj.paid_payment,    # total amount of the order should pay (unit:'yuan (RMB)')
            subject=subject,    # subject of this order
            return_url=url_for('payment.payment_finished', _external=True),   # where to go after the payment
            notify_url=None  # not usable, so I used another method to replace this
        )

    elif order_obj.out_trade_no[0] == 'P':
        subject = "Premium membership for SIREN"
        # For web on PC (production), we need to redirect to：https://openapi.alipay.com/gateway.do? + order_string
        # For sandbox environment (development): https://openapi.alipaydev.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_obj.out_trade_no,  # trade number, which should be unique inside a same retailer
            total_amount=order_obj.payment,  # total amount of the order (unit:'yuan (RMB)')
            subject=subject,  # subject of this order
            return_url=url_for('payment.payment_finished', _external=True),  # where to go after the payment
            notify_url=None  # not usable, so I used another method to replace this
        )

    else:
        current_app.logger.warning('wrong order!')
        return redirect(url_for('main.index'))

    # redirect to the page of alipay
    payment_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

    # return redirect(payment_url)
    return payment_url


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
@login_required
@customer_only()
def payment_finished():
    """
    Render the page of 'payment finished',
    everytime the payment finished, user will be redirected to there.
    """
    return render_template('order/payment-success.html')


@payment.route('/api/payment-notify', methods=['POST'])
@login_required_for_ajax()
@customer_only(is_ajax=True)
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
        is_from_ali = alipay.verify(alipay_notify_data, signature)
        if is_from_ali:
            print("---------------> trade data from alipay!")

            # get the data we need
            out_trade_no = alipay_notify_data.get('out_trade_no')
            trade_no = alipay_notify_data.get('trade_no')  # trade number generated by alipay, which could be used for refund etc.

            # get the payment type (P or I) from out_trade_no
            payment_type = out_trade_no[0]

            # 'payment of instruments'
            if payment_type == 'I':
                # get the db order id from out_trade_no
                # we have stored it in the second position in out_trade_no
                # e.g. I_2_xx
                order_id = out_trade_no[:out_trade_no.find('_', out_trade_no.find('_')+1)][2:]

                try:
                    order_id = int(order_id)
                except Exception as e:
                    current_app.logger.error(e)
                    return 'failure'

                # update the info
                try:
                    # order
                    order = Order.query.get(order_id)
                    order.out_trade_no = out_trade_no
                    order.trade_no = trade_no
                    order.status_code = 1
                    db.session.add(order)
                    # user
                    user = order.user
                    user.exp += 60
                    db.session.add(user)
                    db.session.commit()
                    # update the info of models in this order (stock, sales ... )
                    order.update_model_info()

                except Exception as e:
                    # record error into log file
                    current_app.logger.error(e)
                    # rollback the db operation
                    db.session.rollback()

                return 'success'

            # payment of premiums
            elif payment_type == 'P':
                # get the db premium_order id from out_trade_no
                # we have stored it in the second position in out_trade_no
                # e.g. P_2_xx
                premium_order_id = out_trade_no[:out_trade_no.find('_', out_trade_no.find('_') + 1)][2:]

                try:
                    premium_order_id = int(premium_order_id)
                except Exception as e:
                    current_app.logger.error(e)
                    return 'failure'

                # update the premium order and the user premium info
                try:
                    # premiumOrder
                    p_order = PremiumOrder.query.get(premium_order_id)
                    p_order.trade_no = trade_no
                    p_order.is_paid = True
                    db.session.add(p_order)
                    # user
                    user = p_order.user
                    user.is_premium = True
                    user.premium_left_days += p_order.duration
                    user.exp += 230
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    current_app.logger.error(e)
                    db.session.rollback()

                return 'success'

            else:
                current_app.logger.error('no such type of payment!')
                return 'failure'

        else:
            current_app.logger.warning('payment failed!')
            return 'failure'
