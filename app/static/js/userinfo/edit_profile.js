$("#show_edit").on("click",function()
{window.alert("1111111111")
    let target = $("#profile_form");
    if(target.css("display")=='none')
    {
        window.alert("2222222222")
        target.css('display','');
        window.alert(target.css)
    }
});

$("#close_triger").on("click",function()
{
    let target = $("#profile_form");
    if(target.css("display")!='none')
    {
        target.css('display','none');
    }
});

$("#close_edit_profile_form_btn").on("click",function()
{
    let blocker = $("#profile_form_blocker");
    let show_edit_form = $("#edit_profile_form");
    if(blocker.css("display")!='none')
    {
        blocker.css('display','none');
        show_edit_form.css('display','none');
    }
});

function start_edit_profile(address_id)
{
    let recipient_name = $("#address_recipient_name_"+address_id)[0].innerText;
    let phone = $("#address_phone_"+address_id)[0].innerText;
    let place = $("#address_place_"+address_id)[0].innerText.split(" - ");
    let country = place[0];
    let province_or_state = place[1];
    let city = place[2];
    let district = place[3];

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
