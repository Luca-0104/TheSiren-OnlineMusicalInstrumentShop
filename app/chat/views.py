import datetime
import random
import time
import queue
# from time import strftime, localtime, time
from dateutil import tz
import pytz

from . import chat
from .. import db
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import current_user, login_required
from app import socketio
from flask_socketio import emit, send, join_room, leave_room

from ..decorators import staff_only, customer_only
from ..models import ChatRoom, Message, User
from engineio.payload import Payload

Payload.max_decode_packets = 9999

msg_queue = queue.Queue()


@chat.route('/chat_room', methods=['GET', 'POST'])
@login_required
def chat_room():
    if session.get('username') is not None:
        if session["role_id"] == 1:
            rooms = ChatRoom.query.filter_by(customer_id=session['uid']).all()

            # the staff in the chat room should be changed
            chat_data = Message.query.filter_by(chat_room_id=session['uid']).all()
            # print(chat_data)
            if len(chat_data) > 0:
                last_message = chat_data[-1]
                last_chat_time = last_message.timestamp
                current_time = datetime.datetime.now()

                # the staff and the user more than one day has not contacted
                if (current_time - last_chat_time).days > 1:
                    # find all staff
                    staffs = User.query.filter_by(role_id=2).all()
                    # pick up a staff randomly
                    staff_situation = random.randint(0, len(staffs) - 1)
                    # get the staff id
                    staff_id = staffs[staff_situation].id
                    # update staff_id
                    rooms[0].staff_id = staff_id
                    db.session.add(rooms[0])
                    db.session.commit()

            return redirect(url_for('chat.chat_for_customer', rooms=rooms))

            # current user is staff
        elif session["role_id"] == 2:
            rooms = ChatRoom.query.filter_by(staff_id=session['uid']).all()
            return render_template('chat/chat_staff.html', rooms=rooms)

    return render_template('main/index_new.html')


# this route is used by staff account
@chat.route('/chat_staff/<chat_room_id>', methods=['GET', 'POST'])
@login_required
@staff_only()
def chat_for_staff(chat_room_id):
    # gain the chat data
    messages = Message.query.filter_by(id=chat_room_id).order_by(Message.timestamp.asc()).all()
    print(len(messages))
    chat_room = ChatRoom.query.filter_by(id=chat_room_id).first()
    chat_partner_id = chat_room.customer_id
    chat_partner = User.query.filter_by(id=chat_partner_id).first()
    chat_partner_name = chat_partner.username
    return render_template("chat/chat_staff.html", username="staff", room=chat_room_id,
                           messages=messages, role_id=session['role_id'], chat_partner_name=chat_partner_name)


# this route id used by user account
@chat.route('/chat', methods=['GET', 'POST'])
@login_required
@customer_only()
def chat_for_customer():
    # gain the chat data
    print("create")
    messages = Message.query.filter_by(chat_room_id=session['uid']).order_by(Message.timestamp.asc()).all()
    return render_template("chat/chat_customer.html", username=session['username'], room=session['uid'],
                           messages=messages, role_id=session['role_id'])


@socketio.on('message')
def message(data):
    print('right?')
    print(data.get("time_stamp") is not None)
    if data.get("time_stamp") is not None:
        print('left?')
        send({'msg': data['msg'], 'username': data['username'],
              'time_stamp': data["time_stamp"], 'avatar': data['avatar']}
             , room=data['room'])
    else:
        send({'msg': data['msg'], 'username': data['username'],
              'time_stamp': time.strftime('%H:%M:%S', time.localtime()), 'avatar': data['avatar']}
             , room=data['room'])
        # print("message" + data['msg'])
        # check the identity of the current user
        if session["role_id"] == 1:
            author = 'customer'
        else:
            author = 'staff'
        # insert a new message into database
        new_message = Message(content=data['msg'], author_type=author, chat_room_id=data['room'])
        db.session.add(new_message)
        db.session.commit()
        # 2021-2-21 18:46:23


@socketio.on('join')
def join(data):
    join_room(data['room'])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    # send({'msg': data['username'] + " has left the " + data['room'] + "room."},
    #      room=data['room'])


# @chat.route('/api/history', methods=['POST'])
# def chat_history():
#     chat_room_id = request.form['chatroom_id']
#
#     past_messages = Message.query.filter_by(chat_room_id=chat_room_id).order_by(Message.id.asc()).all()
#     chat_history = []
#     for past_message in past_messages:
#         dic = prepare_for_history_json(past_message, chat_room_id)
#         chat_history.append(dic)
#
#     user = User.query.filter_by(id=current_user.id).first()
#     role_id = user.role_id
#     # role is customer
#     if role_id == 1:
#         role = 'customer'
#         print("customer")
#     if role_id == 2:
#         role = 'staff'
#
#     return jsonify({"history": chat_history,
#                     "current_user": role})


@socketio.on('history')
def history(data):
    chat_room_id = data['room']

    past_messages = Message.query.filter_by(chat_room_id=chat_room_id).order_by(Message.timestamp.asc()).all()
    chat_history = []
    for past_message in past_messages:
        dic = prepare_for_history_json(past_message, chat_room_id)
        chat_history.append(dic)

    for msg in chat_history:
        send({'msg': msg['msg'], 'username': msg['username'],
              'time_stamp': msg['time_stamp'], 'avatar': msg['avatar']}
             , room=chat_room_id)


def prepare_for_history_json(item, chat_id):
    print("nice")
    room = ChatRoom.query.filter_by(id=chat_id).first()
    username = room.customer.username
    staffname = room.staff.username
    # get local timezone
    utc_zone = tz.tzutc()
    local_zone = tz.tzlocal()
    local_dt = item.timestamp.replace(tzinfo=local_zone)
    utc_time = local_dt.astimezone(utc_zone)
    if item.author_type == 'customer':
        avatar = room.customer.avatar
        message = {'msg': item.content, 'username': username, 'time_stamp': utc_time.strftime('%H:%M:%S'),
                   'author_type': 'customer', 'avatar': avatar, 'message_id': item.id}

    if item.author_type == 'staff':
        avatar = room.staff.avatar
        message = {'msg': item.content, 'username': staffname, 'time_stamp': utc_time.strftime('%H:%M:%S'),
                   'author_type': 'staff', 'avatar': avatar, 'message_id': item.id}

    return message


# customize jinja filter
@chat.app_template_filter('times')
def handle_time(time):
    """
    1. in one minute show just now
    2. in one hour show minutes ago
    3. in one day show hours ago
    4. in 30 days show days ago
    5. else show the whole time
    :param time:
    :return:
    """

    now = datetime.datetime.now()
    timestamp = (now - time).total_seconds()  # show time stamp
    if timestamp < 60:
        return "just now"
    elif 60 <= timestamp < 60 * 60:
        minutes = timestamp / 60
        return "%sminutes ago" % minutes
    elif 60 * 60 <= timestamp < 60 * 60 * 24:
        hours = timestamp / (60 * 60)
        return "%shours ago" % int(hours)
    elif 60 * 60 * 24 <= timestamp < 60 * 60 * 24 * 30:
        days = timestamp / (60 * 60 * 24)
        return "%sdays ago" % int(days)
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")
