import os

from flask import render_template, request, jsonify, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from flask_babel import _

from config import Config
from . import userinfo
from ..decorators import customer_only
from ..public_tools import generate_safe_pic_name
from ..userinfo.forms import EditProfileForm, AddAddressForm, EditAddressForm, UpdateAvatarForm
from ..models import User, Address, Recipient, Brand, Category
from .. import db


@userinfo.route('/user_profile/<int:uid>', methods=['GET', 'POST'])
@login_required
@customer_only()
def user_profile(uid):
    # customers can only access their own profiles
    if current_user.id != uid:
        flash(_("Permission Denied! You cannot access the profile of other users!"))
        abort(403)

    user = User.query.get(uid)
    edit_profile_form = EditProfileForm(current_user)
    update_avatar_form = UpdateAvatarForm()
    add_address_form = AddAddressForm()
    edit_address_form = EditAddressForm()

    # user submit the edit profile form
    if edit_profile_form.edit_profile_submit.data and edit_profile_form.validate():
        print('get into profile')
        user.username = edit_profile_form.edit_profile_username.data
        user.email = edit_profile_form.edit_profile_email.data
        user.about_me = edit_profile_form.edit_profile_about_me.data
        print(edit_profile_form.edit_profile_gender.data)
        if edit_profile_form.edit_profile_gender.data == 0:
            user.gender = 'Male'
        elif edit_profile_form.edit_profile_gender.data == 1:
            user.gender = 'Female'
        else:
            user.gender = 'Unknown'

        # print('form gender data')
        # print(form.gender.data)
        db.session.add(user)
        db.session.commit()

        flash(_('Profile update successfully!'))

        # back to the stock management page
        return redirect(url_for('userinfo.user_profile', uid=current_user.id))

    # initialize the edit profile form data
    edit_profile_form.edit_profile_username.data = current_user.username
    edit_profile_form.edit_profile_email.data = current_user.email
    edit_profile_form.edit_profile_about_me.data = current_user.about_me
    if current_user.gender == 'Male':
        edit_profile_form.edit_profile_gender.data = 0
    elif current_user.gender == 'Female':
        edit_profile_form.edit_profile_gender.data = 1
    else:
        edit_profile_form.edit_profile_gender.data = 2

    # user submit the update avatar form
    if update_avatar_form.update_avatar_submit.data and update_avatar_form.validate():
        path = 'upload/avatar'
        avatar_name = update_avatar_form.update_avatar.data.filename
        picname = generate_safe_pic_name(avatar_name)
        file_path = os.path.join(Config.avatar_dir, picname).replace('\\', '/')
        update_avatar_form.update_avatar.data.save(file_path)
        user = User.query.get(current_user.id)
        user.avatar = os.path.join(path, picname).replace('\\', '/')
        db.session.add(user)
        db.session.commit()
        flash(_("Avatar update successfully!"))
        return redirect(url_for("userinfo.user_profile", uid=current_user.id))

    # user submit the add address form
    if add_address_form.add_address_submit.data and add_address_form.validate():
        addresses = Address.query.filter_by(customer_id=current_user.id).first()
        # create a recipient obj
        new_recipient = Recipient(recipient_name=add_address_form.add_recipient_name.data,
                                  phone=add_address_form.add_phone.data)
        db.session.add(new_recipient)

        # user has no address yet
        if addresses is None:
            address = Address(customer_id=current_user.id,
                              country=add_address_form.add_country.data,
                              province_or_state=add_address_form.add_province_or_state.data,
                              city=add_address_form.add_city.data,
                              district=add_address_form.add_district.data,
                              details=add_address_form.add_details.data,
                              is_default=True)
        # user has multiple address
        else:
            address = Address(customer_id=current_user.id,
                              country=add_address_form.add_country.data,
                              province_or_state=add_address_form.add_province_or_state.data,
                              city=add_address_form.add_city.data,
                              district=add_address_form.add_district.data,
                              details=add_address_form.add_details.data
                              )

        # set recipient for this new address
        address.recipient = new_recipient

        db.session.add(address)
        db.session.commit()
        flash(_('Address added successfully!'))

        return redirect(url_for('userinfo.user_profile', uid=current_user.id))

    # user submit the edit address form
    if edit_address_form.edit_address_submit.data and edit_address_form.validate():
        # address_id = request.form.get("address_id")
        address_id = edit_address_form.edit_address_id.data
        print(edit_address_form.edit_recipient_name.data)
        address = Address.query.get(address_id)
        address.recipient.recipient_name = edit_address_form.edit_recipient_name.data
        address.recipient.phone = edit_address_form.edit_phone.data
        address.country = edit_address_form.edit_country.data
        address.province_or_state = edit_address_form.edit_province_or_state.data
        address.city = edit_address_form.edit_city.data
        address.district = edit_address_form.edit_district.data
        address.details = edit_address_form.edit_details.data

        db.session.add(address)
        db.session.add(address.recipient)
        db.session.commit()
        flash(_('Address updated successfully!'))

        return redirect(url_for("userinfo.user_profile", uid=current_user.id))

    all_brands = Brand.query.all()
    all_categories = Category.query.all()

    return render_template('userinfo/user_profile.html', user=user, all_brands=all_brands, all_categories=all_categories,
                           update_avatar_form=update_avatar_form,
                           add_address_form=add_address_form, edit_address_form=edit_address_form,
                           edit_profile_form=edit_profile_form)


# @userinfo.route('/01')
# def temp_address_listing():
#     user = current_user
#     return render_template('userinfo/temp_address_listing.html', user=user)


# @userinfo.route('/edit-profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     """
#     (Backend Form)
#     :return:
#     """
#     form = EditProfileForm(current_user)
#     # form.gender.choices[('1', 'Man'), ('2', 'Woman'), ('3', 'Unknown')]
#
#     if form.validate_on_submit():
#         u = User.query.get(current_user.id)
#         u.username = form.username.data
#         u.email = form.email.data
#         u.about_me = form.about_me.data
#         if form.gender.data == 0:
#             u.gender = 'Male'
#         elif form.gender.data == 1:
#             u.gender = 'Female'
#         else:
#             u.gender = 'Unknown'
#
#         # print('form gender data')
#         # print(form.gender.data)
#         db.session.add(u)
#         db.session.commit()
#
#         flash('Profile update successfully!')
#
#         # back to the stock management page
#         return redirect(url_for('userinfo.user_profile', uid=current_user.id))
#
#     form.username.data = current_user.username
#     form.email.data = current_user.email
#     form.about_me.data = current_user.about_me
#     if current_user.gender == 'Male':
#         form.gender.data = 0
#     elif current_user.gender == 'Female':
#         form.gender.data = 1
#     else:
#         form.gender.data = 2
#
#     return render_template('userinfo/profile_test.html', form=form)


# @userinfo.route('/update-avatar', methods=['GET', 'POST'])
# @login_required
# def update_avatar():
#
#     form = UpdateAvatarForm()
#     path = 'upload/avatar'
#     if form.validate_on_submit():
#         print('get in')
#         avatar_name = form.avatar.data.filename
#         picname = generate_safe_pic_name(avatar_name)
#         file_path = os.path.join(Config.avatar_dir, picname).replace('\\', '/')
#         form.avatar.data.save(file_path)
#         user = User.query.get(current_user.id)
#         user.avatar = os.path.join(path, picname).replace('\\', '/')
#         db.session.add(user)
#         db.session.commit()
#         flash("Avatar update successfully!")
#         return redirect(url_for("userinfo.user_profile", uid=current_user.id))
#
#     return render_template('userinfo/avatar_update_test.html', form=form)


# @userinfo.route('/add-address', methods=['GET', 'POST'])
# @login_required
# def add_address():
#     """
#     (Backend Form)
#     :return:
#     """
#     form = AddAddressForm()
#     if form.validate_on_submit():
#         addresses = Address.query.filter_by(customer_id=current_user.id).all()
#         # user has no address yet
#         if addresses is None:
#             address = Address(customer_id=current_user.id,
#                               recipient_name=form.recipient_name.data,
#                               phone=form.phone.data,
#                               country=form.country.data,
#                               province_or_state=form.province_or_state.data,
#                               city=form.city.data,
#                               district=form.district.data,
#                               is_default=True)
#         # user has multiple address
#         else:
#             address = Address(customer_id=current_user.id,
#                               recipient_name=form.recipient_name.data,
#                               phone=form.phone.data,
#                               country=form.country.data,
#                               province_or_state=form.province_or_state.data,
#                               city=form.city.data,
#                               district=form.district.data)
#         db.session.add(address)
#         db.session.commit()
#         flash('Address added successfully!')
#
#         return redirect(url_for('userinfo.user_profile', uid=current_user.id))
#
#     return render_template('userinfo/add_address_test.html', form=form)


# @userinfo.route('/edit-address/<address_id>', methods=['GET', 'POST'])
# @login_required
# def edit_address(address_id):
#     """
#     (Backend Form)
#     :return:
#     """
#     form = EditAddressForm()
#     address = Address.query.filter_by(id=address_id).first()
#     if form.validate_on_submit():
#         address.recipient_name = form.recipient_name.data
#         address.phone = form.phone.data
#         address.country = form.country.data
#         address.province_or_state = form.province_or_state.data
#         address.city = form.city.data
#         address.district = form.district.data
#
#         db.session.add(address)
#         db.session.commit()
#         flash('Address updated successfully!')
#
#         return redirect(url_for("userinfo.user_profile", uid=current_user.id))
#
#     form.recipient_name.data = address.recipient_name
#     form.phone.data = address.phone
#     form.country.data = address.country
#     form.province_or_state.data = address.province_or_state
#     form.city.data = address.city
#     form.district.data = address.district
#
#     return render_template('userinfo/edit_address_test.html', form=form)


# @userinfo.route('/api/edit-address', methods=['POST'])
# @login_required
# def edit_address():
#
#     if request.method == 'POST':
#         address_id = request.form.get('address_id')
#         address = Address.query.get(address_id)
#
#         # check if the address exists
#         if address is None:
#             return jsonify({'returnValue': 1})
#
#         # check is this address belong to current user
#         if address.customer_id != current_user.id:
#             return jsonify({'returnValue': 1})
#
#         address_json = address_prepare_for_json(address)
#         return jsonify({'returnValue': 0,
#                         'address': address_json})
#
#     return jsonify({'returnValue': 1})


@userinfo.route('/api/remove-address', methods=['POST'])
@login_required
@customer_only(is_ajax=True)
def remove_address():
    """
    (Using Ajax)
    """
    if request.method == 'POST':
        # get the address id from ajax
        address_id = request.form.get('address_id')

        # find address from db
        address = Address.query.get(address_id)

        # check if the address exists
        if address is None:
            return jsonify({'returnValue': 1})

        # check is this address belong to current user
        if address.customer_id != current_user.id:
            return jsonify({'returnValue': 1})

        # if the one we gonna delete is a default address
        if address.is_default is True:
            # whether this is the only address of this user
            if current_user.addresses.count() == 1 and current_user.addresses.first() == address:
                # if this is the only one, we can just delete it
                db.session.delete(address)
                db.session.commit()
                flash(_('Address has been deleted!'))

                # '3' means no new_id
                return jsonify({'returnValue': 3})

            else:
                # if there are still some other addresses, we set the first one as new default address after removal
                # first, remove this one
                db.session.delete(address)
                db.session.commit()
                # then, change the first one to default
                new_default_address = current_user.addresses.first()
                new_default_address.is_default = True
                db.session.add(new_default_address)
                db.session.commit()

                flash(_('Address has been deleted!'))
                return jsonify({'returnValue': 2, 'new_id': new_default_address.id})

        else:
            # if the one we gonna delete is not a default address
            # we can just delete it
            db.session.delete(address)
            db.session.commit()

        flash(_('Address has been deleted!'))

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


@userinfo.route('/api/change-default-address', methods=['POST'])
@login_required
@customer_only(is_ajax=True)
def change_default_address():
    if request.method == 'POST':
        # get the address id from ajax
        address_id = request.form.get('address_id')

        # find address from db
        new_default_address = Address.query.get(address_id)
        # old_default_address = Address.query.filter_by(customer_id=current_user.id, is_default=True).first()
        old_default_address = current_user.addresses.filter_by(is_default=True).first()

        # check if the address exists
        if new_default_address is None:
            return jsonify({'returnValue': 1})

        # check is this address belong to current user
        if new_default_address.customer_id != current_user.id:
            return jsonify({'returnValue': 1})

        for address in current_user.addresses:
            address.is_default = False
            db.session.add(address)

        # set this one as detault
        new_default_address.is_default = True

        # update default address
        db.session.add(new_default_address)
        db.session.add(old_default_address)
        db.session.commit()

        flash(_('Default address changed successfully!'))

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


def address_prepare_for_json(address_obj):
    """
    This function is used to support ajax process
    :param address_obj:
    :return: address data in json
    """
    address = {'id': address_obj.id, 'recipient_name': address_obj.recipient_name, 'phone': address_obj.phone,
               'country': address_obj.country, 'province_or_state': address_obj.province_or_state,
               'city': address_obj.city,
               'district': address_obj.district, 'is_default': address_obj.district}
    return address


# ---------------------------------------- Brand section ----------------------------------------

@userinfo.route('/api/userinfo/brand-section/follow-brand', methods=['POST'])
@login_required
@customer_only(is_ajax=True)
def follow_brand():
    """
        (Using Ajax)
        This is a function for a customer to follow a brand
    """
    if request.method == 'POST':
        # get info from Ajax
        brand_id = request.form.get("brand_id")

        if brand_id is None:
            current_app.logger.error("Info not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # query Brand instance from db
        brand = Brand.query.get(brand_id)

        if brand is None:
            current_app.logger.error("No such brand with this id")
            return jsonify({'returnValue': 1})

        # add this brand to the followed_brands of current user
        current_user.followed_brands.append(brand)

        db.session.add(current_user)
        db.session.commit()

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


@userinfo.route('/api/userinfo/brand-section/unfollow-brand', methods=['POST'])
@login_required
@customer_only(is_ajax=True)
def unfollow_brand():
    """
        (Using Ajax)
        This is a function for a customer to unfollow a brand
    """
    if request.method == 'POST':
        # get info from Ajax
        brand_id = request.form.get("brand_id")

        if brand_id is None:
            current_app.logger.error("Info not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # query Brand instance from db
        brand = Brand.query.get(brand_id)

        if brand is None:
            current_app.logger.error("No such brand with this id")
            return jsonify({'returnValue': 1})

        # validate whether the user followed this brand (If do not do this, there might be an error)
        if brand not in current_user.followed_brands:
            current_app.logger.error("A user wants to unfollow a brand even he/she has not followed it!")
            return jsonify({'returnValue': 1})

        # add this brand to the followed_brands of current user
        current_user.followed_brands.remove(brand)

        db.session.add(current_user)
        db.session.commit()

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


# ---------------------------------------- Category section ----------------------------------------


@userinfo.route('/api/userinfo/category-section/follow-category', methods=['POST'])
@login_required
@customer_only(is_ajax=True)
def follow_category():
    """
        (Using Ajax)
        This is a function for a customer to follow a category
    """
    if request.method == 'POST':
        # get info from Ajax
        category_id = request.form.get("category_id")

        if category_id is None:
            current_app.logger.error("Info not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # query Category instance from db
        category = Category.query.get(category_id)

        if category is None:
            current_app.logger.error("No such category with this id")
            return jsonify({'returnValue': 1})

        # add this category to the followed_categories of current user
        current_user.followed_categories.append(category)

        db.session.add(current_user)
        db.session.commit()

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


@userinfo.route('/api/userinfo/brand-section/unfollow-category', methods=['POST'])
@login_required
@customer_only(is_ajax=True)
def unfollow_category():
    """
        (Using Ajax)
        This is a function for a customer to unfollow a category
    """
    if request.method == 'POST':
        # get info from Ajax
        category_id = request.form.get("category_id")

        if category_id is None:
            current_app.logger.error("Info not gotten from Ajax")
            return jsonify({'returnValue': 1})

        # query Category instance from db
        category = Category.query.get(category_id)

        if category is None:
            current_app.logger.error("No such category with this id")
            return jsonify({'returnValue': 1})

        # validate whether the user followed this category (If do not do this, there might be an error)
        if category not in current_user.followed_categories:
            current_app.logger.error("A user wants to unfollow a category even he/she has not followed it!")
            return jsonify({'returnValue': 1})

        # add this brand to the followed_categories of current user
        current_user.followed_categories.remove(category)

        db.session.add(current_user)
        db.session.commit()

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})