from flask import request, jsonify, render_template, current_app, flash
from flask_login import current_user, login_required
import json

from app import db
from app.cart import cart
from app.decorators import customer_only
from app.main import main
from app.models import Cart, ModelType


@cart.route('/show-my-cart')
@login_required
@customer_only()
def show_my_cart():
    """
        for rendering the page of "my shopping cart"
    """
    cart_relation_lst = current_user.carts.all()
    length = len(cart_relation_lst)
    return render_template('cart/page-cart.html', cart_relation_lst=cart_relation_lst, length=length)


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------


@cart.route('/api/cart/add-to-cart', methods=['POST'])
@login_required
@customer_only()
def add_to_cart():
    """
    (Using Ajax)
    This function adds the model into the cart with specific count
    """
    if request.method == 'POST':
        model_id = request.form.get("model_id")
        count = request.form.get("count")

        if count is None or model_id is None:
            current_app.logger.error("info not gotten from Ajax")
            return jsonify({'returnValue': 1})

        try:
            count = int(count)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'returnValue': 1})

        # get model obj from db
        model = ModelType.query.get(model_id)
        if model and model.is_deleted == False:
            # check stock number
            if count <= model.stock:
                # check if (this model + this user) already in database
                exist_cart = Cart.query.filter_by(model_type=model, user=current_user).first()
                if exist_cart:
                    # update the count
                    exist_cart.count += count
                    db.session.add(exist_cart)
                    db.session.commit()
                    response_cart_id = exist_cart.id
                else:
                    # create a new cart relation
                    new_cart = Cart(user=current_user, model_type_id=model_id, count=count)
                    db.session.add(new_cart)
                    db.session.commit()
                    response_cart_id = new_cart.id

                flash("Add to cart successful!")
                return jsonify({"returnValue": 0, "cartID": response_cart_id})

            else:
                flash("This item runs out of stock!")
    return jsonify({"returnValue": 1})



@cart.route('/api/cart/update-cart-count', methods=['POST'])
@login_required
@customer_only()
def update_cart_count():
    """
        (Using Ajax)
        update the model account of a specific cart relation, which is about
        current user and the given product
    """
    if request.method == 'POST':
        # get the info from Ajax
        model_id = int(request.form['model_id'])
        new_count = int(request.form['new_count'])

        # new_count should larger than 0
        if new_count > 0:
            # find the instance of the given cart relation from db
            cart_relation = Cart.query.filter_by(user_id=current_user.id, model_type_id=model_id).first()

            # check whether the cart relation exists
            if cart_relation:
                # check if the stock is enough
                model = ModelType.query.get(model_id)

                # if run out of the stock
                if model.stock < 1:
                    return jsonify({'returnValue': 3, 'msg': 'This item is out of stock now!'})

                if new_count <= model.stock:
                    cart_relation.count = new_count
                    db.session.commit()
                    return jsonify({'returnValue': 0})
                else:
                    # the new count exceeds the maximum of the stock!
                    return jsonify({'returnValue': 2, 'msg': 'exceed maximum stock'})

    return jsonify({'returnValue': 1})


@cart.route('/api/cart/remove-cart-relation', methods=['POST'])
@login_required
@customer_only()
def remove_cart_relation():
    """
        (Using Ajax)
        remove a specific cart relation according to the cart_id
        (remove a product from shopping cart)
    """
    if request.method == 'POST':
        # get the if of the cart relation that we want to remove
        cart_id = request.form.get("cart_id")

        if cart_id is None:
            current_app.logger.error("info not gotten from Ajax")
            return jsonify({"returnValue": 1})

        # query the cart relation from database
        cart_relation = Cart.query.get(cart_id)

        # check if exists
        if cart_relation:
            db.session.delete(cart_relation)
            db.session.commit()
            flash("Remove commodity successful!")
            return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})
