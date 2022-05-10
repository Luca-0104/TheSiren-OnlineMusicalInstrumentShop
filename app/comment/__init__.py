from flask import Blueprint

from ..models import Comment

# Create a Blueprint class object called comment, set the blueprint name as 'comment'
comment = Blueprint('comment', __name__)

from . import views


@comment.app_context_processor
def inject_classes_into_templates():
    return dict(
        Comment=Comment
    )
