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
                    let newIndex = 1;
                    $(".index_section").each(function()
                    {
                        $(this).text(newIndex);
                        newIndex = newIndex + 1;
                    });
                }
                else if(returnValue === 2)
                {
                    targetRow.remove();
                    let newIndex = 1;
                    $(".index_section").each(function()
                    {
                        $(this).text(newIndex);
                        newIndex = newIndex + 1;
                    });
                    let new_id = response['new_id'];
                    set_default(new_id);
                }
                else if(returnValue === 3)
                {
                    targetRow.remove();
                }
                else if (returnValue === 318)
                {
                    let targetURL = response['redirectURL'];
                    window.location.href = targetURL;
                }
            });
}

function set_default(address_id)
{
    let newDefaultRow = $("#default_bar_"+address_id)
    let newDefaulta = $("#default_a_"+address_id);

    let previousDefaultRow = $(".default_one");
    let previousID = previousDefaultRow.attr("address_id");
    let previousDefaulta = $('#default_a_'+previousID);

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
                    //set previous default as normal
                    previousDefaultRow.removeClass("bg-primary");
                    previousDefaultRow.removeClass("default_one");
                    previousDefaultRow.addClass("not_default");
                    previousDefaulta.removeClass("unclickable");
                    previousDefaulta.addClass("set_default_btn");
                    previousDefaulta.attr("href", "javascript:set_default(" + previousID + ");");
                    previousDefaulta.text('Set as Default');

                    //set new default
                    newDefaultRow.removeClass("not_default");
                    newDefaultRow.addClass("bg-primary");
                    newDefaultRow.addClass("default_one");
                    newDefaulta.removeClass("set_default_btn");
                    newDefaulta.addClass("unclickable");
                    newDefaulta.attr("href", "");
                    newDefaulta.text('Default');
                }
                else if (returnValue === 318)
                {
                    let targetURL = response['redirectURL'];
                    window.location.href = targetURL;
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
                else if (returnValue === 318)
                {
                    let targetURL = response['redirectURL'];
                    window.location.href = targetURL;
                }
            });
}
