from flask import Blueprint

# Create a Blueprint class object called product, set the blueprint name as 'product'
product = Blueprint('product', __name__)

from . import views