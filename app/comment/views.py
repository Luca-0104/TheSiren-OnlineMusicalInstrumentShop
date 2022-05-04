import os

from flask import render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_login import login_required, current_user

from . import comment
from config import Config
from ..public_tools import generate_safe_pic_name, upload_picture
from ..comment.forms import CommentForm
from ..models import User, Address, Comment, ModelType, OrderModelType, Order
from .. import db


@comment.route('/upload-comment/<int:omt_id>', methods=['GET', 'POST'])
@login_required
def upload_comment(omt_id):
    """
    Upload a comment for a bought item
    :param omt_id: the id of the "order model type" that is being commented
    """
    form = CommentForm()

    # get omt by id
    omt = OrderModelType.query.get(omt_id)
    if omt is None:
        current_app.logger.error("No omt with is order!")
        return redirect(url_for("order.my_orders"))

    if omt.is_commented:
        flash("You cannot comment a same model in a order twice!")
        current_app.logger.error("Double comment!")
        return redirect(url_for("order.my_orders"))

    mt_id = omt.model_type_id

    # get the model by id
    model_type = ModelType.query.get(mt_id)
    if model_type is None:
        flash("The model does not exist!")
        current_app.logger.error("No model with is order!")
        return redirect(url_for("order.my_orders"))

    if form.validate_on_submit():
        content = form.content.data
        rate = form.rate.data

        # create a new comment
        new_comment = Comment(content=content, star_num=rate, model_type_id=mt_id, auth_id=current_user.id)
        db.session.add(new_comment)

        """
            deal with the rate number
        """
        # cast the rate from str to float, so that it can be calculated
        rate = float(rate)
        # calculate the average rate,
        # (current total rate + this rate) / (current rate times + 1)
        model_type.rate = ((model_type.rate * model_type.rate_count) + rate) / (model_type.rate_count + 1)
        model_type.rate_count += 1
        db.session.add(model_type)

        """
            mark this OrderModelType as already commented
        """
        omt.is_commented = True
        db.session.add(omt)

        db.session.commit()

        """
           deal with the uploaded pictures
        """
        # get a list of file objects from the user upload
        picture_list = form.pictures.data
        result = upload_picture(picture_list, new_comment.id, Config.PIC_TYPE_COMMENT)
        status = result[0]
        if status != 0:
            flash("Picture upload failed!")
        else:
            current_app.logger.error(status)

        return redirect(url_for("order.my_orders"))

    return render_template('comment/comment.html', order_model=omt, form=form)

@comment.route('/order-listing', methods=['GET', 'POST'])
@login_required
def order_listing():
    orders = Order.query.all()
    return render_template('staff/page-list-orders.html', orders=orders)