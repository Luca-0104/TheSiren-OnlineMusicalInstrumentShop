import os
import random
from datetime import datetime

from flask import current_app
from werkzeug.utils import secure_filename

from app import db
from app.models import User, ModelTypePic, ModelType, Comment, ModelTypeIntroPic, CommentPic, TheSiren
from config import Config


def generate_safe_pic_name(pic_name):
    """
    To avoid the replicated picture name in our picture repository,
    we append the current date time and a random int into the file name

    :param pic_name: The original picture name
    :return:    A safe picture name contains the datetime of now and a long random integer
    """
    # due to ':' and space cannot be contained in the picture name, we replace them with '.' and '_'
    datetime_suffix = str(datetime.utcnow()).replace(" ", "_").replace(":", ".")

    # get a random int
    random_num_suffix = random.randint(0, 9999999999)

    # call the secure_filename function in the werkzeug, this can make the filename safe (for example, replace the blank space with '_', and so on)
    pic_name = secure_filename(pic_name)

    # append the datetime and random int into the pic_name, at the end but before the suffix (.png, .jpg ...)
    pic_name = pic_name[:pic_name.rfind(".")] + '_' + str(
        random_num_suffix) + '_' + datetime_suffix + pic_name[pic_name.rfind("."):]

    return pic_name


def upload_picture(picture_list, host_id, pic_type):
    """
    This method will do mainly 2 things:
    1. save a list of pictures in to the proper directory
    2. turn those pictures into objects in our database and
        establish the relationship between them and their host objects
        (e.g. ModelTypePic->ModelType, CommentPic->Comment...)
    :param picture_list: A list of picture files
    :param host_id: The id of the host object of these pictures
    :param pic_type: The only choices: 'ModelTypePic', 'ModelTypeIntroPic', 'CommentPic'
    :return: (status_code, attach)
            status_code: 0->success, 1->failed and no pic uploaded, 2->failed and some of the pics are not uploaded
            attach: success string (0), Error string (1), failed_list (2)
    """

    """
        Choose different dir to save picture 
        and different path to create address 
        according to the pic_type    
        AND
        Check if the host object with this host_id exists. 
    """
    if pic_type == 'ModelTypePic':
        save_dir = Config.model_type_dir
        path = 'upload/model_type'
        host = ModelType.query.get(host_id)

    elif pic_type == 'ModelTypeIntroPic':
        save_dir = Config.model_type_intro_dir
        path = 'upload/model_type_intro'
        host = ModelType.query.get(host_id)

    elif pic_type == 'CommentPic':
        save_dir = Config.comment_dir
        path = 'upload/comment'
        host = Comment.query.get(host_id)

    else:
        return 1, 'Error! No such pic_type!'

    if host is None:
        return 1, 'Error! No host object with this host_id!'

    """ 
        Loop through the list getting and storing each picture 
    """
    # a list to store the name of pictures that are failed to be uploaded
    failed_list = []
    for pic in picture_list:

        # get the name of the picture
        pic_name = pic.filename
        pic_name_origin = pic_name
        # get the suffix of the picture
        suffix = pic_name.rsplit('.')[-1]

        if suffix in Config.ALLOWED_PIC_SUFFIXES:
            # make sure the name of picture is safe
            pic_name = generate_safe_pic_name(pic_name)

            """
                save the picture in the local directory
            """
            # get the path to store the picture (dir + pic_name)
            file_path = os.path.join(save_dir, pic_name).replace('\\', '/')
            # save the picture
            pic.save(file_path)

            """
                save the picture in the database
            """
            pic_address = os.path.join(path, pic_name).replace('\\', '/')
            # create different object according to the pic_type
            if pic_type == 'ModelTypePic':
                pic_object = ModelTypePic(address=pic_address, model_id=host_id)
            elif pic_type == 'ModelTypeIntroPic':
                pic_object = ModelTypeIntroPic(address=pic_address, model_id=host_id)
            elif pic_type == 'CommentPic':
                pic_object = CommentPic(address=pic_address, comment_id=host_id)
            else:
                return 1, 'Error! No such pic_type!'

            db.session.add(pic_object)

        else:
            # add the pic name into the failed list
            failed_list.append(pic_name_origin)

    # commit db session
    db.session.commit()

    if len(failed_list) == 0:
        return 0, 'All pictures uploaded successfully!'
    else:
        return 2, failed_list


def get_unique_shop_instance():
    """
    This functions is used to get the unique instance of this musical shop
    :return: A instance of TheSiren
    """
    unique_instance = TheSiren.query.get(1)
    return unique_instance


def get_epidemic_mode_status():
    """
    Get the boolean about whether the epidemic mode is turned on
    :return: Boolean
    """
    # get the status of epidemic mode
    siren = get_unique_shop_instance()
    if siren:
        epidemic_mode_on = siren.epidemic_mode_on
    else:
        current_app.logger.error("Siren instance not found!")
        epidemic_mode_on = False

    return epidemic_mode_on


def get_user_by_name(username):
    """
    This function is used to get a user object by their username
    :param username: the username of the user
    :return: a user object
    """
    return User.query.filter_by(username=username).first()


def get_user_by_id(uid):
    """
    This function is used to get a user object by their id
    :param uid: the id of the user
    :return: a user object
    """
    return User.query.get(uid)
