from flask import Blueprint

# Create a Blueprint class object called main, set the blueprint name as 'cart'
cart = Blueprint('cart', __name__)

from . import views
