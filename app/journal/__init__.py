from flask import Blueprint

# Create a Blueprint class object called journal, set the blueprint name as 'journal'
journal = Blueprint('journal', __name__)

from . import views
