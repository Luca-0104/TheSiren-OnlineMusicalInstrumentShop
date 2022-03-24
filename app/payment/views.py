from flask_login import login_required

from app.payment import payment


@payment.route('/pay-for-order')
@login_required
def pay_for_order():
    """
        Get an order obj as the parameter, then render the payment-method-choosing page
    """
    pass
