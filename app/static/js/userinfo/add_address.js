$("#show_add_form_btn").on("click",function()
{
    console.log("try to show");
    let blocker = $("#address_form_blocker");
    let show_add_form = $("#address_form");
    if(blocker.css("display")=='none')
    {
        console.log("change css to show");
        blocker.css('display','');
        show_add_form.css('display','');
    }
});

$("#close_add_form_btn").on("click",function()
{
    let blocker = $("#address_form_blocker");
    let show_add_form = $("#address_form");
    if(blocker.css("display")!='none')
    {
        blocker.css('display','none');
        show_add_form.css('display','none');
    }
});

function remove_address(address_id)
{
    console.log("#address_row_"+address_id);
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
                    targetRow.remove();
                }
            });
}

function set_default(address_id)
{
    let targetRow = $("#address_row_"+address_id);
    let targetTable = $("#address_table_"+address_id);
    let targetDiv = $("#action_"+address_id);
    let targetBtn = $("#default_btn_"+address_id);

    let previousDefaultBar = $("#default_bar");
    let previousID = previousDefaultBar.attr("address_id");
    let previousDefaultDiv = $('[is_default=t]');

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
                    let newHtml = "<tr><td id=\"default_bar\" address_id=\"" + address_id + "\" class=\"bg-primary\" colspan=\"2\">Default</td></tr>";
                    targetTable.prepend(newHtml);
                    targetDiv.attr("is_default","t");

                    newHtml = "<a id=\"default_btn_" + previousID + "\" class=\"badge badge-info mr-2\" data-toggle=\"tooltip\" data-placement=\"top\" title=\"\" data-original-title=\"View\""+
                       "href=\"javascript:set_default(" + previousID + ");\"><i class=\"ri-eye-line mr-0\">Set as Default</i></a>";
                    previousDefaultDiv.prepend(newHtml);
                    previousDefaultDiv.attr("is_default","f");

                    previousDefaultBar.remove();
                    targetBtn.remove();
                }
            });
}
