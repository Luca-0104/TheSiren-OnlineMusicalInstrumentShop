from flask import Blueprint

# Create a Blueprint class object called main, set the blueprint name as 'main'
auth = Blueprint('auth', __name__)

from . import views
