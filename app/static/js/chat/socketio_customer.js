document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

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
            console.log(chatroom_id);
            div_chat.setAttribute("class","direct-chat-msg right");
            span_username.setAttribute("class", "direct-chat-name pull-right");
            span_timestamp.setAttribute("class","direct-chat-timestamp pull-left");
            img.setAttribute("src", $('#chatroom-avatar-' + chatroom_id).attr('avatar-customer'));
        } else if (data.username !== username && typeof data.username !== 'undefined') {
            console.log("inside if 2");

            div_chat.setAttribute("class","direct-chat-msg");
            span_username.setAttribute("class","direct-chat-name pull-left");
            span_timestamp.setAttribute("class","direct-chat-timestamp pull-right");
            img.setAttribute("src", $('#chatroom-avatar-' + chatroom_id).attr('avatar-staff'));
        } else {
            console.log("inside if 3");
            printSysMsg(data.msg);
        }

        span_timestamp.innerHTML = data.time_stamp;
        span_username.innerHTML = data.username;
        div_chat_message.innerHTML = data.msg;
        div_chat_user.innerHTML = span_username.outerHTML + span_timestamp.outerHTML;
        //message html generation
        div_chat.innerHTML = div_chat_user.outerHTML + img.outerHTML + div_chat_message.outerHTML;
         //generation end
        console.log("before append!!")
        document.querySelector('#chat-window').append(div_chat);
    });

    socket.on('history', data => {
        console.log(`Message received: ${data}`);

        console.log("A history appended!!!")
        // check is that the last history
        if (data.isLast === '1'){
            // true
            // we put the system notification below this one
            // put notification of which staff is connected to you
            printConnMsg(staffName + " is connected to you");
            // determine whether need to send the automatic message
            if(entranceType === 'consult'){
                /* send 2 auto msg, a plaintext and a model_type info */
                // send plaintext
                socket.send({'msg': "Hi, I want to consult about the following instrument:", 'username': username, 'room': chatroom_id, 'avatar': avatar });
                // send model_type info
                socket.emit('auto-msg-consult', {'room' : chatroom_id, 'model_type_id': modelTypeId, 'username': username, 'avatar': avatar});

            }else if (entranceType === 'after-sale'){
                /* send 2 auto msg, a plaintext and a order info */
                // send plaintext
                socket.send({'msg': "Hi, I want to ask for the after-sale service, my order is shown below:", 'username': username, 'room': chatroom_id, 'avatar': avatar });
                // send order info
                socket.emit('auto-msg-after-sale', {'room' : chatroom_id, 'order_id': orderId, 'username': username, 'avatar': avatar});

            }
        }
        else
        {
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

            if (data.user_need_chat_history === username && data.type === "history"){
                if (data.username === username){
                console.log("inside if 1");
                console.log(chatroom_id);
                div_chat.setAttribute("class","direct-chat-msg right");
                span_username.setAttribute("class", "direct-chat-name pull-right");
                span_timestamp.setAttribute("class","direct-chat-timestamp pull-left");
                img.setAttribute("src", $('#chatroom-avatar-' + chatroom_id).attr('avatar-customer'));
            } else if (data.username !== username && typeof data.username !== 'undefined') {
                console.log("inside if 2");

                div_chat.setAttribute("class","direct-chat-msg");
                span_username.setAttribute("class","direct-chat-name pull-left");
                span_timestamp.setAttribute("class","direct-chat-timestamp pull-right");
                img.setAttribute("src", $('#chatroom-avatar-' + chatroom_id).attr('avatar-staff'));
            } else {
                console.log("inside if 3");
                printSysMsg(data.msg);
            }

            span_timestamp.innerHTML = data.time_stamp;
            span_username.innerHTML = data.username;
            div_chat_message.innerHTML = data.msg;
            div_chat_user.innerHTML = span_username.outerHTML + span_timestamp.outerHTML;
            //message html generation
            div_chat.innerHTML = div_chat_user.outerHTML + img.outerHTML + div_chat_message.outerHTML;
            //generation end
            document.querySelector('#chat-window').append(div_chat);
            }
        }
    });


    // put up the auto sent msg - consult
    socket.on('auto-msg-consult', data => {

    });

    // put up the auto sent msg - after-sale
    socket.on('auto-msg-after-sale', data => {

    });


    // Send message
   $('#send-message-' + chatroom_id).on("click", function(){
        if (document.querySelector('#user_message').value === ''){

        }
        else {
        console.log(document.querySelector('#user_message').value);
        socket.send({'msg': document.querySelector('#user_message').value,
        'username': username, 'room': chatroom_id, 'avatar': avatar });
        // Clear input area
        document.querySelector('#user_message').value = '';

        }
    });


    // Leave room
    function leaveRoom(chatroom_id) {
        socket.emit('leave', {'username' : username, 'room' : chatroom_id});
    }

    // Join room
    function joinRoom(chatroom_id) {
        socket.emit('join', {'username': username, 'room': chatroom_id});
        // Clear message area
        document.querySelector('#chat-window').innerHTML = '';

        socket.emit('history', {'room': chatroom_id});

        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }

    //Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#chat-window').append(p);
    }

    //Print "which staff is connected connected for you."
    function printConnMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#chat-window').append(p);
    }
});