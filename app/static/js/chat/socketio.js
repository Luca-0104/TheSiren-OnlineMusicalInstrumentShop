document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // let room = "Chat";
    // let room = "Chat";
    
    // Set the id of this chat room as an global variable in this js file
    let chatRoomId = 0;

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
          document.querySelector('#chat-window-' + chatRoomId).append(div_chat);

          $('#chat-window-' + chatRoomId).scrollTop = $('#chat-window-' + chatRoomId).scrollHeight;
    });

    socket.on('history', data => {
        // console.log(`Message received: ${data}`);

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
         if (data.user_need_chat_history === username && data.type === "history"){
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
          document.querySelector('#chat-window-' + chatRoomId).append(div_chat);

          $('#chat-window-' + chatRoomId).scrollTop = $('#chat-window-' + chatRoomId).scrollHeight;
         }

    });


    // put up the auto sent msg - consult
    socket.on('auto-msg-consult', data => {

        console.log("here in consult append!!");

        let msgHTML = '<div class="chat chat-left">'
        + '<div class="chat-user">'
        + '<a class="avatar m-0">'
        + '<img src="' + data.avatar + '" alt="avatar" class="avatar-35 ">'
        + '</a>'
        + '<span class="chat-time mt-1">' + data.timestamp + '</span>'
        + '</div>'
        + '<div class="chat-detail">'
        + '<div class="chat-message">'
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
        $('#chat-window-' + chatRoomId).append(msgHTML);

    });

    // put up the auto sent msg - after-sale
    socket.on('auto-msg-after-sale', data => {

        console.log("here in after-sale append!!");

        let msgHTML = '<div class="chat chat-left">'
        + '<div class="chat-user">'
        + '<a class="avatar m-0">'
        + '<img src="' + data.avatar + '" alt="avatar" class="avatar-35 ">'
        + '</a>'
        + '<span class="chat-time mt-1">' + data.timestamp + '</span>'
        + '</div>'
        + '<div class="chat-detail">'
        + '<div class="chat-message">'
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
        + '<span class="commodity-price">' + data.order_out_trade_no + '</span>'
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
        $('#chat-window-' + chatRoomId).append(msgHTML);

    });



    // Send message
    $('.btn-send-message').on("click", function(){
        let roomId = $(this).attr("room-id");
        if (document.querySelector('#user-message-' + roomId).value === ''){
        }
        else {
        console.log(document.querySelector('#user-message-' + roomId).value);
        socket.send({'msg': document.querySelector('#user-message-' + roomId).value,
        'username': username, 'room': chatroom_id, 'avatar': avatar, 'type': 'new' });
        // Clear input area
        document.querySelector('#user-message-' + roomId).value = '';
        console.log(chatroom_id);
        console.log(username);
        }
    });

    // Room selection
    // document.querySelectorAll('.listing-item').forEach(a => {
    //     a.onclick = () => {
    //         let newRoom = a.getAttribute('id');
    //
    //         // determine whether the current staff is belong to this clicked room
    //         let roomStaffId = a.attr("room-staff-id");
    //         let currentStaffId = a.attr("current-staff-id");
    //         console.log("roomStaffId: " + roomStaffId);
    //         console.log("currentStaffId: " + currentStaffId);
    //
    //         console.log(chatroom_id);
    //         if (newRoom === chatroom_id) {
    //             // msg = `You are already in ${room} room.`
    //             // printSysMsg(msg);
    //         } else {
    //             console.log("??");
    //
    //             if (chatroom_id !== undefined){
    //                 leaveRoom(chatroom_id);
    //             }
    //
    //             joinRoom(newRoom);
    //             chatroom_id = newRoom;
    //         }
    //     }
    // });

    /* Room selection */
    $(".listing-item").on('click', function (){

        // the id of the selected room
        let newRoomId = $(this).attr("id");

        // determine whether the current staff is belong to this clicked room
        let roomStaffId = $(this).attr("room-staff-id");
        let currentStaffId = $(this).attr("current-staff-id");
        if (roomStaffId !== currentStaffId){
            // get the aborting request url
            let redirectURL = $(this).attr("redirect-URL");
            window.location.href = redirectURL;
        }

        // determine whether the selected room is already shown on the right side
        if (newRoomId === chatroom_id) {
            // msg = `You are already in ${room} room.`
            // printSysMsg(msg);
        } else {

            if (chatroom_id !== undefined){
                leaveRoom(chatroom_id);
            }

            joinRoom(newRoomId);
            chatroom_id = newRoomId;
        }
    });

    // Leave room
    function leaveRoom(chatroom_id) {
        socket.emit('leave', {'username' : username, 'room' : chatroom_id});
        $('#chat-window-' + chatRoomId).html('');
    }

    // Join room
    // joinRoom(room, chat_id)    'room':room+chat_id
    function joinRoom(chatroom_id) {
        // update that global chat room id of current room
        chatRoomId = chatroom_id;
        console.log("3333333333");
        console.log(chatroom_id);
        socket.emit('join', {'username': username, 'room': chatroom_id});
        // Clear message area
        document.querySelector('#chat-window-' + chatRoomId).innerHTML = '';

        socket.emit('history', {'room': chatroom_id})

        // Autofocus on text box
        document.querySelector('#user-message-' + chatroom_id).focus();
    }

    //Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#chat-window-' + chatRoomId).append(p);
    }
});