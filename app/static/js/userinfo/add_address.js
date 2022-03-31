$("#show_triger").on("click",function()
{
    let target = $("#address_form");
    if(target.css("display")=='none')
    {
        target.css('display','');
    }
});

$("#close_triger").on("click",function()
{
    let target = $("#address_form");
    if(target.css("display")!='none')
    {
        target.css('display','none');
    }
});

function remove_address(address_id)
{
    let targetRow = $("#address_row_"+address_id);

    $.post("/api/remove-address",
        {
            "address_id": address_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    target.remove();
                }
            });
}

function set_default(address_id)
{
    let targetRow = $("#address_row_"+address_id);
    let targetTable = $("address_table_"+address_id);

    let previousDefaultBar = $("#default_bar");

    $.post("/api/change-default-address",
        {
            "address_id": address_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    let newHtml = "<tr><td id=\"default_bar\" class=\"bg-primary\" colspan=\"2\">Default</td></tr>";
                    targetTable.prepend(newHtml);
                    previousDefaultBar.remove();
                }
            });
}
