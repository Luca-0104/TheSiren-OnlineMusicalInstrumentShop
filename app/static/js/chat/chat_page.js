document.addEventListener('DOMContentLoaded', () => {
    // Make 'enter' key submit message


    /* add event listener for every message input blank */
    $(".user-message-input-blank").keypress(function (event) {

        // when pressing the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // prevent the original usage of "Enter" key
            event.preventDefault();
            //get the room id
            let roomId = $(this).attr("room-id");
            // simulate the "send" button clicking event
            $("#send-message-" + roomId).click();
        }

    });

});