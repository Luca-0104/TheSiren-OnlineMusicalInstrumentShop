import os

from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from . import comment
from config import Config
from ..public_tools import generate_safe_pic_name, upload_picture
from ..comment.forms import CommentForm
from ..models import User, Address, Comment
from .. import db


@comment.route('/upload-comment/<int:model_type_id>', methods=['GET', 'POST'])
@login_required
def upload_comment(model_type_id):
    """
    Upload a comment for a bought item
    :param model_type_id: the id of the model type that is being commented
    """
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        rate = form.rate.data

        # create a new comment
        new_comment = Comment(content=content, star_num=rate, model_type_id=model_type_id, auth_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()

        """
           dealing with the uploaded pictures
        """
        # get a list of file objects from the user upload
        picture_list = form.pictures.data
        result = upload_picture(picture_list, new_comment.id, Config.PIC_TYPE_COMMENT)
        status = result[0]
        if status != 0:
            flash("Picture upload failed!")

        return redirect(url_for("order.my_orders"))

    return render_template('', form=form)

