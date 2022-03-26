from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, json, flash, jsonify

from app import db
from app.models import Cart, Order, OrderModelType, ModelType
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
        print("here")
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

                flash('Order created!')
                return redirect(url_for('order.order_confirm', order_id=new_order.id))

    flash('Order generation failed!')
    return redirect(url_for('main.index'))


@order.route('/generate-order-from-buy-now/<int:model_id>/<int:count>', methods=['GET'])
@login_required
def generate_order_from_buy_now(model_id, count):
    """
    Get the id of model type, get the count of this model.
    Generate a order obj and its OrderModelType obj
    :param model_id: which model type
    :param count: how many
    """
    # get model obj from db
    model = ModelType.query.get(model_id)
    if model:
        # check stock number
        if count <= model.stock:

            # generate the order obj
            new_order = Order(status_code=0, user_id=current_user.id)
            db.session.add(new_order)
            db.session.commit()

            # add this model in to this order
            new_omt = OrderModelType(order=new_order, model_type=model, count=count, unit_pay=model.price)
            db.session.add(new_omt)
            db.session.commit()

            flash('Order created!')
            return redirect(url_for('order.order_confirm', order_id=new_order.id))

    flash('Order generation failed!')
    return redirect(url_for('main.index'))


@order.route('/order_confirm/<int:order_id>')
@login_required
def order_confirm(order_id):
    """
        This function is for rendering the page of order confirmation.
    """
    return render_template('order/order-confirm.html', order_id=order_id)