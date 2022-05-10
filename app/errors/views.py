import os

from flask import render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_login import login_required, current_user

from . import comment
from config import Config
from ..decorators import customer_only
from ..public_tools import generate_safe_pic_name, upload_picture
from ..comment.forms import CommentForm
from ..models import User, Address, Comment, ModelType, OrderModelType, Order
from .. import db

