import os

# The directory of this project
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'no one will guess'  # a secret key for the wtf forms
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'zh']

    """ picture uploading """
    # The allowed suffixes type of the picture that is uploaded
    ALLOWED_PIC_SUFFIXES = ['jpg', 'png', 'gif', 'bmp', 'webp', 'pcx', 'tif', 'jpeg', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'al', 'hdri', 'raw', 'wmf', 'flic', 'emf', 'ico', 'avif', 'apng']
    # pic type constants
    PIC_TYPE_MODEL = 'ModelTypePic'
    PIC_TYPE_MODEL_INTRO = 'ModelTypeIntroPic'
    PIC_TYPE_COMMENT = 'CommentPic'

    """ Following define the directories used in this project """
    app_dir = os.path.join(basedir, 'app')
    static_dir = os.path.join(app_dir, 'static')
    upload_dir = os.path.join(static_dir, 'upload')
    model_type_dir = os.path.join(upload_dir, 'model_type')       # The directory for storing the photos of model types in this website
    video_dir = os.path.join(model_type_dir, 'videos')          # videos of model types
    audios_dir = os.path.join(model_type_dir, 'audios')         # audios of model types
    threeD_dir = os.path.join(model_type_dir, '3d-model-files')     # 3d model files of model types
    model_type_intro_dir = os.path.join(upload_dir, 'model_type_intro')       # The directory for storing the photos of the introduction of model types in this website
    comment_dir = os.path.join(upload_dir, 'comment')       # The directory for storing the photos of the comments of products in this website
    avatar_dir = os.path.join(upload_dir, 'avatar')         # The directory for storing the avatars of users

    """ Chat config """
    SERVICE_EXPIRE_LENGTH = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # use SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    # use MySQL8 (Aly RDS cloud database)
    # DB_USERNAME = os.environ.get('DB_USERNAME') or ''
    # DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    # DB_HOSTNAME = os.environ.get('DB_HOSTNAME') or ''
    # DB_DBNAME = os.environ.get('DB_DBNAME') or ''
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://{}:{}@{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_DBNAME)
    # print('----------------------------------------------------------------------------')
    # print(SQLALCHEMY_DATABASE_URI)

    # Alipay config
    RETURN_URL = "http://127.0.0.1:5000/"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'

    # Alipay config
    RETURN_URL = ""


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    # Alipay config
    RETURN_URL = ""


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
