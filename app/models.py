from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from faker import Faker

from app import db
from app.table_info import category_list, brand_list, user_list, product_list

from . import login_manager

import random

from .prestore.product_info import pm_lst
from .prestore.index_slide_prestore import pm_lst as pm_lst_index
from .prestore.product_info_g import pm_lst as pm_lst_g
from .prestore.product_info_l import pm_lst as pm_lst_l
from .prestore.product_info_t import pm_lst as pm_lst_t


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
        TheSiren.create_unique_instance()  # Create the global unique instance of this musical shop
        Role.insert_roles()  # roles of users
        User.insert_users(50, 2)  # the constant user accounts for test
        Recipient.insert_recipients(100)  # the recipient info
        Address.insert_address()  # addresses for delivery
        # # users(100)  # 100 fake users
        Category.insert_categories()  # the product categories
        Brand.insert_brands()  # the product brands
        # Product.insert_products()  # the constant products for show
        # ProductPic.insert_pictures()  # the pictures of the constant products
        # ------
        # Tools.insert_pm()   # pre-stored product and mt info
        Tools.insert_pm_glt(pm_lst_index,
                            'index_slide')  # (!!! This must be the first of all fake models !!! ) That 5 products in the index slide window
        Tools.insert_pm_glt(pm_lst_g, 'g')
        Tools.insert_pm_glt(pm_lst_l, 'l')
        Tools.insert_pm_glt(pm_lst_t, 't')
        # ------
        # # products(100)  # 100 fake products
        # ModelType.insert_model_types()  # the constant model types for testing
        # insert 3D files and texture files
        Tools.insert_3d_for_mt()
        Comment.insert_comments(12)
        Cart.insert_carts()
        Order.insert_orders(20)
        OrderModelType.insert_omts()
        # insert journals
        Journal.insert_journals(50)

        # chat message
        Message.insert_messages(30)

    @staticmethod
    def insert_3d_for_mt():
        """
        This should be called after calling all of the other insert functions
        """
        # insert the 3D model file and texture file for that cello model type (id=13)
        cello = ModelType.query.get(13)
        cello.three_d_model_texture_address = "upload/model_type/3d-model-texture-files/pre-store/cello.png"
        cello.three_d_model_address = "upload/model_type/3d-model-files/pre-store/cello.fbx"
        # to ensure this can be shown as the first several products
        cello.views = 4685267
        cello.sales = 1562
        db.session.add(cello)
        db.session.commit()


    @staticmethod
    def insert_pm_glt(pm_list, member_code):
        """
        Insert the pre-stored products and its models into the database.
        :param pm_list: This parameter can be different pm_lst that created by different group member
        :param member_code: The value can be "g", "l" or "t"
        """
        for p_info in pm_list:
            # get product info
            p_name = p_info[0]
            brand_id = p_info[1]
            cate_id_c = p_info[2]
            cate_id_t = p_info[3]
            cate_id_a = p_info[4]
            mt_lst = p_info[5]

            """ create the product first """
            # create the serial_prefix
            serial_prefix = "b{}-c{}-t{}-a{}".format(brand_id, cate_id_c, cate_id_t - 6, cate_id_a - 52)
            # query for the serial_rank
            serial_rank = 1 + Product.query.filter_by(serial_prefix=serial_prefix).count()
            # create Product
            new_product = Product(serial_prefix=serial_prefix,
                                  serial_rank=serial_rank,
                                  name=p_name,
                                  brand_id=brand_id)
            # add categories
            cate_c = Category.query.get(cate_id_c)
            cate_t = Category.query.get(cate_id_t)
            cate_a = Category.query.get(cate_id_a)
            new_product.categories.append(cate_c)
            new_product.categories.append(cate_t)
            new_product.categories.append(cate_a)
            # add to db session
            db.session.add(new_product)

            """ create the model types """
            for mt_info in mt_lst:
                # get model type info
                mt_name = mt_info[0]
                description = mt_info[1]
                price = mt_info[2]
                weight = mt_info[3]
                pic_lst = mt_info[4]
                video_address = ""
                # if there is a video (no audio)
                if len(mt_info) == 6:
                    video_address = 'upload/model_type/videos/{}'.format(mt_info[5])

                # generate some random info
                stock = random.randint(100, 500)
                sales = random.randint(0, 300)
                views = random.randint(0, 50000)
                serial_number = 'M{}'.format(ModelType.query.count() + 1)
                user_id = [3, 4][random.randint(0, 1)]
                # create this model type object
                new_mt = ModelType(name=mt_name,
                                   description=description,
                                   price=price,
                                   weight=weight,
                                   stock=stock,
                                   sales=sales,
                                   views=views,
                                   serial_number=serial_number,
                                   user_id=user_id,
                                   product=new_product,
                                   video_address=video_address)
                # add to db session
                db.session.add(new_mt)

                """ add audio relation if there has some """
                # if there is a list of audio (may be no video, but at least the video section should be "")
                if len(mt_info) == 7:
                    # read the audio addresses
                    audio_name_lst = mt_info[6]
                    for audio_name in audio_name_lst:
                        audio_address = 'upload/model_type/audios/{}'.format(audio_name)
                        # create a new Audio obj
                        new_audio = Audio(address=audio_address, model_type=new_mt)
                        db.session.add(new_audio)
                    db.session.commit()

                """ create picture objects for this mt """
                for pic_name in pic_lst:
                    # the pictures gathered by different member are stored in different dirs
                    if member_code == 'g' or member_code == 'l' or member_code == 't' or member_code == 'index_slide':
                        address = "upload/model_type/prestore_{}/{}".format(member_code, pic_name)
                    else:
                        address = "upload/model_type/default.jpg"
                    # create the picture obj
                    new_mtp = ModelTypePic(model_type=new_mt, address=address)
                    # add to db session
                    db.session.add(new_mtp)

        # commit db session
        db.session.commit()

    @staticmethod
    def insert_pm():
        """
        Insert the pre-stored products and its models into the database.
        :return:
        """
        for p_info in pm_lst:
            # get product info
            p_name = p_info[0]
            brand_id = p_info[1]
            cate_id_c = p_info[2]
            cate_id_t = p_info[3]
            cate_id_a = p_info[4]
            mt_lst = p_info[5]

            """ create the product first """
            # create the serial_prefix
            serial_prefix = "b{}-c{}-t{}-a{}".format(brand_id, cate_id_c, cate_id_t, cate_id_a)
            # query for the serial_rank
            serial_rank = 1 + Product.query.filter_by(serial_prefix=serial_prefix).count()
            # create Product
            new_product = Product(serial_prefix=serial_prefix,
                                  serial_rank=serial_rank,
                                  name=p_name,
                                  brand_id=brand_id)
            # add categories
            cate_c = Category.query.get(cate_id_c)
            cate_t = Category.query.get(cate_id_t)
            cate_a = Category.query.get(cate_id_a)
            new_product.categories.append(cate_c)
            new_product.categories.append(cate_t)
            new_product.categories.append(cate_a)
            # add to db session
            db.session.add(new_product)

            """ create the model types """
            for mt_info in mt_lst:
                # get model type info
                mt_name = mt_info[0]
                description = mt_info[1]
                price = mt_info[2]
                weight = mt_info[3]
                pic_lst = mt_info[4]
                # generate some random info
                stock = random.randint(100, 500)
                sales = random.randint(0, 300)
                views = random.randint(0, 50000)
                serial_number = 'M{}'.format(ModelType.query.count())
                user_id = [3, 4][random.randint(0, 1)]
                # create this model type object
                new_mt = ModelType(name=mt_name,
                                   description=description,
                                   price=price,
                                   weight=weight,
                                   stock=stock,
                                   sales=sales,
                                   views=views,
                                   serial_number=serial_number,
                                   user_id=user_id,
                                   product=new_product)
                # add to db session
                db.session.add(new_mt)

                """ create picture objects for this mt """
                for pic_name in pic_lst:
                    address = "upload/model_type/prestore/{}".format(pic_name)
                    new_mtp = ModelTypePic(model_type=new_mt, address=address)
                    # add to db session
                    db.session.add(new_mtp)

        # commit db session
        db.session.commit()

    @staticmethod
    def delete_instance_state(dic):
        # This method is for deleting the following item in dict
        # This item is not JSON serializable, and we do not need it
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        return dic

    @staticmethod
    def add_relation_to_dict(dic, relations, key_name):
        """
        This method is for adding the relation objects (in a list) in to the dictionary.
        For example, adding carts relations into the JSON dict of a model type object.
        :param dic: The JSON dict of a model type
        :param relations: A db Model relation, for examples, carts, pictures...
        :param key_name: The name of the key of the newly added item
        :return: The dictionary after adding the relations
        """
        relation_lst = []
        for r in relations:
            relation_lst.append(r.to_dict())
        dic[key_name] = relation_lst

    @staticmethod
    def bytes_to_human_readable_str(number):
        """
        Transform the number to and human readable str.
        e.g. 1000 -> 1k, 10000 -> 10k, 10000000 -> 10M
        :param number: The original number
        :return: A string after formatting process
        """
        if number < 1024:  # bit
            number = str(round(number, 2))                    # B
        elif number >= 1024 and number < 1024 * 1024:
            number = str(round(number / 1024, 2)) + 'K'              # KB
        elif number >= 1024 * 1024 and number < 1024 * 1024 * 1024:
            number = str(round(number / 1024 / 1024, 2)) + 'M'
        elif number >= 1024 * 1024 * 1024 and number < 1024 * 1024 * 1024 * 1024:
            number = str(round(number / 1024 / 1024 / 1024, 2)) + 'G'
        elif number >= 1024 * 1024 * 1024 * 1024 and number < 1024 * 1024 * 1024 * 1024 * 1024:
            number = str(round(number / 1024 / 1024 / 1024 / 1024, 2)) + 'T'
        elif number >= 1024 * 1024 * 1024 * 1024 * 1024 and number < 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
            number = str(round(number / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + 'P'
        elif number >= 1024 * 1024 * 1024 * 1024 * 1024 * 1024 and number < 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
            number = str(round(number / 1024 / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + 'E'
        return number


class BaseModel(db.Model):
    """
        This is a base model, which should be the superclass of all
        the other Model classes
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        """
            Map the object to dictionary data structure
        """
        # turn columns into items in dictionary
        result = self.__dict__.copy()
        return result


class Journal(BaseModel):
    """
        The journal that staff can upload
    """
    __tablename_ = 'journals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), default="Untitled")   # about 25 words
    text = db.Column(db.Text(5120), nullable=False)     # about 1000 words
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def insert_journals(count: int):
        journals = [
            ['Gibson Discount', 'Gibson guitars are on sale, go to check it!  Gibson guitars are on sale, go to check it! Gibson guitars are on sale, go to check it! Gibson guitars are on sale, go to check it! Gibson guitars are on sale, go to check it! Gibson guitars are on sale, go to check it! Gibson guitars are on sale, go to check it!'],
            ['Welcome to The Siren', 'Welcome to our online musical instrument shop, here you will be provided the best services. Welcome to our online musical instrument shop, here you will be provided the best services. Welcome to our online musical instrument shop, here you will be provided the best services. Welcome to our online musical instrument shop, here you will be provided the best services. Welcome to our online musical instrument shop, here you will be provided the best services. Welcome to our online musical instrument shop, here you will be provided the best services. Welcome to our online musical instrument shop, here you will be provided the best services.'],
            ['New Function', 'Quality communication with our staffs is available now, just try it! Quality communication with our staffs is available now, just try it! Quality communication with our staffs is available now, just try it! Quality communication with our staffs is available now, just try it! Quality communication with our staffs is available now, just try it! Quality communication with our staffs is available now, just try it! Quality communication with our staffs is available now, just try it!'],
            ['Payment Security', 'Alipay is cooperating with us, you can pay for your order with Alipay. Alipay is cooperating with us, you can pay for your order with Alipay. Alipay is cooperating with us, you can pay for your order with Alipay. Alipay is cooperating with us, you can pay for your order with Alipay. Alipay is cooperating with us, you can pay for your order with Alipay. Alipay is cooperating with us, you can pay for your order with Alipay. Alipay is cooperating with us, you can pay for your order with Alipay.']
        ]
        for i in range(count):
            # get a random journal
            journal_index = random.randint(0, len(journals)-1)
            journal = journals[journal_index]

            # get a random staff as the author
            staffs = User.query.filter_by(role_id=2, is_deleted=False).all()
            author_id = staffs[random.randint(0, len(staffs)-1)].id

            new_journal = Journal(title=journal[0], text=journal[1], author_id=author_id)
            db.session.add(new_journal)
        db.session.commit()


class TheSiren(BaseModel):
    """
        This table stores only a single instance of this musical shop.
        There should be a single global instance of this row of table.
    """
    __tablename__ = 'the_siren'
    id = db.Column(db.Integer, primary_key=True)
    epidemic_mode_on = db.Column(db.Boolean, default=False)  # whether the shop owner turns on the "epidemic mode"

    @staticmethod
    def create_unique_instance():
        if TheSiren.query.count() == 0:
            unique_instance = TheSiren()
            db.session.add(unique_instance)
            db.session.commit()


class Refund(BaseModel):
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

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     return Tools.delete_instance_state(super(Refund, self).to_dict())


# class Change(db.Model):
#     pass

class ChatRoom(BaseModel):
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

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     result = super(ChatRoom, self).to_dict()
    #     # add relations to the result dict
    #     Tools.add_relation_to_dict(result, self.messages.all(), "messages")
    #     return Tools.delete_instance_state(result)


class Message(BaseModel):
    """
        (Chatting version 2 ->  + Message)
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
    # possible values: 'normal', 'consult', 'after-sale'
    chat_type = db.Column(db.String(12), default='normal')
    # Which chatting room this message belongs to
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'))

    # model_type for msg in type of "consult" (only auto consult msg have this)
    model_type_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))
    # order for msg in type of "after-sale" (only auto after-sale msg have this)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def __repr__(self):
        return '<Chat %r>' % self.content[:10]

    @staticmethod
    def insert_messages(count):
        fake = Faker()
        for i in range(count):
            room_id = random.randint(1, 2)
            author_type_list = ['customer', 'staff']
            author_type = random.randint(0, 1)
            new_message = Message(content=fake.text(), timestamp=fake.past_datetime(),
                                  author_type=author_type_list[author_type], chat_room_id=room_id)
            db.session.add(new_message)
        db.session.commit()

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     return Tools.delete_instance_state(super(Message, self).to_dict())


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


class Order(BaseModel):
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
    out_trade_no = db.Column(db.String(64),
                             unique=True)  # trade number, which should be unique inside a same retailer (us), includes numbers, letters and '_' only
    trade_no = db.Column(db.String(72), unique=True)  # this is generated by Alipay for each order after payment
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    order_type = db.Column(db.String(20), default='delivery')  # 'delivery' or 'self-collection'
    delivery_fee = db.Column(db.Integer, default=9)  # if the order_type is 'self-collection', delivery fee should be 0
    gross_payment = db.Column(
        db.Float)  # total amount without discount (delivery_fee + items) # only 2 digits in decimal e.g. 10.xx
    paid_payment = db.Column(
        db.Float)  # real amount need to pay (delivery_fee + items*discount) # only 2 digits in decimal e.g. 10.xx
    status_code = db.Column(db.Integer, default=0)  # the status code of this order
    priority = db.Column(db.Integer, default=1)     # 1, 2, 3
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # the uid of the customer who owns this order
    timestamp_1 = db.Column(db.DateTime(), index=True)  # time record of status changing to 'preparing'
    timestamp_2 = db.Column(db.DateTime(), index=True)  # time record of status changing to 'on delivery'
    timestamp_3 = db.Column(db.DateTime(), index=True)  # time record of status changing to 'waiting got collection'
    timestamp_4 = db.Column(db.DateTime(), index=True)  # time record of status changing to 'finished'
    timestamp_5 = db.Column(db.DateTime(), index=True)  # time record of status changing to 'canceled'
    timestamp_6 = db.Column(db.DateTime(), index=True)  # time record of status changing to 'expired'
    # 1 order -> 1 Addresses; 1 Address -> n order
    # address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    # 1 order (self-collection) -> 1 recipient
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipients.id'))
    # 1 order -> n OrderModelType; 1 OrderModelType -> 1 order
    order_model_types = db.relationship('OrderModelType', backref='order', lazy='dynamic')
    # record the detailed address as an string
    address_text = db.Column(db.String)
    # 1 order --> n msg (after-sale)
    msgs = db.relationship('Message', backref='order', lazy='dynamic')

    @staticmethod
    def insert_orders(count):
        # a order for test
        test_order = Order(status_code=0, user_id=1, order_type='self-collection')
        # need recipient info
        test_order.recipient_id = random.randint(1, Recipient.query.count())
        db.session.add(test_order)
        db.session.commit()
        test_order.generate_unique_out_trade_no()

        # create a faker instance
        faker = Faker()
        # create some new orders into db
        for i in range(count):
            new_order = Order(timestamp=faker.past_datetime(), user_id=1,
                              order_type=["delivery", "self-collection"][random.randint(0, 1)])
            if new_order.order_type == "delivery":
                # need address and recipient info
                address_id = random.randint(1, Address.query.count())
                address = Address.query.get(address_id)
                new_order.address_text = address.get_address()
                new_order.recipient_id = address.recipient.id
                new_order.status_code = [0, 1, 2, 4, 5, 6][random.randint(0, 5)]
            elif new_order.order_type == "self-collection":
                # need recipient info
                new_order.recipient_id = random.randint(1, Recipient.query.count())
                new_order.status_code = [0, 1, 3, 4, 5, 6][random.randint(0, 5)]
            db.session.add(new_order)
            db.session.commit()
            new_order.generate_unique_out_trade_no()

    def to_dict(self):
        """ Map the object to dictionary data structure """
        result = super(Order, self).to_dict()
        # change status code to statement
        result["status"] = self.get_status()
        # add model list to this dict
        model_types = []
        for omt in self.order_model_types.all():
            model_types.append(omt.model_type.to_dict())
        result['model_types'] = model_types
        if self.address is not None:
            # add address to this dict
            result['address'] = self.address.to_dict()
        if self.recipient is not None:
            # add address to this dict
            result['recipient'] = self.recipient.to_dict()
        return Tools.delete_instance_state(result)

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

    def generate_delivery_fee(self):
        """
        Premium members can enjoy delivery for free.
        The base fee is 9 RMB (within 1 kg), every extra 1 kg contributes to an extra fee of 2 RMB.
        The weight fee is up rounded. e.g. 2.x kg -> 3.0 kg (x > 0)
        The top limit is 200 RMB.
        Then the field 'delivery_fee' will be filled.
        :return:
        """
        # premium members get a free delivery
        if self.user.is_premium:
            fee = 0
        else:
            if self.order_type == "delivery":
                # calculate the total weight in order
                total_weight = 0
                for omt in self.order_model_types:
                    total_weight += omt.model_type.weight * omt.count

                # less than 1 kg, is the base fee of 9 RMB
                if total_weight < 1:
                    fee = 9
                else:
                    # calculate the extra fee
                    total_weight -= 1
                    # The weight is up rounded. e.g. 2.x kg -> 3.0 kg (x > 0)
                    if total_weight > (total_weight // 1):
                        total_weight = (total_weight // 1) + 1
                    # fee = base + extra
                    fee = 9 + (total_weight * 2)
                    if fee > 200:
                        fee = 200
            else:
                fee = 0

        # write delivery_fee into db
        self.delivery_fee = fee
        db.session.add(self)
        db.session.commit()

        return fee

    def generate_payment(self):
        """
        This function calculates the "gross payment" of this order (delivery + commodities)
        This function also calculates the "paid payment" of this order (delivery + commodities*discount)
        Then the field 'gross_payment' will be filled.
        Then the field 'paid_payment' will be filled.
        :return: gross_payment
        """
        payment = 0

        # add delivery fee
        if self.order_type == 'delivery':
            payment += self.delivery_fee

        # calculate and add fee for commodities
        payment_commodity = 0
        for omt in self.order_model_types:
            payment_commodity += (omt.model_type.price * omt.count)

        # record the total payment
        gross_payment = payment + payment_commodity
        gross_payment = round(gross_payment, 2)  # remain 2 digits in decimal place
        self.gross_payment = gross_payment

        # record the real amount should be paid
        # check the premium discount
        if self.user.is_premium:
            payment_commodity *= 0.95
        paid_payment = payment + payment_commodity
        paid_payment = round(paid_payment, 2)  # remain 2 digits in decimal place
        self.paid_payment = paid_payment

        # commit to db
        db.session.add(self)
        db.session.commit()

    def generate_unique_out_trade_no(self):
        """
        for generating the unique out_trade_no, which is required by Alipay.
        We add a random number and timestamp with order_id
        The field 'out_trade_no' will be filled.
        :return: out_trade_no
        """
        # get current datetime
        datetime_suffix = str(datetime.utcnow()).replace(" ", "").replace(":", "").replace('-', '').replace('.', '')
        # get a random int
        random_num_suffix = random.randint(0, 99999999999999999999)
        # form the out_trade_no ('I' refers to instruments)
        out_trade_no = '{}_{}_{}_{}'.format('I', self.id, random_num_suffix, datetime_suffix)
        # the max length is 64
        if len(out_trade_no) > 64:
            out_trade_no = out_trade_no[0:64]

        # add the out_trade_no to this obj
        self.out_trade_no = out_trade_no
        db.session.add(self)
        db.session.commit()

        return out_trade_no

    def update_model_info(self):
        """
        This function is used to update the
            stock number
        AND sale number
        of each model type in this order.
        The stock of these model types will be decreased by the count of it in this order.
        """
        for omt in self.order_model_types:
            # get the model type
            mt = omt.model_type
            # update the stock of this model type
            mt.stock = mt.stock - omt.count
            mt.sales = mt.sales + omt.count
            db.session.add(mt)
        db.session.commit()


class OrderModelType(BaseModel):
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
    is_commented = db.Column(db.Boolean, default=False)  # is this model in this order is already commented
    # refund record (this can be none)
    refunds = db.relationship('Refund', backref='order_model_type', lazy='dynamic')

    def __repr__(self):
        return '<OrderModelType order_id: %r --- model_type: %r * %r>' % (self.order_id, self.model_type_id, self.count)

    @staticmethod
    def insert_omts():
        """ we ensure each fake order has at least one order model type """
        # get all the orders
        order_lst = Order.query.all()
        for order in order_lst:
            # for each order, we get a random number of model types being included.
            omt_count = random.randint(1, 6)
            total_mt_count = ModelType.query.count()
            model_type_set = set()
            for i in range(omt_count):
                # ensure model types in a order are different
                mt = ModelType.query.get(random.randint(1, total_mt_count))
                while mt in model_type_set:
                    mt = ModelType.query.get(random.randint(1, total_mt_count))
                model_type_set.add(mt)
            # create omts for this order using the selected models
            for mt in model_type_set:
                new_omt = OrderModelType(order=order, model_type=mt, count=random.randint(1, 3), unit_pay=mt.price)
                db.session.add(new_omt)
            # update the payment of order
            order.generate_delivery_fee()
            order.generate_payment()
        db.session.commit()

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     result = super(OrderModelType, self).to_dict()
    #     # add relations to the result dict
    #     Tools.add_relation_to_dict(result, self.refunds.all(), "refunds")
    #     return Tools.delete_instance_state(result)


class Cart(BaseModel):
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

    def to_dict(self):
        """
            Map the object to dictionary data structure
        """
        return Tools.delete_instance_state(super(Cart, self).to_dict())

    @staticmethod
    def insert_carts():
        for i in range(50):
            # random info
            user_id = [1, 2][random.randint(0, 1)]
            model_type = ModelType.query.get(random.randint(1, ModelType.query.count()))
            count = random.randint(1, 15)
            # generate a new cart relation
            new_cart = Cart(user_id=user_id, model_type=model_type, count=count)
            db.session.add(new_cart)
        db.session.commit()


class Comment(BaseModel):
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

    def to_dict(self):
        """
            Map the object to dictionary data structure
        """
        result = super(Comment, self).to_dict()
        # add relations to the result dict
        Tools.add_relation_to_dict(result, self.pictures.all(), "pictures")

        return Tools.delete_instance_state(result)

    @staticmethod
    def insert_comments(count):
        content = "This is a testing comment. This is a testing comment. This is a testing comment. This is a testing comment. Pictures are also for testing. Pictures are also for testing. Pictures are also for testing. "
        pic_address_lst = [
            'upload/comment/pre-stored/1.jpg',
            'upload/comment/pre-stored/2.jpg',
            'upload/comment/pre-stored/3.png',
            'upload/comment/pre-stored/4.png',
            'upload/comment/pre-stored/5.jpg',
            'upload/comment/pre-stored/6.jpg',
            'upload/comment/pre-stored/7.jpg',
            'upload/comment/pre-stored/8.png',
            'upload/comment/pre-stored/9.jpg',
            'upload/comment/pre-stored/10.png',
            'upload/comment/pre-stored/12.jpg',
            'upload/comment/pre-stored/13.png',
            'upload/comment/pre-stored/14.jpg',
            'upload/comment/pre-stored/15.jpg',
            'upload/comment/pre-stored/16.jpg',
            'upload/comment/pre-stored/17.jpg',
            'upload/comment/pre-stored/18.jpg',
            'upload/comment/pre-stored/19.jpg',
            'upload/comment/pre-stored/20.jpg',
            'upload/comment/pre-stored/21.png'
        ]
        # get all the model types
        mt_lst = ModelType.query.all()
        # get all customers
        customer_lst = User.query.filter_by(role_id=1).all()
        # for each model type
        for mt in mt_lst:
            # create comments for this model type
            for i in range(count):
                new_comment = Comment(content=content, model_type_id=mt.id, auth_id=customer_lst[random.randint(0, len(customer_lst)-1)].id, star_num=random.randint(1, 5))
                db.session.add(new_comment)

                # create pictures for this comment
                current_pic_address_lst = []
                for j in range(random.randint(2, 5)):
                    # get an random and not repeat pic address
                    address = pic_address_lst[random.randint(0, len(pic_address_lst) - 1)]
                    while address in current_pic_address_lst:
                        address = pic_address_lst[random.randint(0, len(pic_address_lst) - 1)]
                    current_pic_address_lst.append(address)
                    # create pic obj
                    new_pic = CommentPic(address=address, comment=new_comment)
                    db.session.add(new_pic)
            db.session.commit()


class CommentPic(BaseModel):
    """
        a table for storing all the pictures of the comments of a model type of a products
    """
    __tablename__ = 'comment_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))  # 1 comment --> n picture

    def __repr__(self):
        return '<CommentPic %r>' % self.address

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     return Tools.delete_instance_state(super(CommentPic, self).to_dict())


'''
    This is a table for containing the 'n to n' relationship of Product model and Category model 
'''
ProductCategory = db.Table('product_category',
                           db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
                           db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
                           )


class Product(BaseModel):
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
            new_product = Product(name=name, brand_id=random.randint(1, Brand.query.count()),
                                  serial_prefix=serial_prefix,
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

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     result = super(Product, self).to_dict()
    #     # add relations to the result dict
    #     Tools.add_relation_to_dict(result, self.categories.all(), "categories")
    #     Tools.add_relation_to_dict(result, self.get_exist_model_types(), "model_types")
    #     return Tools.delete_instance_state(result)

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


class ModelTypePic(BaseModel):
    """
        Each model type of a product can have a group of pictures
    """
    __tablename__ = 'model_type_pictures'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(512), default='upload/model_type/default.jpg')
    model_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))  # 1 model type --> n picture

    def __repr__(self):
        return '<ModelTypePic %r>' % self.address

    def to_dict(self):
        """ Map the object to dictionary data structure """
        return Tools.delete_instance_state(super(ModelTypePic, self).to_dict())


class ModelTypeIntroPic(BaseModel):
    """
        (Abandoned)
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

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     return Tools.delete_instance_state(super(ModelTypeIntroPic, self).to_dict())


class ModelType(BaseModel):
    """
        A single product can contain several different specific model types
        For example, different colors or something...
        Each model of a product may have different name, price, pictures and descriptions
        1 ModelType -> 1 Product
        1 Product -> n ModelType

        0: nothing
        1: only 3d
        2: only audio
        3: only vedio
        4: audio & vedio
        5: 3d & vedio
        6: 3d & audio
        7: 3d & audio & vedio
    """
    __tablename__ = 'model_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    price = db.Column(db.Float)
    weight = db.Column(db.Float)  # kg
    rate = db.Column(db.Float, default=3)  # the star rating
    rate_count = db.Column(db.Integer, default=0)  # how many time this model is rated
    stock = db.Column(db.Integer, default=0)
    sales = db.Column(db.Integer, default=0)  # how many this models have been sold out
    views = db.Column(db.Integer, default=0)  # how many times its details page has been viewed
    serial_number = db.Column(db.String(128), nullable=False)
    release_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    video_address = db.Column(db.String, default=None)  # video
    three_d_model_address = db.Column(db.String, default=None)    # 3d model file
    three_d_model_texture_address = db.Column(db.String, default=None)    # 3d model texture file
    # 1 model -> n addresses, 1 address -> 1 model
    audio_addresses = db.relationship('Audio', backref='model_type', lazy='dynamic')  # audio
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
    # 1 model --> n B_histories
    browsing_histories = db.relationship('BrowsingHistory', backref='model_type', lazy='dynamic')
    # 1 model -> n customization
    customizations = db.relationship('Customization', backref='model_type', lazy='dynamic')
    # 1 model_type --> n msg (consult)
    msgs = db.relationship('Message', backref='model_type', lazy='dynamic')

    def to_dict(self):
        """
            Map the object to dictionary data structure
        """
        result = super(ModelType, self).to_dict()
        # add relations to the result dict
        # Tools.add_relation_to_dict(result, self.comments.all(), "comments")
        Tools.add_relation_to_dict(result, self.pictures.all(), "pictures")
        # Tools.add_relation_to_dict(result, self.intro_pictures.all(), "intro_pictures")
        Tools.add_relation_to_dict(result, self.carts.all(), "carts")
        # Tools.add_relation_to_dict(result, self.order_model_types.all(), "order_model_types")

        # add brand name
        result["brand_name"] = self.product.brand.name

        # add type id
        result["addition_type"] = self.get_addition_type()

        # return result
        return Tools.delete_instance_state(result)


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

    def get_formatted_views(self):
        """
        Format the number of views. e.g. 1000 -> 1k, 1000000 -> 1M
        :return: A string of formatted view number
        """
        return Tools.bytes_to_human_readable_str(self.views)

    def get_formatted_sales(self):
        """
        Format the number of sales. e.g. 1000 -> 1k, 1000000 -> 1M
        :return: A string of formatted sales number
        """
        return Tools.bytes_to_human_readable_str(self.sales)

    def get_addition_type(self):
        """
        Tells the type of additional and return it
        Types:
                0: nothing
                1: only 3d
                2: only audio
                3: only video
                4: audio & video
                5: 3d & video
                6: 3d & audio
                7: 3d & audio & video
        :return: A integer representing the type of additional
        """
        has3d = False
        has_audio = False
        has_video = False
        if self.three_d_model_address is not None and self.three_d_model_address != "":
            has3d = True
        if self.audio_addresses.count() != 0:
            has_audio = True
        if self.video_address is not None and self.video_address != "":
            has_video = True

        if has3d and has_audio and has_video:
            return 7
        elif has3d and has_audio and not has_video:
            return 6
        elif has3d and not has_audio and has_video:
            return 5
        elif not has3d and has_audio and has_video:
            return 4
        elif not has3d and not has_audio and has_video:
            return 3
        elif not has3d and has_audio and not has_video:
            return 2
        elif has3d and not has_audio and not has_video:
            return 1
        else:
            return 0

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
            description = '(For TEST) A dramatically more powerful camera system. A display so responsive, every interaction feels new again. The world’s fastest smartphone chip. Exceptional durability. And a huge leap in battery life.'
            price = random.randint(2000, 999999)
            weight = round(10 * random.random(), 2)
            stock = random.randint(100, 500)
            serial_number = 'M' + str(i)
            user_id = [3, 4][random.randint(0, 1)]
            product_id = random.randint(1, 10)
            # create the object of this model type
            new_mt = ModelType(name=name, description=description, price=price, weight=weight, stock=stock,
                               serial_number=serial_number, user_id=user_id, product_id=product_id)
            db.session.add(new_mt)
            # add several pics for this model type
            for j in range(3):
                new_mt_pic = ModelTypePic(model_type=new_mt)
                db.session.add(new_mt_pic)
        db.session.commit()


class Customization(BaseModel):
    """
        This table records which customer has which customization of texture of which model type
    """
    __tablename__ = 'customizations'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model_type_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))
    texture_address = db.Column(db.String, nullable=False)


class Audio(BaseModel):
    __tablename__ = 'audios'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    model_type_id = db.Column(db.Integer, db.ForeignKey('model_types.id'))


'''
    This is a table for containing the 'n to n' following relationship of User model and Category model 
'''
UserCategory = db.Table('user_category',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                        db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
                        )


class Category(BaseModel):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     return Tools.delete_instance_state(super(Category, self).to_dict())

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


'''
    This is a table for containing the 'n to n' following relationship of User model and Brand model 
'''
UserBrand = db.Table('user_brand',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('brand_id', db.Integer, db.ForeignKey('brands.id'))
                     )


class Brand(BaseModel):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    logo = db.Column(db.String(256))    # the address of logo picture
    products = db.relationship('Product', backref='brand', lazy='dynamic')  # 1 brand --> n product

    def __repr__(self):
        return '<Brand %r>' % self.name

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     result = super(Brand, self).to_dict()
    #     # add relations to the result dict
    #     Tools.add_relation_to_dict(result, self.products.all(), "products")
    #     return Tools.delete_instance_state(result)

    @staticmethod
    def insert_brands():
        """
            This is a method for inserting the brands into the database.
            This should be used a single time in the terminal.
            This should be called before calling the Product.insert_products()
        """
        for brand_info in brand_list:
            name = brand_info[0]
            logo = brand_info[1]
            new_brand = Brand(name=name, logo=logo)
            db.session.add(new_brand)
        db.session.commit()


class BrowsingHistory(BaseModel):
    """
        A table records the browsing history of each user
        1 BH -> 1 user and 1 model type
        1 user and 1 model type -> 1 BH
    """
    __tablename__ = 'browsing_histories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    model_type_id = db.Column(db.Integer, db.ForeignKey('model_types.id'), nullable=False)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)  # the last visit time
    count = db.Column(db.Integer, default=1)  # How many time the user viewed this model type
    is_deleted = db.Column(db.Boolean, default=False)


class PremiumOrder(BaseModel):
    """
        The table records the payment orders of premium membership info.
        1 user (customer) -> n premiumOrder
        1 premium -> 1 user (customer)
    """
    __tablename__ = 'premium_orders'
    id = db.Column(db.Integer, primary_key=True)
    # 1 premium -> 1 user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)  # the unit is 'day': e.g. 7, 30, 365
    payment = db.Column(db.Float, nullable=False)  # only 2 digits in decimal e.g. 10.xx
    out_trade_no = db.Column(db.String(64),
                             unique=True)  # trade number, which should be unique inside a same retailer (us), includes numbers, letters and '_' only
    trade_no = db.Column(db.String(72), unique=True)  # this is generated by Alipay for each order after payment
    is_paid = db.Column(db.Boolean, default=False)  # whether the payment is finished

    def generate_unique_out_trade_no(self):
        """
        for generating the unique out_trade_no, which is required by Alipay.
        We add a random number and timestamp with order_id
        The field 'out_trade_no' will be filled.
        :return: out_trade_no
        """
        # get current datetime
        datetime_suffix = str(datetime.utcnow()).replace(" ", "").replace(":", "").replace('-', '').replace('.', '')
        # get a random int
        random_num_suffix = random.randint(0, 99999999999999999999)
        # form the out_trade_no ('P' refers to premium)
        out_trade_no = '{}_{}_{}_{}'.format('P', self.id, random_num_suffix, datetime_suffix)
        # the max length is 64
        if len(out_trade_no) > 64:
            out_trade_no = out_trade_no[0:64]

        # add the out_trade_no to this obj
        self.out_trade_no = out_trade_no
        db.session.add(self)
        db.session.commit()

        return out_trade_no


class Recipient(BaseModel):
    """
        The recipient information.
        1 address -> 1 recipient
        1 order (self-collection) -> 1 recipient OR 1 order (delivery) -> 1 address
    """
    __tablename__ = "recipients"
    id = db.Column(db.Integer, primary_key=True)
    recipient_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(24), nullable=False)
    # 1 recipient -> n address
    addresses = db.relationship('Address', backref='recipient', lazy='dynamic')
    # 1 recipient -> n orders
    orders = db.relationship('Order', backref='recipient', lazy='dynamic')

    @staticmethod
    def insert_recipients(count):
        fake = Faker()
        faker_for_phone = Faker("zh_CN")
        for i in range(count):
            new_recipient = Recipient(recipient_name=fake.name(), phone=faker_for_phone.phone_number())
            db.session.add(new_recipient)
        db.session.commit()

    def to_dict(self):
        """ Map the object to dictionary data structure """
        result = super(Recipient, self).to_dict()
        return Tools.delete_instance_state(result)


class Address(BaseModel):
    """
        The table records the address of delivery.
        1 address -> 1 user (customer)
        1 user (customer) -> n addresses
    """
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(128), nullable=False)
    province_or_state = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    district = db.Column(db.String(128), nullable=False)
    details = db.Column(db.String(128), nullable=False)
    is_default = db.Column(db.Boolean(), default=False)
    # 1 address -> 1 recipient
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipients.id'))
    # 1 address -> 1 user (customer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 1 address -> n orders
    # orders = db.relationship('Order', backref='address', lazy='dynamic')

    @staticmethod
    def insert_address():
        fake = Faker()

        for i in range(10):
            new_address = Address(customer_id=1, recipient_id=random.randint(1, Recipient.query.count()),
                                  country=fake.country(), province_or_state='Province{}'.format(i + 1),
                                  city=fake.city(), district='District{}'.format(i + 1),
                                  details="A test detailed address")
            db.session.add(new_address)

        # add a default address for this customer
        new_address = Address(is_default=True, customer_id=1, recipient_id=1,
                              country=fake.country(), province_or_state='Province{}'.format(11), city=fake.city(),
                              district='District{}'.format(11), details="pingleyuan 100 BJUT (fake address for test)")
        db.session.add(new_address)
        db.session.commit()

    def to_dict(self):
        """ Map the object to dictionary data structure """
        result = super(Address, self).to_dict()
        # add relations to the result dict
        # Tools.add_relation_to_dict(result, self.orders.all(), "orders")
        return Tools.delete_instance_state(result)

    def get_address(self):
        address = "{} - {} - {} - {} - {}".format(self.country, self.province_or_state, self.city, self.district,
                                                  self.details)
        return address


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


class Role(BaseModel):
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

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     result = super(Role, self).to_dict()
    #     # add relations to the result dict
    #     Tools.add_relation_to_dict(result, self.users.all(), "users")
    #     return Tools.delete_instance_state(result)

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


class User(UserMixin, BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    start_datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.String(256), default='upload/avatar/default-avatars/default__9__.jpg')  # The avatar
    background_pic = db.Column(db.String(256), default='upload/user-background/default__0__.png')  # The avatar
    theme = db.Column(db.String(16), default='light')  # the user preferred theme of our website
    language = db.Column(db.String(16), default='en')
    about_me = db.Column(db.Text(300))
    gender = db.Column(db.String(16), default='Unknown')  # 3 possible values: 'Male', 'Female', 'Unknown'
    exp = db.Column(db.Integer, default=0)  # the experience (level) of the user
    is_premium = db.Column(db.Boolean, default=False)
    premium_left_days = db.Column(db.Integer, default=0)  # the day left of the premium membership
    is_deleted = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 1 role --> n users

    # followed brands and categories
    followed_brands = db.relationship('Brand', secondary=UserBrand, backref=db.backref('user', lazy='dynamic'), lazy='dynamic')
    followed_categories = db.relationship('Category', secondary=UserCategory, backref=db.backref('user', lazy='dynamic'), lazy='dynamic')

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
    # 1 user (customer) -> n premiumsOrder
    premium_orders = db.relationship('PremiumOrder', backref='user', lazy='dynamic')
    # 1 user --> n B_histories
    browsing_histories = db.relationship('BrowsingHistory', backref='user', lazy='dynamic')
    # 1 staff --> n journals
    journals = db.relationship('Journal', backref='author', lazy='dynamic')
    # 1 customer -> n customization
    customizations = db.relationship('Customization', backref='user', lazy='dynamic')


    def __repr__(self):
        return '<User %r>' % self.username

    # def to_dict(self):
    #     """ Map the object to dictionary data structure """
    #     return Tools.delete_instance_state(super(User, self).to_dict())

    def get_default_address(self):
        """
        Get the default address of this user
        :return:
        """
        for ad in self.addresses:
            if ad.is_default:
                return ad
        return None

    def get_level(self):
        """
        calculate the user level by their exp (experiences)
        :return: A int number indicates the user level
        """
        return self.exp // 100

    @staticmethod
    def insert_users(count_customer: int, count_staff: int):
        """
        This is a method for inserting the testing user information
        This should be used in the console only a single time.
        """
        # insert customers first (customers must be the first)
        for i in range(count_customer):
            email = "Customer{}@163.com".format(i+1)
            username = "Customer{}".format(i+1)
            password = "12345678"
            role_id = 1
            # random avatar for customers
            default_avatars = [
                "upload/avatar/default-avatars/default__1__.jpg",
                "upload/avatar/default-avatars/default__2__.jpg",
                "upload/avatar/default-avatars/default__3__.jpg",
                "upload/avatar/default-avatars/default__4__.jpg",
                "upload/avatar/default-avatars/default__5__.jpg",
                "upload/avatar/default-avatars/default__6__.jpg",
                "upload/avatar/default-avatars/default__7__.jpg",
                "upload/avatar/default-avatars/default__8__.jpg",
                "upload/avatar/default-avatars/default__9__.jpg",
            ]
            avatar = default_avatars[random.randint(0, len(default_avatars)-1)]
            new_user = User(email=email, username=username, password=password, role_id=role_id, avatar=avatar)
            db.session.add(new_user)
        db.session.commit()

        # then insert staff users (staffs must be after the customers)
        for i in range(count_staff):
            email = "Staff{}@163.com".format(i + 1)
            username = "Staff{}".format(i + 1)
            password = "12345678"
            role_id = 2
            # same default avatar for all staffs
            avatar = "upload/avatar/default-avatars/default__0__.jpg"
            new_user = User(email=email, username=username, password=password, role_id=role_id, avatar=avatar)
            db.session.add(new_user)
        db.session.commit()

        # assign all customers users their initial chat room
        for cus in User.query.filter_by(role_id=1):
            # assign a random staff to this chat room
            staffs = User.query.filter_by(role_id=2).all()
            rand_staff = staffs[random.randint(0, len(staffs)-1)]
            # create chat room for this customer
            new_chatroom = ChatRoom(customer_id=cus.id, staff_id=rand_staff.id)
            db.session.add(new_chatroom)
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

    # def become_premium_member(self, duration: int):
    #     """
    #     Call this function to set this user as the premium member.
    #     :param duration: the duration of this new premium membership, unit is 'day'
    #     """
    #
    #     # mark the current premium record as expired
    #     # (if this is a renewal of membership, we still need to let only a single record be marked as not expired)
    #     p = self.get_current_premium()
    #     if p:
    #         p.expire()
    #
    #     # create a obj of new premium record
    #     new_premium = Premium(user_id=self.id, duration=duration)
    #
    #     # update the premium Columns in this table
    #     self.is_premium = True
    #     self.premium_left_days += new_premium.duration
    #     db.session.commit()

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
