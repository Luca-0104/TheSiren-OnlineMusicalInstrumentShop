from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from . import userinfo
from ..userinfo.forms import EditProfileForm, AddAddressForm, EditAddressForm
from ..models import User, Address
from .. import db


@userinfo.route('/user_profile/<int:uid>')
def user_profile(uid):
    user = User.query.get(uid)
    return render_template('auth/user_profile.html', user=user)


@userinfo.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    (Backend Form)
    :return:
    """
    form = EditProfileForm(current_user)
    # form.gender.choices[('1', 'Man'), ('2', 'Woman'), ('3', 'Unknown')]

    if form.validate_on_submit():
        u = User.query.get(current_user.id)
        u.username = form.username.data
        u.email = form.email.data
        u.about_me = form.about_me.data
        if form.gender.data == 0:
            u.gender = 'Male'
        elif form.gender.data == 1:
            u.gender = 'Female'
        else:
            u.gender = 'Unknown'

        # print('form gender data')
        # print(form.gender.data)
        db.session.add(u)
        db.session.commit()

        flash('Profile update successfully!')

        # back to the stock management page
        return redirect(url_for('auth.user_profile'))

    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me
    if current_user.gender == 'Male':
        form.gender.data = 0
    elif current_user.gender == 'Female':
        form.gender.data = 1
    else:
        form.gender.data = 2

    return render_template('userinfo/profile_test.html', form=form)


@userinfo.route('/add-address', methods=['GET', 'POST'])
@login_required
def add_address():
    """
    (Backend Form)
    :return:
    """
    form = AddAddressForm()
    if form.validate_on_submit():
        addresses = Address.query.filter_by(customer_id=current_user.id).all()
        if addresses is None:
            address = Address(customer_id=current_user.id,
                              recipient_name=form.recipient_name.data,
                              phone=form.phone.data,
                              country=form.country.data,
                              province_or_state=form.province_or_state.data,
                              city=form.city.data,
                              district=form.district.data,
                              is_default=1)
        else:
            address = Address(customer_id=current_user.id,
                              recipient_name=form.recipient_name.data,
                              phone=form.phone.data,
                              country=form.country.data,
                              province_or_state=form.province_or_state.data,
                              city=form.city.data,
                              district=form.district.data)
        db.session.add(address)
        db.session.commit()
        flash('Address added successfully!')

        return redirect(url_for('auth.user_profile'))

    return render_template('userinfo/add_address_test.html', form=form)


@userinfo.route('/edit-address/<address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    """
    (Backend Form)
    :return:
    """
    form = EditAddressForm()
    address = Address.query.filter_by(id=address_id).first()
    if form.validate_on_submit():
        address.recipient_name = form.recipient_name.data
        address.phone = form.phone.data
        address.country = form.country.data
        address.province_or_state = form.province_or_state.data
        address.city = form.city.data
        address.district = form.district.data

        db.session.add(address)
        db.session.commit()
        flash('Address updated successfully!')

    form.recipient_name.data = address.recipient_name
    form.phone.data = address.phone
    form.country.data = address.country
    form.province_or_state.data = address.province_or_state
    form.city.data = address.city
    form.district.data = address.district

    return render_template('', form=form)


@userinfo.route('/api/remove-address', methods=['POST'])
@login_required
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

        # remove this address from db
        db.session.remove(address)
        db.session.commit()

        return jsonify({'returnValue': 0})

    return jsonify({'returnValue': 1})


@userinfo.route('/api/change-default-address', methods=['POST'])
@login_required
def change_default_address():
    pass



def address_prepare_for_json(address_obj):
    address = {'id': address_obj.id, 'recipient_name': address_obj.recipient_name, 'phone': address_obj.phone,
               'country': address_obj.country, 'province_or_state': address_obj.province_or_state, 'city': address_obj.city,
               'district': address_obj.district, 'is_default': address_obj.district}
    return address






