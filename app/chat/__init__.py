from flask import Blueprint

# Create a Blueprint class object called chat, set the blueprint name as 'chat'
chat = Blueprint('chat', __name__)

from . import views