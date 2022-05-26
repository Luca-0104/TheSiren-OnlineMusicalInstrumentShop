$(document).ready(function ()
{
    let chat_entrance_anchor = $("#chat-entrance-anchor");
    if(chat_entrance_anchor.length == 1)
    {
        let entrance_type = chat_entrance_anchor.attr("entrance-type");
        console.log("entrance_type: " + entrance_type)
        let entrance = $("#sticky-chat-btn");
        entrance.get(0).onclick="";
        if(entrance_type === "commodity")
        {
            let model_id = chat_entrance_anchor.attr("model-id");
            entrance.on('click', function()
            {
               window.open('/chat-consult/'+model_id);
            });
        }
    }
});