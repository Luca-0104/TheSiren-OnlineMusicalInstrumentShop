console.log("chat_page js read!!")

document.addEventListener('DOMContentLoaded', () => {
    // Make 'enter' key submit message
    console.log("chat_page listener added!!")

    /* add event listener for every message input blank */
    $(".user-message-input-blank").keypress(function (event) {

        console.log("key pressed!!")

        // when pressing the "Enter" key on the keyboard
        if (event.keyCode === 13) {

            console.log("The key is enter!")

            // prevent the original usage of "Enter" key
            event.preventDefault();
            //get the room id
            let roomId = $(this).attr("room-id");

            console.log("roomId: " + roomId);

            // simulate the "send" button clicking event
            $("#send-message-" + roomId).click();
        }
    });

});