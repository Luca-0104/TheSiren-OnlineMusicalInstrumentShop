import os

import random
from datetime import datetime

from alipay import AliPay, AliPayConfig
from flask import session, redirect, url_for

from config import DevelopmentConfig
from . import payment


@payment.route("/pay_order", methods=["POST", "GET"])
def pay_order():
    """
    This is only for testing and adjustment now.
    The one being adopted is in views.py
    """
    # initialize the files of keys
    dir_app_private_key_string = os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem")
    dir_alipay_public_key_string = os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem")

    app_private_key_string = open(dir_app_private_key_string).read()
    alipay_public_key_string = open(dir_alipay_public_key_string).read()


    # create an object of Alipay sdk (initialize the Alipay)
    alipay = AliPay(
        appid="2021000119628595",
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True,  # 默认 False
        verbose=False,  # 输出调试数据
        config=AliPayConfig(timeout=15)  # 可选，请求超时时间
    )

    subject = "测试订单"
    test_out_trade_no = "{}_{}_{}".format(1, str(datetime.utcnow()).replace(" ", "").replace(":", "").replace('-', '').replace('.', ''), random.randint(1, 99999999999))

    # For web on PC (production), we need to redirect to：https://openapi.alipay.com/gateway.do? + order_string
    # For sandbox environment (development): https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=test_out_trade_no,    # trade number, which should be unique inside a same retailer
        total_amount=0.01,  # total amount of the order (unit:'cent')
        subject=subject,    # subject of this order
        return_url=url_for('payment.payment_finished', _external=True),   # where to go after the payment
        notify_url=None  # 可选，不填则使用默认 notify url
    )

    # redirect to the page of alipay
    payment_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

    return redirect(payment_url)
