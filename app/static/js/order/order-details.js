$(document).ready(function (){

});

// modify type
$("#modify-type-btn").on("click",function()
{
    let blocker = $("#order_detail_blocker");
    let modify_type_form = $("#modify_type_form");

    if(blocker.css("display")=='none')
    {
        blocker.css('display','');
        modify_type_form.css('display','');
    }
});

$("#close_modify_type_form_btn").on("click",function()
{
    let blocker = $("#order_detail_blocker");
    let modify_type_form = $("#modify_type_form");
    if(blocker.css("display")!='none')
    {
        blocker.css('display','none');
        modify_type_form.css('display','none');
    }
});

$("#select-type").change(function()
{
    let checkValue = $("#select-type").val();
    let address_field_row_1 = $("#address-field-row-1");
    let recipient_field_row_1 = $("#recipient-field-row-1");
    if(checkValue==='Delivery')
    {
        address_field_row_1.css('display','');
        recipient_field_row_1.css('display','none');
    }
    else if(checkValue==='Self-Collection')
    {
        recipient_field_row_1.css('display','');
        address_field_row_1.css('display','none');
    }
});

// modify address or recipiant
$("#modify-ar-btn").on("click",function()
{
    let blocker = $("#order_detail_blocker");
    let modify_ar_form = $("#modify_ar_form");
    if(blocker.css("display")=='none')
    {
        blocker.css('display','');
        modify_ar_form.css('display','');
    }
});

$("#close_modify_ar_form_btn").on("click",function()
{
    let blocker = $("#order_detail_blocker");
    let modify_ar_form = $("#modify_ar_form");
    if(blocker.css("display")!='none')
    {
        blocker.css('display','none');
        modify_ar_form.css('display','none');
    }
});

$(".address-1").on("click", function()
{
    let fieldId = 1;
    let orderId = $(this).parent().attr("order-id");
    let addressId = $(this).attr("address-id");
    console.log('clicked');
    $(".address-"+fieldId).removeClass("chosen-address");
    let id = "#address-" + fieldId + "-" + addressId;
    $(id).addClass("chosen-address");
    // update_order_address(1, orderId, addressId);
});

$(".address-2").on("click", function()
{
    console.log(".address-2 clicked");
    let fieldId = 2;
    let orderId = $(this).parent().attr("order-id");
    let addressId = $(this).attr("address-id");

    $(".address-"+fieldId).removeClass("chosen-address");
    let id = "#address-" + fieldId + "-" + addressId;
    $(id).addClass("chosen-address");

    $("#modify_ar_form").attr("addressId", addressId);
});

$("#update-ar-btn").on("click", function()
{
    console.log("#modify-ar-btn clicked");
    let current_type = $("#modify_ar_form").attr("current-type");
    let orderId = $("#modify_ar_form").attr("orderId");
    if(current_type==="delivery")
    {
        console.log("type delivery");
        let addressId = $("#modify_ar_form").attr("addressId");
        update_order_address(orderId, addressId);
    }
    else if(current_type==="self-collection")
    {
        console.log("type self-Collection");
        let recipient_field_2_name = $("#recipient-field-2-name").val();
        let recipient_field_2_phone = $("#recipient-field-2-phone").val();
        update_order_recipient(orderId, recipient_field_2_name, recipient_field_2_phone)
    }
});

function update_order_address(orderId, addressId)
{
    $.post("/api/update-order-address",
        {
            "order_id": orderId,
            "address_id": addressId
        }).done(function (response)
        {
            //get response from server
            let returnValue = response['returnValue'];
            console.log('recived');

            if (returnValue === 0)
            {
                console.log('successed');
                //success
                location.reload();
            }
        });
}

function update_order_recipient(orderId, recipientName, recipientPhone)
{
    $.post("/api/update-order-recipient",
        {
            "order_id": orderId,
            "recipient_name": recipientName,
            "recipient_phone": recipientPhone
        }).done(function (response)
        {
            //get response from server
            let returnValue = response['returnValue'];

            if (returnValue === 0)
            {
                console.log('successed');
                //success
                location.reload();
            }
        });
}