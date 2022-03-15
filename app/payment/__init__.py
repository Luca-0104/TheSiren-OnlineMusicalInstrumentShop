from flask import Blueprint

# Create a Blueprint class object called payment, set the blueprint name as 'payment'
payment = Blueprint('payment', __name__)

from . import pay_alipay