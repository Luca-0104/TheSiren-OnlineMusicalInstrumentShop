from flask import Flask, session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import logging
from logging.handlers import RotatingFileHandler
from flask_socketio import SocketIO
from flask_moment import Moment
from flask_babel import Babel

# load the extensions we need
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
socketio = SocketIO()
moment = Moment()
babel = Babel()


def create_app(config_name):
    app = Flask(__name__)
    # load the config from the Config class according to the config name
    app.config.from_object(config[config_name])
    # choose the specific config class by using the config_name as the key in the dict
    config[config_name].init_app(app)

    # initialize the extensions we need
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # register the logger
    # register_logger(app)

    # register blueprint - main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # register blueprint - auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # register blueprint - product
    from .product import product as product_blueprint
    app.register_blueprint(product_blueprint)

    # register blueprint - chat
    from .chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)

    # register blueprint - order
    from .order import order as order_blueprint
    app.register_blueprint(order_blueprint)

    # register blueprint - payment
    from .payment import payment as payment_blueprint
    app.register_blueprint(payment_blueprint)

    return app


def register_logger(app):
    """
    Define the configure of the logger file
    """
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y%b%d-%H:%M:%S")

    file_handler = RotatingFileHandler('logs/prweb.log', maxBytes=10 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # if not app.debug:
    app.logger.addHandler(file_handler)


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(['en', 'zh'])
    return request.accept_languages.best_match([session['language']])
