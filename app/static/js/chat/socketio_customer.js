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

        toBottom();
    });


    socket.on('history-customer', data => {
        console.log(" ------------------------ in customer history ------------------------------");

        // console.log(`Message received: ${data}`);

        // check whether all the histories are emitted finished (after finished)
        if (data.isLast === '1'){   // true

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


        // still emitting the history message
        } else {

            /*
                check the message type
            */

            // plaintext
            if (data.msgType === "normal"){

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


            // "consult" msg or "after-sale" msg
            }else if (data.msgType === 'consult'){

                let msgHTML = '<div class="direct-chat-msg right">'
                + '<div class="direct-chat-info clearfix">'
                + '<span class="direct-chat-name pull-right">' + data.username + '</span>'
                + '<span class="direct-chat-timestamp pull-left">' + data.time_stamp + '</span>'
                + '</div>'
                + '<img class="direct-chat-img" src="' + data.avatar_full_address + '" alt="avatar">'
                + '<div class="direct-chat-text">'
                + '<div role="listitem" class="w-dyn-item product-box" style="padding: 10">'
                + '<table class="commodity-table clickable" onclick="window.open(\'' + data.mt_url + '\')">'
                + '<tr>'
                + '<td colspan="4" class="title-cell">'
                + '<span class="order-title">Commodity</span>'
                + '</td>'
                + '</tr>'
                + '<tr>'
                + '<td class="empty-cell2" rowspan="2"></td>'
                + '<td class="commodity-image-cell">'
                + '<div class="img_container">'
                + '<img src="' + data.mt_pic + '" loading="lazy" alt="img">'
                + '</div>'
                + '</td>'
                + '<td class="commodity-info-cell">'
                + '<div class="box-product-info-card">'
                + 'Product price'
                + '<div class="my-price-container">'
                + '<span class="commodity-price">￥ ' + data.mt_price + '</span>'
                + '</div>'
                + '<br>'
                + 'Product name'
                + '<div class="my-product-name-container">'
                + '<span class="commodity-name">' + data.mt_name + '</span>'
                + '</div>'
                + '</div>'
                + '</td>'
                + '<td class="empty-cell2" rowspan="2"></td>'
                + '</tr>'
                + '<tr>'
                + '<td class="notify-cell" colspan="2">'
                + '<span class="click-notify">Click to View</span>'
                + '</td>'
                + '</tr>'
                + '</table>'
                + '</div>'
                + '</div>'
                + '</div>';

                // append to the chatting window
                $('#chat-window').append(msgHTML);



            }else if (data.msgType === 'after-sale'){
                let msgHTML = '<div class="direct-chat-msg right">'
                + '<div class="direct-chat-info clearfix">'
                + '<span class="direct-chat-name pull-right">' + data.username + '</span>'
                + '<span class="direct-chat-timestamp pull-left">' + data.time_stamp + '</span>'
                + '</div>'
                + '<img class="direct-chat-img" src="' + data.avatar_full_address + '" alt="avatar">'
                + '<div class="direct-chat-text">'
                + '<div role="listitem" class="w-dyn-item product-box" style="padding: 10">'
                + '<table class="order-table clickable" onclick="window.open(\'' + data.order_url + '\')">'
                + '<tr>'
                + '<td colspan="3" class="title-cell">'
                + '<span class="order-title">Order</span>'
                + '</td>'
                + '</tr>'
                + '<tr>'
                + '<td class="empty-cell2" rowspan="2"></td>'
                + '<td class="order-info-cell">'
                + '<div class="box-product-info-card">'
                + 'Trade ID'
                + '<div class="my-price-container">'
                + '<span class="order-id-cell">' + data.order_out_trade_no + '</span>'
                + '</div>'
                + '</div>'
                + '</td>'
                + '<td class="empty-cell2" rowspan="2"></td>'
                + '</tr>'
                + '<tr>'
                + '<td class="order-info-cell">'
                + '<span class="click-notify">Click to View</span>'
                + '</td>'
                + '</tr>'
                + '</table>'
                + '</div>'
                + '</div>'
                + '</div>';

                // append to the chatting window
                $('#chat-window').append(msgHTML);
            }

        }

        atBottom();
    });







    // put up the auto sent msg - consult
    socket.on('auto-msg-consult', data => {

        let msgHTML = '<div class="direct-chat-msg right">'
        + '<div class="direct-chat-info clearfix">'
        + '<span class="direct-chat-name pull-right">' + data.username + '</span>'
        + '<span class="direct-chat-timestamp pull-left">' + data.timestamp + '</span>'
        + '</div>'
        + '<img class="direct-chat-img" src="' + data.avatar + '" alt="avatar">'
        + '<div class="direct-chat-text">'
        + '<div role="listitem" class="w-dyn-item product-box" style="padding: 10">'
        + '<table class="commodity-table clickable" onclick="window.open(\'' + data.mt_url + '\')">'
        + '<tr>'
        + '<td colspan="4" class="title-cell">'
        + '<span class="order-title">Commodity</span>'
        + '</td>'
        + '</tr>'
        + '<tr>'
        + '<td class="empty-cell2" rowspan="2"></td>'
        + '<td class="commodity-image-cell">'
        + '<div class="img_container">'
        + '<img src="' + data.mt_pic + '" loading="lazy" alt="img">'
        + '</div>'
        + '</td>'
        + '<td class="commodity-info-cell">'
        + '<div class="box-product-info-card">'
        + 'Product price'
        + '<div class="my-price-container">'
        + '<span class="commodity-price">￥ ' + data.mt_price + '</span>'
        + '</div>'
        + '<br>'
        + 'Product name'
        + '<div class="my-product-name-container">'
        + '<span class="commodity-name">' + data.mt_name + '</span>'
        + '</div>'
        + '</div>'
        + '</td>'
        + '<td class="empty-cell2" rowspan="2"></td>'
        + '</tr>'
        + '<tr>'
        + '<td class="notify-cell" colspan="2">'
        + '<span class="click-notify">Click to View</span>'
        + '</td>'
        + '</tr>'
        + '</table>'
        + '</div>'
        + '</div>'
        + '</div>';

        // append to the chatting window
        $('#chat-window').append(msgHTML);

        toBottom();
    });

    // put up the auto sent msg - after-sale
    socket.on('auto-msg-after-sale', data => {
        let msgHTML = '<div class="direct-chat-msg right">'
        + '<div class="direct-chat-info clearfix">'
        + '<span class="direct-chat-name pull-right">' + data.username + '</span>'
        + '<span class="direct-chat-timestamp pull-left">' + data.timestamp + '</span>'
        + '</div>'
        + '<img class="direct-chat-img" src="' + data.avatar + '" alt="avatar">'
        + '<div class="direct-chat-text">'
        + '<div role="listitem" class="w-dyn-item product-box" style="padding: 10">'
        + '<table class="order-table clickable" onclick="window.open(\'' + data.order_url + '\')">'
        + '<tr>'
        + '<td colspan="3" class="title-cell">'
        + '<span class="order-title">Order</span>'
        + '</td>'
        + '</tr>'
        + '<tr>'
        + '<td class="empty-cell2" rowspan="2"></td>'
        + '<td class="order-info-cell">'
        + '<div class="box-product-info-card">'
        + 'Trade ID'
        + '<div class="my-price-container">'
        + '<span class="order-id-cell">' + data.order_out_trade_no + '</span>'
        + '</div>'
        + '</div>'
        + '</td>'
        + '<td class="empty-cell2" rowspan="2"></td>'
        + '</tr>'
        + '<tr>'
        + '<td class="order-info-cell">'
        + '<span class="click-notify">Click to View</span>'
        + '</td>'
        + '</tr>'
        + '</table>'
        + '</div>'
        + '</div>'
        + '</div>';

        // append to the chatting window
        $('#chat-window').append(msgHTML);

        toBottom();
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

        socket.emit('history-customer', {'room': chatroom_id});

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
        p.setAttribute("class", "connection-notifier");
        document.querySelector('#chat-window').append(p);
    }
});

function atBottom()
{
    let chat_window = $("#chat-window");
    let h = chat_window[0].scrollHeight * 1.5;
    chat_window.animate({scrollTop: h}, 0);
}

function toBottom()
{
    let chat_window = $("#chat-window");
    let h = chat_window[0].scrollHeight * 1.5;
    chat_window.animate({scrollTop: h}, 2000);
}