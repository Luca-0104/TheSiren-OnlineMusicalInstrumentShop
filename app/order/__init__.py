from flask import Blueprint

# Create a Blueprint class object called order, set the blueprint name as 'order'
order = Blueprint('order', __name__)

from . import views