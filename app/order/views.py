from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, json, flash

from app import db
from app.models import Cart, Order, OrderModelType
from app.order import order


@order.route('/generate-order-from-cart', methods=['GET', 'POST'])
@login_required
def generate_order_from_cart():
    """
        Get a list of cart relation objs from frontend.
        Generate a new order obj first.
        Then generate several OrderModelType objs according to the cart objs.
        Then link those OrderModelType objs in to that order obj
    """
    if request.method == 'POST':
        # get the cart_id_list from ajax
        list_json = request.form["JSON_cart_list"]

        if list_json:
            # unpack json back to list
            cart_id_list = json.loads(list_json)

            if len(cart_id_list) > 0:
                # Create a new order
                new_order = Order(status_code=0, user_id=current_user.id)
                db.session.add(new_order)
                db.session.commit()

                # Add the models that the user has chosen into this order
                for cart_id in cart_id_list:
                    cart = Cart.query.get(cart_id)
                    new_omt = OrderModelType(order=new_order, model_type=cart.model_type, count=cart.count, unit_pay=cart.model_type.price)
                    db.session.add(new_omt)
                db.session.commit()

                return redirect(url_for('order.order_confirm', order_id=new_order.id))

    flash('Order generation failed!')
    return redirect(url_for('main.index'))


@order.route('/generate-order-from-single', methods=['GET'])
@login_required
def generate_order_from_single():
    """
        Get the id of model type, get the count of this model.
        Generate a order obj and its OrderModelType obj
    """
    # return redirect(url_for('order.order_confirm', order_id=))


@order.route('/order_confirm/<int:order_id>')
@login_required
def order_confirm(order_id):
    """
        This function is for rendering the page of order confirmation.
    """
    return render_template('order/order-confirm.html')
