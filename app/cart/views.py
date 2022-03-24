from flask import request, jsonify
from flask_login import current_user, login_required

from app import db
from app.main import main


# ------------------------------ BACK-END Server (using Ajax) ----------------------------------
from app.models import Cart


@main.route('/api/cart/update-cart-count', methods=['POST'])
@login_required
def update_cart_count():
    """
        update the model account of a specific cart relation, which is about
        current user and the given product
    """
    if request.method == 'POST':
        # get the info from Ajax
        model_id = request.form['model_id']
        new_count = int(request.form['new_count'])

        # new_count should larger than 0
        if new_count > 0:
            # find the instance of the given cart relation from db
            cart_relation = Cart.query.filter_by(user_id=current_user.id, model_type_id=model_id).first()

            # check whether the cart relation exists
            if cart_relation:
                cart_relation.count = new_count
                db.session.commit()
                return jsonify({'returnValue': 0})
            else:
                return jsonify({'returnValue': 1})
        else:
            return jsonify({'returnValue': 1})

    return jsonify({'returnValue': 1})


@main.route('/api/cart/remove-cart-relation', methods=['POST'])
@login_required
def remove_cart_relation():
    """
        remove a specific cart relation according to the cart_id
        (remove a product from shopping cart)
    """
    if request.method == 'POST':
        # get the if of the cart relation that we want to remove
        cart_id = request.form['cart_id']

        # query the cart relation from database
        cart_relation = Cart.query.get(cart_id)

        # check if exists
        if cart_relation:
            db.session.delete(cart_relation)
            db.session.commit()
            return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})