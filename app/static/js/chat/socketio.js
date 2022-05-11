document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // let room = "Chat";
    // let room = "Chat";

    // Display incoming message
    socket.on('message', data => {
        console.log(`Message received: ${data}`);

        //html elements declaration
        const p = document.createElement('p');

        const div_chat = document.createElement('div');
        const div_chat_user = document.createElement('div');
        const div_username = document.createElement('div');
        const div_chat_detail = document.createElement('div');
        const div_chat_message = document.createElement('div');

        const span_timestamp = document.createElement('span');

        const a = document.createElement('a');
        const img = document.createElement('img');

        //html elements attribute set and filling
        div_chat_user.setAttribute("class","chat-user")
        div_username.setAttribute("class", "chat-sidebar-name");
        div_username.innerHTML = data.username;

        div_chat_detail.setAttribute("class","chat-detail");
        div_chat_message.setAttribute("class","chat-message");

        span_timestamp.setAttribute("class", "chat-time mt-1");
        span_timestamp.innerHTML = data.time_stamp;

        a.setAttribute("class","avatar m-0");

        img.setAttribute("class","avatar-35");
        img.setAttribute("alt","avatar");
        //set and filling end



         //generation end
         console.log("near if");
        if (data.username === username){
            console.log("inside if 1");
            div_chat.setAttribute("class","chat");
            img.setAttribute("src", $('#chatroom-avatar-'+chatroom_id).attr("avatar-staff"));

        } else if (data.username !== username && typeof data.username !== 'undefined') {
            console.log("inside if 2");
            img.setAttribute("src", $('#chatroom-avatar-'+chatroom_id).attr("avatar-customer"));
            div_chat.setAttribute("class","chat chat-left");

        } else {
            console.log("inside if 3");
            printSysMsg(data.msg)
        }
         //message html generation
          p.innerHTML=data.msg;
          a.innerHTML = img.outerHTML;
          div_chat_user.innerHTML = a.outerHTML + span_timestamp.outerHTML;

          //+ div_username.outerHTML ;

          div_chat_message.innerHTML = p.outerHTML;
          div_chat_detail.innerHTML = div_chat_message.outerHTML;

          div_chat.innerHTML = div_chat_user.outerHTML + div_chat_detail.outerHTML;
          document.querySelector('#chat-window').append(div_chat);

          $('#chat-window').scrollTop = $('#chat-window').scrollHeight;
    });

    // Send message
    $('#send_message').on("click", function(){
        if (document.querySelector('#user_message').value === ''){
        }
        else {
        console.log(document.querySelector('#user_message').value);
        socket.send({'msg': document.querySelector('#user_message').value,
        'username': username, 'room': chatroom_id, 'avatar': avatar });
        // Clear input area
        document.querySelector('#user_message').value = '';
        console.log(chatroom_id);
        console.log(username);
        }
    });

    // Room selection
    document.querySelectorAll('.listing-item').forEach(a => {
        a.onclick = () => {
            let newRoom = a.getAttribute('id');

            console.log(chatroom_id);
            if (newRoom == chatroom_id) {
                // msg = `You are already in ${room} room.`
                // printSysMsg(msg);
            } else {
                console.log("??");
                leaveRoom(chatroom_id);
                joinRoom(newRoom);
                chatroom_id = newRoom;
            }
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

        socket.emit('history', {'room': chatroom_id})

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