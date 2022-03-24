document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // let room = "Chat";
    // let room = "Chat";
    joinRoom(room);


    // Display incoming message
    socket.on('message', data => {
        // console.log(`Message received: ${data}`);
        const p = document.createElement('p');
        const span_username = document.createElement('span')
        const span_timestamp = document.createElement('span')
        const br = document.createElement('br');

        if (data.username == username){
            p.setAttribute("class", "my-msg");

            span_username.setAttribute("class", "my-username");
            span_username.innerHTML = data.username;

            span_timestamp.setAttribute("class", "timestamp");
            span_timestamp.innerHTML = data.time_stamp;

            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML
            + span_timestamp.outerHTML;
            // p.innerHTML = data;
            document.querySelector('#display-message-section').append(p);
        } else if (data.username != username && typeof data.username !== 'undefined') {
            p.setAttribute("class", "others-msg");

            span_username.setAttribute("class", "other-username");
            span_username.innerHTML = data.username;

            span_timestamp.setAttribute("class", "timestamp");
            span_timestamp.innerHTML = data.time_stamp;

            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML
            + span_timestamp.outerHTML;
            // p.innerHTML = data;
            document.querySelector('#display-message-section').append(p);
        } else {
            printSysMsg(data.msg)
        }


    });

    // Send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
        'username': username, 'room': room });
        // Clear input area
        document.querySelector('#user_message').value = '';
    }

    // Room selection
    // document.querySelectorAll('.select-room').forEach(p => {
    //     p.onclick = () => {
    //         let newRoom = p.innerHTML;
    //         if (newRoom == room) {
    //             msg = `You are already in ${room} room.`
    //             printSysMsg(msg);
    //         } else {
    //             leaveRoom(room);
    //             joinRoom(newRoom);
    //             room = newRoom;
    //         }
    //     }
    // });

    // Leave room
    function leaveRoom(room) {
        socket.emit('leave', {'username' : username, 'room' : room});
    }

    // Join room
    // joinRoom(room, chat_id)    'room':room+chat_id
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
        // Clear message area
        // document.querySelector('#display-message-section').innerHTML = ''
        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }

    //Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
});