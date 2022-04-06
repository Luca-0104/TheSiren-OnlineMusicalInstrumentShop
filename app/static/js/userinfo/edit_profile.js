// $("#show_edit").on("click",function()
// {
//     let target = $("#profile_form");
//     if(target.css("display")=='none')
//     {
//
//         target.css('display','');
//
//     }
// });
//
// $("#close_triger").on("click",function()
// {
//     let target = $("#profile_form");
//     if(target.css("display")!='none')
//     {
//         target.css('display','none');
//     }
// });

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

$("#show_edit_info_form_btn").on("click",function()
{
    // let username = $("#username")[0].innerText;
    // let email = $("#email")[0].innerText;
    // let gender = $("#gender")[0].value();
    // let about = $("#about");


    // let province_or_state = place[1];
    // let city = place[2];
    // let district = place[3];

    let blocker = $("#profile_form_blocker");
    let show_add_form = $("#edit_profile_form");
    if(blocker.css("display")=='none')
    {
        blocker.css('display','');
        show_add_form.css('display','');
    }

    // document.getElementById('address_form_hidden_id').value = address_id;
    // console.log("pre id"+address_form_hidden_id.val());
    // address_form_hidden_id.val(String(address_id));
    // console.log("post id"+document.getElementById('address_form_hidden_id').value);

    // let address_form_address_id = $("#address_form_hidden_idasdf");
    // address_form_address_id.val(address_id);




    // let profile_form_username = $("#profile_form_username");
    // profile_form_username.val(username);
    //
    // let profile_form_email = $("#profile_form_email");
    // profile_form_email.val(email);
    //
    // let profile_form_gender = $("#profile_form_gender");
    // profile_form_gender.val(gender);
    //
    // let profile_form_about = $("#profile_form_about");
    // profile_form_about.val(about);




    // let address_form_city = $("#address_form_city");
    // address_form_city.val(city);
    //
    // let address_form_district = $("#address_form_district");
    // address_form_district.val(district);
});

// function update_address()
// {
//     let address_form_hidden_id = $("#address_form_hidden_id").val();
//     let address_form_recipient_name = $("#address_form_recipient_name").val();
//     let address_form_phone = $("#address_form_phone").val();
//     let address_form_country = $("#address_form_country").val();
//     let address_form_pos = $("#address_form_pos").val();
//     let address_form_city = $("#address_form_city").val();
//     let address_form_district = $("#address_form_district").val();
//
//     $.post("",
//         {
//             "id" : address_form_hidden_id,
//             "recipient_name" : address_form_hidden_id,
//             "phone" : address_form_hidden_id,
//             "country" : address_form_hidden_id,
//             "province_or_state" : address_form_hidden_id,
//             "city" : address_form_hidden_id,
//             "district" : address_form_hidden_id
//         }).done(function (response)
//             {
//                 // get from server (backend)
//                 let returnValue = response['returnValue'];
//
//                 if(returnValue === 0)
//                 {
//                     //success
//
//                 }
//             });
// }
