from flask import Blueprint

# Create a Blueprint class object called userinfo, set the blueprint name as 'userinfo'
userinfo = Blueprint('userinfo', __name__)

from . import views
