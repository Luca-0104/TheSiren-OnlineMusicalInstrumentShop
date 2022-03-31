import os

from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from . import comment
from config import Config
from ..public_tools import generate_safe_pic_name
from ..comment.forms import AForm, BForm
from ..models import User, Address
from .. import db


@comment.route('/00', methods=['GET', 'POST'])
def testPip():
    print("test")
    aForm = AForm()
    bForm = BForm()
    if aForm.submita.data and aForm.validate():
        print("a")
        print(aForm.texta.data)
    if bForm.submitb.data and bForm.validate():
        print("b")
        print(bForm.textb.data)
    return render_template('main/testPip.html', aForm=aForm, bForm=bForm)