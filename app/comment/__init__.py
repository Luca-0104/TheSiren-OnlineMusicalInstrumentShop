from flask import Blueprint

# Create a Blueprint class object called comment, set the blueprint name as 'comment'
comment = Blueprint('comment', __name__)

from . import views
