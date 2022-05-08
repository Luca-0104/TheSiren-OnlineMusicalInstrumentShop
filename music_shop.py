import os

from flask import session

from app import create_app, db, socketio

# create an object of our app
from app.models import Tools, Permission, User, Role, Brand, Category, ModelType, ModelTypeIntroPic, ModelTypePic, \
    Product, CommentPic, Comment, Cart, OrderModelType, Order, TheSiren, Journal

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """
    When using the flask shell command, there is no needs to import db, User, Role...anymore.
    """
    return dict(db=db,
                Tools=Tools,
                Permission=Permission,
                User=User,
                Role=Role,
                Brand=Brand,
                Category=Category,
                ModelType=ModelType,
                ModelTypeIntroPic=ModelTypeIntroPic,
                ModelTypePic=ModelTypePic,
                Product=Product,
                CommentPic=CommentPic,
                Comment=Comment,
                Cart=Cart,
                OrderModelType=OrderModelType,
                Order=Order,
                Journal=Journal)
