from flask import Blueprint

# Create a Blueprint class object called errors, set the blueprint name as 'errors'
errors = Blueprint('errors', __name__)

from . import views
