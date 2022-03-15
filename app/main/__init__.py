from flask import Blueprint

# Create a Blueprint class object called main, set the blueprint name as 'main'
main = Blueprint('main', __name__)

from . import views
