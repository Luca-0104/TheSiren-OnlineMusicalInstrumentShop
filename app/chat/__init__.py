from flask import Blueprint

# Create a Blueprint class object called chat, set the blueprint name as 'chat'
from ..models import Message

chat = Blueprint('chat', __name__)

from . import views


@chat.app_context_processor
def inject_classes_into_templates():
    return dict(
        Message=Message
    )