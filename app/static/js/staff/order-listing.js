$(document).ready(function ()
{
    let addressId = $(".chosen-address").attr("address-id");
    $("#modify_type_form").attr("addressId", addressId);
    $("#modify_ar_form").attr("addressId", addressId);
});

// update priority //////////////////////////////////////////////////////////////////////////////////////////////////
$(".priority-select").change(function ()
{
    let orderId = $(this).attr("orderId");
    let checkValue = $(this).val();
    let priority_sort = $("#priority-sort-" + orderId);

    $(this).removeClass("btn-light");
    $(this).removeClass("btn-info");
    $(this).removeClass("btn-secondary");

    if (checkValue === 'Normal')
    {
        $(this).addClass("btn-light");
        priority_sort.html(1);
        update_priority(orderId, 1);
    }
    else if (checkValue === 'Important')
    {
        $(this).addClass("btn-info");
        priority_sort.html(2);
        update_priority(orderId, 2);
    }
    else if (checkValue === 'Significant')
    {
        $(this).addClass("btn-secondary");
        priority_sort.html(3);
        update_priority(orderId, 3);
    }
});

function update_priority(orderId, newPriority)
{
    $.post(
        "/api/order-management/update-priority",
        {
            "order_id": orderId,
            "new_priority": newPriority
        }).done(function (response)
    {
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0)
        {
            //success
            location.reload();
        }
    });
}

// change status //////////////////////////////////////////////////////////////////////////////////////////////////
function changeStatusTo(order_id, new_code)
{
    $.post(
        "/api/order/my-orders/change-status",
        {
            "new_code": new_code,
            "order_id": order_id
        }).done(function (response)
    {
        // get from server (backend)
        let returnValue = response['returnValue'];
        console.log(returnValue);

        if (returnValue === 0)
        {
            //success
            location.reload();
        }
    });
}

// modify type //////////////////////////////////////////////////////////////////////////////////////////////////
// $(".type-select").change(function ()
// {
//     console.log("here");
//     let orderId = $(this).attr("orderId");
//     let checkValue = $(this).val();
//     console.log(orderId);
//     console.log(checkValue);
//
//     let type_address_section = $("#type-address-section-" + orderId);
//     let type_name_section = $("#type-name-section-" + orderId);
//     let type_phone_section = $("#type-phone-section-" + orderId);
//
//     if (checkValue === 'Delivery')
//     {
//         type_address_section.css('display','');
//         type_name_section.css('display','none');
//         type_phone_section.css('display','none');
//     }
//     else if (checkValue === 'Self-Collection')
//     {
//         type_address_section.css('display','none');
//         type_name_section.css('display','');
//         type_phone_section.css('display','');
//     }
// });
$(".select-type-a").on("click", function ()
{
    console.log(".select-type-a clicked");
    let orderId = $(this).attr("orderId");
    let selectType = $(this).attr("selectType");
    console.log(orderId);
    console.log(selectType);

    // get element of the select's mask
    let select_type = $("#select-type-"+orderId);
    let select_type_display = $("#select-type-display-"+orderId);

    // get element of further action area
    let type_address_section = $("#type-address-section-" + orderId);
    let type_name_section = $("#type-name-section-" + orderId);
    let type_phone_section = $("#type-phone-section-" + orderId);

    if (selectType === 'Delivery')
    {
        // change select's mask
        select_type.val("Delivery");
        select_type_display.html("Delivery");
        $("#select-type-a-delivery-"+orderId).attr("aria-selected",true);
        $("#select-type-a-collection-"+orderId).attr("aria-selected",false);

        // set display of further action area
        type_address_section.css('display','');
        type_name_section.css('display','none');
        type_phone_section.css('display','none');
    }
    else if (selectType === 'Self-Collection')
    {
        // change select's mask
        select_type.val("Self-Collection");
        select_type_display.html("Self-Collection");
        $("#select-type-a-collection-"+orderId).attr("aria-selected",true);
        $("#select-type-a-delivery-"+orderId).attr("aria-selected",false);

        // set display of further action area
        type_address_section.css('display','none');
        type_name_section.css('display','');
        type_phone_section.css('display','');
    }
});

$(".address-1").on("click", function()
{
    let orderId = $(this).attr("orderId");
    let addressId = $(this).attr("address-id");
    let addresses_ul = $("#addresses-1-"+orderId);
    addresses_ul.attr("addressId", addressId);

    $(".address-1-"+orderId).removeClass("chosen-address");
    let id = "#address-1-" + orderId + "-" + addressId;
    $(id).addClass("chosen-address");
});

$(".type-btn").on("click", function()
{
    console.log(".type-btn clicked");
    let orderId = $(this).attr("orderId");
    let type_select = $("#select-type-"+orderId);
    let current_type = type_select.val();
    if(current_type==="Delivery")
    {
        console.log("type delivery");
        let addresses_ul = $("#addresses-1-"+orderId);
        let addressId = addresses_ul.attr("addressId");
        if(addressId == '' || addressId == undefined || addressId == null)
        {
            alert("You must choose one address.");
        }
        else
        {
            update_to_delivery(orderId, addressId);
        }
    }
    else if(current_type==="Self-Collection")
    {
        console.log("type self-Collection");
        let recipient_name = $("#recipient-name-1-"+orderId).val();
        let recipient_phone = $("#recipient-phone-1-"+orderId).val();
        if(recipient_name == '' || recipient_name == undefined || recipient_name == null)
        {
            alert("The recipient Name can not be empty.")
        }
        else if(recipient_phone == '' || recipient_phone == undefined || recipient_phone == null)
        {
            alert("The recipient Phone can not be empty.")
        }
        else
        {
            update_to_selfCollection(orderId, recipient_name, recipient_phone);
        }
    }
});

function update_to_delivery(orderId, addressId)
{
    console.log("update_to_delivery(orderId, addressId)");
    console.log(orderId);
    console.log(addressId);
    $.post("/api/cus-modify-order/change-order-to-delivery",
        {
            "order_id": orderId,
            "address_id": addressId
        }).done(function (response)
        {
            //get response from server
            let returnValue = response['returnValue'];
            console.log('recived');

            console.log(returnValue);

            if (returnValue === 0)
            {
                console.log('successed');
                //success
                location.reload();
            }
        });
}

function update_to_selfCollection(orderId, recipientName, recipientPhone)
{
    $.post("/api/cus-modify-order/change-order-to-collection",
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

// modify address //////////////////////////////////////////////////////////////////////////////////////////////////
$(".address-2").on("click", function()
{
    console.log("here");
    let orderId = $(this).attr("orderId");
    let addressId = $(this).attr("address-id");
    let addresses_ul = $("#addresses-2-"+orderId);
    addresses_ul.attr("addressId", addressId);

    $(".address-2-"+orderId).removeClass("chosen-address");
    let id = "#address-2-" + orderId + "-" + addressId;
    $(id).addClass("chosen-address");
    console.log("finished");
});

$(".address-btn").on("click", function()
{
    let orderId = $(this).attr("orderId");
    let addresses_ul = $("#addresses-2-"+orderId);
    let addressId = addresses_ul.attr("addressId");
    if(addressId == '' || addressId == undefined || addressId == null)
    {
        alert("You must choose one address.");
    }
    else
    {
        update_order_address(orderId, addressId);
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

// modify recipient //////////////////////////////////////////////////////////////////////////////////////////////////
$(".recipient-btn-2").on("click", function()
{
    let orderId = $(this).attr("orderId");
    let recipient_name = $("#recipient-name-2-"+orderId).val();
    let recipient_phone = $("#recipient-phone-2-"+orderId).val();
    update_order_recipient(orderId, recipient_name, recipient_phone);
});

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