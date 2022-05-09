

document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // let room = "Chat";
    // let room = "Chat";

    joinRoom(chatroom_id);

    // Display incoming message
    socket.on('message', data => {
        console.log(`Message received: ${data}`);

        //html elements declaration
        const p = document.createElement('p');

        const div_chat = document.createElement('div');
        const div_chat_user = document.createElement('div');
        const div_chat_message = document.createElement('div');

        const span_timestamp = document.createElement('span');
        const span_username = document.createElement('span');

        const img = document.createElement('img');

        //html elements attribute set and filling
        div_chat_user.setAttribute("class","direct-chat-info clearfix");
        img.setAttribute("class","direct-chat-img");
        div_chat_message.setAttribute("class","direct-chat-text");
        //set and filling end



         console.log("near if");
        if (data.username === username){
            console.log("inside if 1");

            div_chat.setAttribute("class","direct-chat-msg right");
            span_username.setAttribute("class", "direct-chat-name pull-right");
            span_timestamp.setAttribute("class","direct-chat-timestamp pull-left");
            img.setAttribute("src","https://img.icons8.com/color/36/000000/administrator-male.png");


        } else if (data.username !== username && typeof data.username !== 'undefined') {
            console.log("inside if 2");

            div_chat.setAttribute("class","direct-chat-msg");
            span_username.setAttribute("class","direct-chat-name pull-left");
            span_timestamp.setAttribute("class","direct-chat-timestamp pull-right");
            img.setAttribute("src","https://img.icons8.com/office/36/000000/person-female.png");
        } else {
            console.log("inside if 3");
            printSysMsg(data.msg)
        }

        span_timestamp.innerHTML = data.time_stamp;
        span_username.innerHTML = data.username;
        div_chat_message.innerHTML = data.msg;
        div_chat_user.innerHTML = span_username.outerHTML + span_timestamp.outerHTML;
        //message html generation
        div_chat.innerHTML = div_chat_user.outerHTML + img.outerHTML + div_chat_message.outerHTML;
         //generation end
        document.querySelector('#chat-window').append(div_chat);
    });

    // Send message
   $('#send_message').on("click", function(){
        if (document.querySelector('#user_message').value === ''){
            console.log('Cannot use empty message!');
        }
        else {
        console.log(document.querySelector('#user_message').value);
        socket.send({'msg': document.querySelector('#user_message').value,
        'username': username, 'room': chatroom_id, 'user': user });
        // Clear input area
        document.querySelector('#user_message').value = '';
        console.log(chatroom_id);
        console.log(username);
        }
    });


    // Leave room
    function leaveRoom(chatroom_id) {
        socket.emit('leave', {'username' : username, 'room' : chatroom_id});
    }

    // Join room
    // joinRoom(room, chat_id)    'room':room+chat_id
    function joinRoom(chatroom_id) {
        console.log("3333333333");
        console.log(chatroom_id);
        socket.emit('join', {'username': username, 'room': chatroom_id});
        // Clear message area
        document.querySelector('#chat-window').innerHTML = '';

        $.post('/api/history', {
            'chatroom_id': chatroom_id
        }).done(function (response) {
            let chat_history = response['history'];
            let current_user = response['current_user'];
            console.log("4444");
             for(let i = 0; i < chat_history.length; i++){
                 console.log(".....");
                 console.log(chat_history[i]);
                 socket.send({'msg': chat_history[i].msg,
                'username': chat_history[i].username, 'room': chatroom_id, 'time_stamp': chat_history[i].time_stamp, 'user': chat_history[i].user });

             }
        })

        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }

    //Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#chat-window').append(p);
    }
});