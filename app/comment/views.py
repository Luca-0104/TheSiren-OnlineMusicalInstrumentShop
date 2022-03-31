import os

from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from config import Config
from . import userinfo
from ..public_tools import generate_safe_pic_name
from ..comment.forms import AForm, BForm
from ..models import User, Address
from .. import db


@userinfo.route('/00')
def testPip():
    aForm = AForm()
    BForm = BForm()
    return render_template('main/testPip.html', aForm=aForm, bForm=bForm)