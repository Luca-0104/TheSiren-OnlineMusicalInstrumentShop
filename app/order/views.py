from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, json, flash, jsonify, current_app
from flask_babel import _

from app import db
from app.models import Cart, Order, OrderModelType, ModelType, PremiumOrder
from app.order import order

from datetime import datetime


# -------------------------------------- generate orders --------------------------------------

@order.route('/generate-order-from-cart', methods=['GET', 'POST'])
@login_required
def generate_order_from_cart():
    """
        (Using Ajax)
        Get a list of cart relation objs from frontend.
        Generate a new order obj first.
        Then generate several OrderModelType objs according to the cart objs.
        Then link those OrderModelType objs in to that order obj
    """
    if request.method == 'POST':
        # get the cart_id_list in from of JSON string list
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
                    new_omt = OrderModelType(order=new_order, model_type=cart.model_type, count=cart.count,
                                             unit_pay=cart.model_type.price)
                    db.session.add(new_omt)
                db.session.commit()

                # generate related payment amount
                new_order.generate_delivery_fee()
                new_order.generate_gross_payment()
                # generate out_trade_no for this order, as it is created
                new_order.generate_unique_out_trade_no()

                flash(_('Order created!'))
                return jsonify({'returnValue': 0, 'order_id': new_order.id})
                # return redirect(url_for('order.order_confirm', order_id=new_order.id))

    flash(_('Order generation failed!'))
    return jsonify({'returnValue': 1})
    # return redirect(url_for('main.index'))


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

            # generate related payment amount
            new_order.generate_delivery_fee()
            new_order.generate_gross_payment()
            # generate out_trade_no for this order, as it is created
            new_order.generate_unique_out_trade_no()

            flash(_('Order created!'))
            return jsonify({'returnValue': 0, 'order_id': new_order.id})
            # return redirect(url_for('order.order_confirm', order_id=new_order.id))

    # flash('Order generation failed!')
    # return redirect(url_for('main.index'))
    return jsonify({'returnValue': 1})


@order.route('/order-confirm/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order_confirm(order_id):
    """
        This function is for rendering the page of order confirmation.
    """
    o = Order.query.get(order_id)
    # check if that order belong to current user
    if o in current_user.orders:
        return render_template('order/order-confirm.html', order=o)
    else:
        flash(_('Permission denied!'))
        return redirect(url_for('main.index'))



# -------------------------------------- view my orders --------------------------------------

@order.route('/my-orders')
@login_required
def my_orders():
    """
    For rendering the page of 'my orders'
    and pass all the orders of this user to the frontend
    """
    # order the orders by their timestamps
    order_lst = current_user.orders.order_by(Order.timestamp.desc()).all()
    return render_template('order/order-listing.html', order_lst=order_lst)


@order.route('/order-details/<int:order_id>')
@login_required
def order_details(order_id):
    """
    Rendering the page of order details
    :param order_id: The id of the selected order
    """
    order_obj = Order.query.get(order_id)
    return render_template('order/order-detail.html', order_obj=order_obj)


@order.route('/api/order/my-orders/filter-orders', methods=['POST'])
@login_required
def filter_orders():
    """
    (Using ajax)
    Query the order objs in given status and
    return them in the form of JSON dict
    """
    if request.method == 'POST':
        print("here")
        # get status code from Ajax
        status_code = int(request.form.get('status_code'))
        print(status_code)

        if status_code == -1:
            # query all the orders of current user
            order_lst = current_user.orders.order_by(Order.timestamp.desc()).all()
        else:
            # query the order object by status_code and current user
            order_lst = current_user.orders.filter_by(status_code=status_code).order_by(Order.timestamp.desc()).all()

        # turn objects into a list of dicts
        data = [o.to_dict() for o in order_lst]

        print(data)

        return jsonify({'returnValue': 0, 'data': data})

    return jsonify({'returnValue': 1})


@order.route('/api/order/my-orders/change-status', methods=['POST'])
@login_required
def change_status():
    """
    (Using Ajax)
        --- status code table ---
        0:"waiting for payment",
        1:"preparing"
        2:"on delivery",
        3:"waiting for collection",
        4:"finished",
        5:"canceled"
        6:"expired

        --- permission ---
        customers -> {(2->)4, 5}
        staff     -> {2, 3, (3->)4, 5}
    """
    if request.method == 'POST':
        # get data from Ajax
        new_code = int(request.form.get('new_code'))
        order_id = int(request.form.get('order_id'))

        # get the order by id
        o = Order.query.get(order_id)

        # check if the order exists
        if o is None:
            return jsonify({'returnValue': 1})

        # get current status code
        current_code = o.status_code

        # specify the permissions
        perm_cus = {4, 5}
        perm_staff = {2, 3, 4, 5}

        # check the role of the current user
        # customer
        if current_user.role_id == 1:
            # check if the oder is belong to this user
            if o.user_id == current_user.id:
                # check the permission
                if new_code in perm_cus:
                    # customer can only change the status to 'finished' when it is 'on delivery'
                    if new_code == 4 and current_code != 2:
                        return jsonify({'returnValue': 2, 'msg': 'Permission denied!'})
                    # update status
                    o.status_code = new_code
                    # record the time of status changing
                    if new_code == 4:
                        o.timestamp_4 = datetime.utcnow()
                    elif new_code == 5:
                        o.timestamp_5 = datetime.utcnow()
                    db.session.add(o)
                    db.session.commit()
                    return jsonify({'returnValue': 0})
                else:
                    return jsonify({'returnValue': 2, 'msg': 'Permission denied!'})
            else:
                return jsonify({'returnValue': 2, 'msg': 'Permission denied!'})

        # staff
        elif current_user.role_id == 2:
            # check the permission
            if new_code in perm_staff:
                # staff can only change the status to 'finished' when it is 'waiting for collection'
                if new_code == 4 and current_code != 3:
                    return jsonify({'returnValue': 2, 'msg': 'Permission denied!'})
                # update status
                o.status_code = new_code
                # record the time of status changing
                if new_code == 2:
                    o.timestamp_2 = datetime.utcnow()
                elif new_code == 3:
                    o.timestamp_3 = datetime.utcnow()
                elif new_code == 4:
                    o.timestamp_4 = datetime.utcnow()
                elif new_code == 5:
                    o.timestamp_5 = datetime.utcnow()
                db.session.add(o)
                db.session.commit()
                return jsonify({'returnValue': 0})
            else:
                return jsonify({'returnValue': 2, 'msg': 'Permission denied!'})

    return jsonify({'returnValue': 1})


# -------------------------------------------- Premium orders --------------------------------------------

@order.route('/api/generate-premium-order', methods=['POST'])
@login_required
def generate_premium_order():
    """
    (Using Ajax)
    This function works like the function 'order_confirm'.
    For the premium order, we order generation and confirm can be integrated together,
    because no status of "waiting for payment" for premium orders.
    :return:
    """
    if request.method == 'POST':
        # get order info from Ajax
        duration = request.form.get('duration')  # how many days
        payment = request.form.get('payment')

        # validate the info we get
        if duration:
            try:
                duration = int(duration)
            except Exception as e:
                current_app.logger.error(e)
                flash(_("Error in Duration info!"))
                return redirect(url_for('main.index'))
        else:
            current_app.logger.warning('Duration is None!')
            flash(_("No duration info!"))
            return redirect(url_for('main.index'))

        if payment:
            try:
                payment = int(payment)
            except Exception as e:
                current_app.logger.error(e)
                flash(_("Error in payment info!"))
                return redirect(url_for('main.index'))
        else:
            current_app.logger.warning('Payment is None!')
            flash(_("No payment info!"))
            return redirect(url_for('main.index'))

        # create a new premium order
        new_p_order = PremiumOrder(user=current_user, duration=duration, payment=payment)
        db.session.add(new_p_order)
        db.session.commit()

        # start process of Alipay
        return redirect(url_for('payment.pay_for_order_premium', p_order_id=new_p_order.id))
