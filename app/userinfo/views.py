import os

from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from config import Config
from . import userinfo
from ..public_tools import generate_safe_pic_name
from ..userinfo.forms import EditProfileForm, AddAddressForm, EditAddressForm, UpdateAvatarForm
from ..models import User, Address
from .. import db


@userinfo.route('/user_profile/<int:uid>')
def user_profile(uid):
    user = User.query.get(uid)
    edit_profile_form = EditProfileForm(current_user)
    update_avatar_form = UpdateAvatarForm()
    add_address_form = AddAddressForm()
    edit_address_form = EditAddressForm()

    # user submit the edit profile form
    if edit_profile_form.edit_profile_submit.data and edit_profile_form.validate():

        user.username = edit_profile_form.username.data
        user.email = edit_profile_form.email.data
        user.about_me = edit_profile_form.about_me.data
        if edit_profile_form.gender.data == 0:
            user.gender = 'Male'
        elif edit_profile_form.gender.data == 1:
            user.gender = 'Female'
        else:
            user.gender = 'Unknown'

        # print('form gender data')
        # print(form.gender.data)
        db.session.add(user)
        db.session.commit()

        flash('Profile update successfully!')

        # back to the stock management page
        return redirect(url_for('userinfo.user_profile', uid=current_user.id))

    # initialize the edit profile form data
    edit_profile_form.username.data = current_user.username
    edit_profile_form.email.data = current_user.email
    edit_profile_form.about_me.data = current_user.about_me
    if current_user.gender == 'Male':
        edit_profile_form.gender.data = 0
    elif current_user.gender == 'Female':
        edit_profile_form.gender.data = 1
    else:
        edit_profile_form.gender.data = 2

    # user submit the update avatar form
    if update_avatar_form.update_avatar_submit.data and update_avatar_form.validate():
        path = 'upload/avatar'
        avatar_name = update_avatar_form.avatar.data.filename
        picname = generate_safe_pic_name(avatar_name)
        file_path = os.path.join(Config.avatar_dir, picname).replace('\\', '/')
        update_avatar_form.avatar.data.save(file_path)
        user = User.query.get(current_user.id)
        user.avatar = os.path.join(path, picname).replace('\\', '/')
        db.session.add(user)
        db.session.commit()
        flash("Avatar update successfully!")
        return redirect(url_for("userinfo.user_profile", uid=current_user.id))


    # user submit the add address form
    if add_address_form.add_address_submit.data and add_address_form.validate():
        addresses = Address.query.filter_by(customer_id=current_user.id).all()
        # user has no address yet
        if addresses is None:
            address = Address(customer_id=current_user.id,
                              recipient_name=add_address_form.recipient_name.data,
                              phone=add_address_form.phone.data,
                              country=add_address_form.country.data,
                              province_or_state=add_address_form.province_or_state.data,
                              city=add_address_form.city.data,
                              district=add_address_form.district.data,
                              is_default=True)
        # user has multiple address
        else:
            address = Address(customer_id=current_user.id,
                              recipient_name=add_address_form.recipient_name.data,
                              phone=add_address_form.phone.data,
                              country=add_address_form.country.data,
                              province_or_state=add_address_form.province_or_state.data,
                              city=add_address_form.city.data,
                              district=add_address_form.district.data)
        db.session.add(address)
        db.session.commit()
        flash('Address added successfully!')

        return redirect(url_for('userinfo.user_profile', uid=current_user.id))


    # user submit the edit address form
    if edit_address_form.edit_address_submit.data and edit_address_form.validate():
        address_id = request.form.get("address_id")
        address = Address.query.filter_by(id=address_id).first()
        address.recipient_name = edit_address_form.recipient_name.data
        address.phone = edit_address_form.phone.data
        address.country = edit_address_form.country.data
        address.province_or_state = edit_address_form.province_or_state.data
        address.city = edit_address_form.city.data
        address.district = edit_address_form.district.data

        db.session.add(address)
        db.session.commit()
        flash('Address updated successfully!')

        return redirect(url_for("userinfo.user_profile", uid=current_user.id))


    return render_template('userinfo/user_profile.html', user=user, update_avatar_form=update_avatar_form, add_address_form=add_address_form)


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


@userinfo.route('/api/edit-address', methods=['POST'])
@login_required
def edit_address():

    if request.method == 'POST':
        address_id = request.form.get('address_id')
        address = Address.query.get(address_id)

        # check if the address exists
        if address is None:
            return jsonify({'returnValue': 1})

        # check is this address belong to current user
        if address.customer_id != current_user.id:
            return jsonify({'returnValue': 1})

        address_json = address_prepare_for_json(address)
        return jsonify({'returnValue': 0,
                        'address': address_json})

    return jsonify({'returnValue': 1})



@userinfo.route('/api/remove-address', methods=['POST'])
@login_required
def remove_address():
    """
    (Using Ajax)
    """
    if request.method == 'POST':
        # get the address id from ajax
        address_id = request.form.get('address_id')
        print(address_id)

        # find address from db
        address = Address.query.get(address_id)
        if address.is_default is True:
            print('default is true')
            new_default_address = Address.query.filter_by(customer_id=current_user.id).first()
            print(new_default_address)
            if new_default_address is not None:
                new_default_address.is_default = True
                db.session.add(new_default_address)
                print('over')

        # check if the address exists
        if address is None:
            return jsonify({'returnValue': 1})

        # check is this address belong to current user
        if address.customer_id != current_user.id:
            return jsonify({'returnValue': 1})

        print(address)
        # remove this address from db
        db.session.delete(address)
        db.session.commit()

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


@userinfo.route('/api/change-default-address', methods=['POST'])
@login_required
def change_default_address():

    if request.method == 'POST':
        # get the address id from ajax
        address_id = request.form.get('address_id')
        print(address_id)

        # find address from db
        new_default_address = Address.query.get(address_id)
        old_default_address = Address.query.filter_by(customer_id=current_user.id, is_default=True).first()

        # check if the address exists
        if new_default_address is None:
            return jsonify({'returnValue': 1})

        # check is this address belong to current user
        if new_default_address.customer_id != current_user.id:
            return jsonify({'returnValue': 1})

        new_default_address.is_default = True
        old_default_address.is_default = False

        # update default address
        db.session.add(new_default_address)
        db.session.add(old_default_address)
        db.session.commit()

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})



def address_prepare_for_json(address_obj):
    """
    This function is used to support ajax process
    :param address_obj:
    :return: address data in json
    """
    address = {'id': address_obj.id, 'recipient_name': address_obj.recipient_name, 'phone': address_obj.phone,
               'country': address_obj.country, 'province_or_state': address_obj.province_or_state, 'city': address_obj.city,
               'district': address_obj.district, 'is_default': address_obj.district}
    return address






