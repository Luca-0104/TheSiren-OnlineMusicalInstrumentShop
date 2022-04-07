$("#show_add_form_btn").on("click",function()
{
    let blocker = $("#profile_form_blocker");
    let show_add_form = $("#add_address_form");
    if(blocker.css("display")=='none')
    {
        blocker.css('display','');
        show_add_form.css('display','');
    }
});

$("#close_add_form_btn").on("click",function()
{
    let blocker = $("#profile_form_blocker");
    let show_add_form = $("#add_address_form");
    if(blocker.css("display")!='none')
    {
        blocker.css('display','none');
        show_add_form.css('display','none');
    }
});

$("#close_edit_form_btn").on("click",function()
{
    let blocker = $("#profile_form_blocker");
    let show_add_form = $("#edit_address_form");
    if(blocker.css("display")!='none')
    {
        blocker.css('display','none');
        show_add_form.css('display','none');
    }
});

function remove_address(address_id)
{
    console.log("remove #address_row_"+address_id);
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
                else if(returnValue === 2)
                {
                    targetRow.remove();
                    let new_id = response['new_id'];
                    console.log("new id: " + new_id);
                    set_default(new_id);
                }
                else if(returnValue === 3)
                {
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

                    newHtml = "<td id=\"default_btn_" + previousID + "\" class=\"address_action_btn bg-grey\"><a class=\"set_default_btn\" data-toggle=\"tooltip\" data-placement=\"top\" title=\"\" data-original-title=\"View\""+
                       "href=\"javascript:set_default(" + previousID + ");\"><i class=\"ri-eye-line mr-0\">Set as Default</i></a></td>";
                    previousDefaultDiv.prepend(newHtml);
                    previousDefaultDiv.attr("is_default","f");

                    previousDefaultBar.remove();
                    targetBtn.remove();
                }
            });
}

function start_edit_address(address_id)
{
    let recipient_name = $("#address_recipient_name_"+address_id)[0].innerText;
    let phone = $("#address_phone_"+address_id)[0].innerText;
    let country = $("#address_place_"+address_id).attr("country");
    let province_or_state = $("#address_place_"+address_id).attr("pos");
    let city = $("#address_place_"+address_id).attr("city");
    let district = $("#address_place_"+address_id).attr("district");
    let details = $("#address_place_"+address_id).attr("details");

    let blocker = $("#profile_form_blocker");
    let show_add_form = $("#edit_address_form");
    if(blocker.css("display")=='none')
    {
        blocker.css('display','');
        show_add_form.css('display','');
    }

    // document.getElementById('address_form_hidden_id').value = address_id;
    // console.log("pre id"+address_form_hidden_id.val());
    // address_form_hidden_id.val(String(address_id));
    // console.log("post id"+document.getElementById('address_form_hidden_id').value);

    let address_form_address_id = $("#address_form_hidden_idasdf");
    address_form_address_id.val(address_id);

    let address_form_recipient_name = $("#address_form_recipient_name");
    address_form_recipient_name.val(recipient_name);

    let address_form_phone = $("#address_form_phone");
    address_form_phone.val(phone);

    let address_form_country = $("#address_form_country");
    address_form_country.val(country);

    let address_form_pos = $("#address_form_pos");
    address_form_pos.val(province_or_state);

    let address_form_city = $("#address_form_city");
    address_form_city.val(city);

    let address_form_district = $("#address_form_district");
    address_form_district.val(district);

    let address_form_details = $("#address_form_details");
    address_form_details.val(details);
}

function update_address()
{
    let address_form_hidden_id = $("#address_form_hidden_id").val();
    let address_form_recipient_name = $("#address_form_recipient_name").val();
    let address_form_phone = $("#address_form_phone").val();
    let address_form_country = $("#address_form_country").val();
    let address_form_pos = $("#address_form_pos").val();
    let address_form_city = $("#address_form_city").val();
    let address_form_district = $("#address_form_district").val();

    $.post("",
        {
            "id" : address_form_hidden_id,
            "recipient_name" : address_form_hidden_id,
            "phone" : address_form_hidden_id,
            "country" : address_form_hidden_id,
            "province_or_state" : address_form_hidden_id,
            "city" : address_form_hidden_id,
            "district" : address_form_hidden_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success

                }
            });
}
