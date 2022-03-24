from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.table_info import category_list, brand_list, user_list, product_list

from . import login_manager

import random


class Tools:
    """
    All the tool methods for creating the tables
    """

    @staticmethod
    def update_db():
        db.drop_all()
        db.create_all()
        Tools.fill_all_tables()

    @staticmethod
    def fill_all_tables():
        """
        Fill all the tables in an specific order.
        This should be used in the console only a single time.
        """
        Role.insert_roles()  # roles of users
        User.insert_users()  # the constant user accounts for test
        # # users(100)  # 100 fake users
        Category.insert_categories()  # the product categories
        Brand.insert_brands()  # the product brands
        Product.insert_products()  # the constant products for show
        # ProductPic.insert_pictures()  # the pictures of the constant products
        # # products(100)  # 100 fake products
        ModelType.insert_model_types()  # the constant model types for testing


class Refund(db.Model):
    """
        The refund records, each line in this table related to a line in 'OrderModelType' (1 to 1 relation (we implement it as 1 to n))

        Attention! Each time a "refund" is applied, a piece of "Chat" will be generated automatically then be sent to the staff.
    """
    __tablename__ = 'refunds'
    id = db.Column(db.Integer, primary_key=True)
    order_model_type_id = db.Column(db.Integer, db.ForeignKey('order_model_types.id'))
    count = db.Column(db.Integer,
                      default=1)  # how many items is applied to be refund in this order_model_type. This should <= the count in this order_model_type
    reason = db.Column(db.Text())  # customer should give the reason why they ask for a refund
    is_done = db.Column(db.Boolean, default=False)


# class Change(db.Model):
#     pass

class ChatRoom(db.Model):
    """
        (Chatting version 2 -> ChatRoom + Message)
    """
    __tablename__ = 'chat_rooms'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # messages in this chat room
    messages = db.relationship('Message', backref='chat_room', lazy='dynamic')

    def __repr__(self):
        return '<ChatRoom cus: %r - staff: %r>' % (self.customer_id, self.staff_id)


class Message(db.Model):
    """
        (Chatting version 2 -> ChatRoom + Message)
        Storing the chatting record of a customer and staff(staff role, not a specific staff)
    """
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    # for specifying whose statement is this (from customer or staff)
    # only 2 possible values, 'customer' and 'staff'
    author_type = db.Column(db.String(12), nullable=False)
    # The type of this piece of information
    # possible values: "normal", "refund", "enquiry"...
    chat_type = db.Column(db.String(12), default='normal')
    # Which chatting room this message belongs to
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'))

    def __repr__(self):
        return '<Chat %r>' % self.content[:10]


'''
Chatting version 1
class Chat(db.Model):
    """
        Storing the chatting record of a customer and staff(staff role, not a specific staff)
    """
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    # for specifying whose statement is this (from customer or staff)
    # only 2 possible values, 'customer' and 'staff'
    author_type = db.Column(db.String(12), nullable=False)
    # The type of this piece of information
    # possible values: "normal", "refund", "enquiry"...
    chat_type = db.Column(db.String(12), default='normal')

    def __repr__(self):
        return '<Chat %r>' % self.content[:10]
'''


class Order(db.Model):
    """
        A purchase can be regarded as an order.

        An order can contain multiple model types of products. (This is implemented by using a third-party table "OrderModelType")
        An order can contain multiple references to "OrderModelType" table

        Every order have their states code: 0:"waiting for payment",
                                            1:"preparing"
                                            2:"on delivery",
                                            3:"waiting for collection",
                                            4:"finished",
                                            5:"canceled"
                                            6:"expired
        "finished" orders can be seen as shopping histories
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    status_code = db.Column(db.Integer, default=0)  # the status code of this order
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # the uid of the customer who owns this order
    # 1 order -> n OrderModelType; 1 OrderModelType -> 1 order
    order_model_types = db.relationship('OrderModelType', backref='order', lazy='dynamic')

    def get_status(self):
        """
        Get the status of this order.
        :return: A string of the status of this order
        """
        if self.status_code == 0:
            return 'waiting for payment'
        elif self.status_code == 1:
            return 'preparing'
        elif self.status_code == 2:
            return 'on delivery'
        elif self.status_code == 3:
            return 'waiting for collection'
        elif self.status_code == 4:
            return 'finished'
        elif self.status_code == 5:
            return 'canceled'
        elif self.status_code == 6:
            return 'expired'


class OrderModelType(db.Model):
    """
        This is a third-party table for recording the n to n relationship
        between "Order" table and "ModelType" table.

        Each line in this table records a specific model type and a order
    """
    __tablename__ = 'order_model_types'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    model_type_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))
    count = db.Column(db.Integer, default=1)  # how many this model type the user bought in this order
    unit_pay = db.Column(db.Float,
                         nullable=False)  # how much the user really paid for each of this model (unit_pay*count=total payment of this model)
    # refund record (this can be none)
    refunds = db.relationship('Refund', backref='order_model_type', lazy='dynamic')

    def __repr__(self):
        return '<OrderModelType order_id: %r --- model_type: %r * %r>' % (self.order_id, self.model_type_id, self.count)


class Cart(db.Model):
    """
    This is a table for recording the n to n relationship between
    a user and a specific model type of a product
    1 user --> n model types of products
    1 model type --> n users
    """
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model_type_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))
    count = db.Column(db.Integer, default=1)  # how many this model type the user have in their cart
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Cart user: %r --- model_type: %r * %r>' % (self.user, self.model_type, self.count)


class Comment(db.Model):
    """
        a table for storing the comments of products (star + text)
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    pictures = db.relationship('CommentPic', backref='comment', lazy='dynamic')  # 1 comment --> n pictures
    model_type_id = db.Column(db.Integer, db.ForeignKey('model_types.id'), nullable=False)  # 1 model type --> n comment
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 1 user --> n comment
    star_num = db.Column(db.Integer, nullable=False)  # this records the star that the user rated this product

    def __repr__(self):
        return '<Comment %r>' % self.content[:10]


class CommentPic(db.Model):
    """
        a table for storing all the pictures of the comments of a model type of a products
    """
    __tablename__ = 'comment_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))  # 1 comment --> n picture

    def __repr__(self):
        return '<CommentPic %r>' % self.address


'''
    This is a table for containing the 'n to n' relationship of Product model and Category model 
'''
ProductCategory = db.Table('product_category',
                           db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
                           db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
                           )


class Product(db.Model):
    """
        a table for storing all the products in our website
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    # e.g. b1-c1-t1-a1
    serial_prefix = db.Column(db.String(64), nullable=False)
    # e.g. 2
    serial_rank = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    release_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    # 1 product --> n categories;  1 category --> n products
    categories = db.relationship('Category', secondary=ProductCategory, backref=db.backref('products', lazy='dynamic'),
                                 lazy='dynamic')
    # 1 product --> 1 brand; 1 brand --> n product
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    # 1 product --> n model types
    model_types = db.relationship('ModelType', backref='product', lazy='dynamic')

    @staticmethod
    def insert_products():
        for product_info in product_list:
            name = product_info[0]
            serial_prefix = product_info[2]
            serial_rank = product_info[3]

            """ brand and categories are random now for test!!! """
            new_product = Product(name=name, brand_id=random.randint(1, 5), serial_prefix=serial_prefix,
                                  serial_rank=serial_rank)
            db.session.add(new_product)

            """ add categories """
            # cate group1: 1-6, group2: 7-52, group3: 53-56
            cate1_id = random.randint(1, 6)
            cate2_id = random.randint(7, 52)
            cate3_id = random.randint(53, 56)
            cate1 = Category.query.get(cate1_id)
            cate2 = Category.query.get(cate2_id)
            cate3 = Category.query.get(cate3_id)
            new_product.categories.append(cate1)
            new_product.categories.append(cate2)
            new_product.categories.append(cate3)
            db.session.add(new_product)

        db.session.commit()

    def delete(self):
        """
            Mark this product as is_deleted and also
            mark all its model types as is_deleted
        """
        self.is_deleted = True
        db.session.add(self)
        for m in self.model_types:
            m.is_deleted = True
            db.session.add(m)
        db.session.commit()

    def get_exist_model_types(self):
        """
        :return: A list of model types that are not deleted
        """
        return self.model_types.filter_by(is_deleted=False).all()

    def get_serial_number(self):
        """
        Concat the serial_prefix with serial_rank to form the real serial number
        e.g. b1-c1-t1-a1 + 2 >> b1-c1-t1-a1-2
        :return: The serial number string
        """
        return '{}-{}'.format(self.serial_prefix, self.serial_rank)


class ModelTypePic(db.Model):
    """
        Each model type of a product can have a group of pictures
    """
    __tablename__ = 'model_type_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), default='upload/model_type/default.png')
    model_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))  # 1 model type --> n picture

    def __repr__(self):
        return '<ModelTypePic %r>' % self.address


class ModelTypeIntroPic(db.Model):
    """
        Each model type of a product can have a group of intro pictures.
        Intro pictures are the pictures in the detail pages, when you scroll down you can see them.
        Using the same technology as what JD company do.
    """
    __tablename__ = 'model_type_intro_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), default='upload/model_type_intro/default.png')
    model_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))  # 1 model type --> n picture

    def __repr__(self):
        return '<ModelTypeIntroPic %r>' % self.address


class ModelType(db.Model):
    """
        A single product can contain several different specific model types
        For example, different colors or something...
        Each model of a product may have different name, price, pictures and descriptions
        1 ModelType -> 1 Product
        1 Product -> n ModelType
    """
    __tablename__ = 'model_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    price = db.Column(db.Float)
    stock = db.Column(db.Integer, default=0, nullable=False)
    serial_number = db.Column(db.String(128), nullable=False)
    release_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    # 1 user(staff) --> n model type
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 1 model --> 1 product
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    # 1 model --> n comments
    comments = db.relationship('Comment', backref='model_type', lazy='dynamic')
    # 1 model --> n pictures
    pictures = db.relationship('ModelTypePic', backref='model_type', lazy='dynamic')
    # 1 model --> n intro pictures
    intro_pictures = db.relationship('ModelTypeIntroPic', backref='model_type', lazy='dynamic')
    # 1 model --> n cart (relation)
    carts = db.relationship('Cart', backref='model_type', lazy='dynamic')
    # 1 model -> n OrderModelType; 1 OrderModelType -> 1 model
    order_model_types = db.relationship('OrderModelType', backref='model_type', lazy='dynamic')

    def delete(self):
        """
            Mark this Model type as is_deleted
        """
        self.is_deleted = True
        db.session.add(self)
        db.session.commit()

    def get_serial_number(self):
        """
        Concat the serial_prefix and serial_rank of the product of this model,
        then concat it with the serial_number of this model to form the complete serial number of this model.
        e.g. (b1-c1-t1-a1 + 2) + m1 >> b1-c1-t1-a1-2-m1
        :return: The real complete serial number string
        """
        return '{}-{}'.format(self.product.get_serial_number(), self.serial_number)

    @staticmethod
    def insert_model_types():
        """
            For creating some model type information into db for showing and testing.
            This method should be called after calling the insert_products methods.
        """
        for i in range(200):
            # create some information for showing
            name = 'Model' + str(i)
            description = 'This is the test Model Type NO.' + str(i)
            price = random.randint(2000, 999999)
            stock = random.randint(100, 500)
            serial_number = 'M' + str(i)
            user_id = [3, 4][random.randint(0, 1)]
            product_id = random.randint(1, 10)
            # create the object of this model type
            new_mt = ModelType(name=name, description=description, price=price, stock=stock,
                               serial_number=serial_number, user_id=user_id, product_id=product_id)
            db.session.add(new_mt)
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    @staticmethod
    def insert_categories():
        """
            This is a method for inserting the categories into the database.
            This should be used a single time in the terminal.
            This should be called before calling the Product.insert_products()
        """
        for cate_name in category_list:
            new_category = Category(name=cate_name)
            db.session.add(new_category)
        db.session.commit()


class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    products = db.relationship('Product', backref='brand', lazy='dynamic')  # 1 brand --> n product

    def __repr__(self):
        return '<Brand %r>' % self.name

    @staticmethod
    def insert_brands():
        """
            This is a method for inserting the brands into the database.
            This should be used a single time in the terminal.
            This should be called before calling the Product.insert_products()
        """
        for brand_name in brand_list:
            new_brand = Brand(name=brand_name)
            db.session.add(new_brand)
        db.session.commit()


class Premium(db.Model):
    """
        The table records the premium membership info.
        1 user (customer) -> n premium (each period of premium is regarded as a record in our db)
        (in a specific period of time, a user can possess only a single premium membership)
        1 premium -> 1 user (customer)
    """
    __tablename__ = 'premiums'
    id = db.Column(db.Integer, primary_key=True)
    # 1 premium -> 1 user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime(), default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)  # the unit is 'day': 7, 30, 365
    is_expired = db.Column(db.Boolean, default=False)

    def expire(self):
        """
            The function fot expire this piece of record
        """
        self.is_expired = True
        db.session.commit()


class Address(db.Model):
    """
        The table records the address of delivery.
        1 address -> 1 user (customer)
        1 user (customer) -> n addresses
    """
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    recipient_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(24), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    province_or_state = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    district = db.Column(db.String(128), nullable=False)
    # 1 address -> 1 user (customer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Permission:
    """
    Using integers to represent different permissions
    all the number are 2^n
    so that the sum of a group of permission numbers
    can represent a sole group of permissions.
    This means when we get a sum number, we can know which permissions the user owns.
    """
    UPLOAD_PRODUCT = 1
    VIEW_ALL_PRODUCT = 2
    GRADE_STARS = 4
    COMMENT = 8
    VIEW_ALL_COMMENTS = 16
    ADMIN = 32
    REMOVE_PRODUCT = 64


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)  # we will set the 'customer' as default role
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')  # 1 role --> n users

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        # initialize the permissions
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    # ----- functions for permission management (learned from the book) -----
    # book: 'Flask Web Development: Developing Web Applications with Python, Second Edition'
    def has_permission(self, perm):
        return self.permissions & perm == perm

    def reset_permission(self):
        self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    @staticmethod
    def insert_roles():
        """
            a static method for creating the roles into the db (use this in the flask shell!!)
        """
        # a roles dict, keys are roles, values are permission of the role
        roles = {
            'Customer': [Permission.VIEW_ALL_PRODUCT, Permission.GRADE_STARS, Permission.COMMENT,
                         Permission.VIEW_ALL_COMMENTS],
            'Staff': [Permission.VIEW_ALL_PRODUCT, Permission.GRADE_STARS, Permission.COMMENT,
                      Permission.VIEW_ALL_COMMENTS, Permission.UPLOAD_PRODUCT]
        }

        # set the default role as 'customer'
        default_role = 'Customer'

        # loop through the roles dict
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            # if the user object is not in db yet, we will create one
            if role is None:
                role = Role(name=r)

            # loop through the permissions of this role
            for perm in roles[r]:
                # give those permissions to this role
                role.add_permission(perm)

            # if this role is the default role (Customer), we set the field of "default" as True
            role.default = (role.name == default_role)

            # add this object to the database session
            db.session.add(role)

        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    start_datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.String(256), default='upload/avatar/default__0__.jpg')  # The avatar
    theme = db.Column(db.String(16), default='light')  # the user preferred theme of our website
    language = db.Column(db.String(16), default='en')
    about_me = db.Column(db.Text(300))
    gender = db.Column(db.String(16), default='Unknown')  # 3 possible values: 'Male', 'Female', 'Unknown'
    exp = db.Column(db.Integer, default=0)  # the experience (level) of the user
    is_premium = db.Column(db.Boolean, default=False)
    premium_left_days = db.Column(db.Integer, default=0)  # the day left of the premium membership
    is_deleted = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 1 role --> n users

    # released_products = db.relationship('Product', backref='seller', lazy='dynamic')  # 1 user --> n products
    # released_comments = db.relationship('Comment', backref='author', lazy='dynamic')  # 1 user --> n comments
    # released_comment_replies = db.relationship('ReplyComment', backref='author', lazy='dynamic')  # 1 user --> n replies
    # # 1 product --> rated ranked by n users; 1 user --> can rank n products
    # rated_product_relations = db.relationship('UserProductRate', backref='user', lazy='dynamic')
    # cart_relations = db.relationship('Cart', backref='user', lazy='dynamic')
    # history_relations = db.relationship('History', backref='user', lazy='dynamic')

    # 1 user(customer) --> n cart (relation)
    carts = db.relationship('Cart', backref='user', lazy='dynamic')
    # 1 user(customer) --> n comments
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    # 1 user(customer) --> n orders
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    # chat room relationship (For version 2)
    chat_rooms_customer = db.relationship('ChatRoom', foreign_keys=[ChatRoom.customer_id],
                                          backref=db.backref('customer', lazy='joined'), lazy='dynamic',
                                          cascade='all, delete-orphan')
    chat_rooms_staff = db.relationship('ChatRoom', foreign_keys=[ChatRoom.staff_id],
                                       backref=db.backref('staff', lazy='joined'), lazy='dynamic',
                                       cascade='all, delete-orphan')
    # 1 user(staff) --> n products
    model_types = db.relationship('ModelType', backref='staff', lazy='dynamic')
    # 1 user (customer) -> n addresses
    addresses = db.relationship('Address', backref='customer', lazy='dynamic')
    # 1 user (customer) -> n premiums (in a specific period of time, a user can possess only a single premium membership)
    premiums = db.relationship('Premium', backref='customer', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def insert_users():
        """
        This is a method for inserting the testing user information, which means fulling the User table.
        This should be used in the console only a single time.
        """
        for user_info in user_list:
            email = user_info[0]
            username = user_info[1]
            password = user_info[2]
            role_id = user_info[3]

            new_user = User(email=email, username=username, password=password, role_id=role_id)

            db.session.add(new_user)
        db.session.commit()

    # ----- use Werkzeug to generate and check the password hash of the user password (learned from the book) -----
    # book: 'Flask Web Development: Developing Web Applications with Python, Second Edition'
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ----- The management of permissions of a user (learned from the book) -----
    # book: 'Flask Web Development: Developing Web Applications with Python, Second Edition'
    def can(self, perm):
        """
        Check whether a user has a specific permission
        :param perm: the permission to be checked
        :return: true means yes while false means no
        """
        return self.role is not None and self.role.has_permission(perm)

    # ------ functions related to the premium membership
    def get_current_premium(self):
        """
            A function for get the obj of current premium membership.
        """
        if self.is_premium:
            for p in self.premiums.all():
                if not p.is_expired:
                    return p
        else:
            return None

    def become_premium_member(self, duration: int):
        """
        Call this function to set this user as the premium member.
        :param duration: the duration of this new premium membership, unit is 'day'
        """

        # mark the current premium record as expired
        # (if this is a renewal of membership, we still need to let only a single record be marked as not expired)
        p = self.get_current_premium()
        if p:
            p.expire()

        # create a obj of new premium record
        new_premium = Premium(user_id=self.id, duration=duration)

        # update the premium Columns in this table
        self.is_premium = True
        self.premium_left_days += new_premium.duration
        db.session.commit()

    def expire_premium_member(self):
        """
            Call this function to deprive the premium member ship of this user
        """
        # mark the current premium records as 'expired'
        p = self.get_current_premium()
        if p:
            p.expire()

        # update the premium Columns in this table
        self.is_premium = False
        self.premium_left_days = 0
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    """ This is required by Flask-Login extension """
    return User.query.get(int(user_id))
