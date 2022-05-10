$(document).ready(function (){

    //get the order id of current order
    let orderId = $(".address-list").attr("order-id")

    //shipping method of this order, default value is "delivery"
    let shippingMethod = "delivery"
    update_order_shipping(orderId, shippingMethod);

    // set the default address as selected
    let defaultSign = $("#address-default-sign")
    let defaultAddressId = defaultSign.parent().parent().attr("address-id")
    defaultSign.parent(".address").addClass("chosen-address");
    update_order_address(orderId, defaultAddressId)

    //update the display of payment
    update_payment_info(orderId);

    //update all the address sequence number
    $(".address-number").each(function (){
        let addressNumber = 1 + $(this).parent().parent().parent().index();
        $(this).text(addressNumber);
    });

    /* when an address is clicked */
    $(".address").on("click", function(){
        // get address id of this address
        let addressId = $(this).attr("address-id");
        //send a ajax request to update the order info
        update_order_address(orderId, addressId);
    });

    /* when a shipping method is clicked */
    $(".shipping-method-list .shipping-method").on("click", function(){
        //get the id of the selected method
        let methodId = $(this).attr("id")

        if(methodId === "method-delivery"){
            shippingMethod = "delivery"
        }else if(methodId === "method-self"){
            shippingMethod = "self-collection"
        }

        //send an ajax request to update the shipping method
        update_order_shipping(orderId, shippingMethod)
    });

    /* When the "place order" btn is clicked */
    $("#btn-place-order").on("click", function (){
        //get the shipping method, if it is "self-collecting", we will ensure the recipient info are not None
        if(shippingMethod === "self-collection"){
            //get the recipient name and phone
            let recipientName = $("#recipient-name").val().trim();
            let recipientPhone = $("#recipient-phone").val().trim();
            // check the recipient info
            if(recipientName === "" || recipientPhone === ""){
                window.alert("If you choose self-collecting, the recipient info should not be empty!")
            }else if(recipientName.length > 64){
                window.alert("The recipient name should not longer than 64 characters!")
            }else if(recipientPhone.length > 24){
                window.alert("The recipient phone number should not longer than 24 characters!")
            }else{
                //send Ajax request for updating the order and paying
                update_order_recipient(orderId, recipientName, recipientPhone);
            }

        }else if (shippingMethod === "delivery"){
            //check if there is any address selected
            if ($(".chosen-address").length === 0){
                // notify the user
                window.alert("You should define an address for this delivery order!");
            }else{
                //send Ajax request for paying directly
                pay_for_order(orderId)
            }
        }
    });

    /* When delete address is clicked */
    $(".btn-address-delete").on("click", function(){
        //count how many addresses left
        let addressCount = $(".address-list").children("li").length;
        //if this is the last one, we won't let user to delete it
        if(addressCount <= 1){
            window.alert("You cannot delete the last address");
        }else{
            //if this is not the last one, we will send Ajax request to delete it
            //get the address id
            let addressID = $(this).parent().parent().attr("address-id");
            console.log("address id: " + addressID);
            //send Ajax request
            delete_address(orderId, addressID);
        }
    });

});

/*
    ---------------------------- using Ajax ------------------------------
*/
/**
 * get the payment info from backend to update the frontend displaying
 * @param orderId
 */
function update_payment_info(orderId){
    $.post("/api/get-order-payment", {
        "order_id": orderId,

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //get the payment info from response
            let payTotal = response['payTotal']
            let deliveryFee = response['deliveryFee']
            let subTotal = payTotal - deliveryFee
            let shouldPay = response['paidPayment']
            console.log("should: " + shouldPay)
            //update the display of payment
            $("#pay-subtotal").text(subTotal)
            $("#pay-total").text(payTotal)
            $("#pay-delivery").text(deliveryFee)
            $("#pay-should").text(shouldPay)
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}

/**
 * Change the address of the given order into the given address
 * @param orderId
 * @param addressId
 */
function update_order_address(orderId, addressId){

    $.post("/api/update-order-address", {
        "order_id": orderId,
        "address_id": addressId

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            console.log("address updated!")
            //only let the selected one have the style of "chosen-class"
            $(".address").removeClass("chosen-address");
            let id = "#address-" + addressId
            $(id).addClass("chosen-address");
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}

/**
 * THis function update the shipping method of the given order
 */
function update_order_shipping(orderId, shippingMethod){

    $.post("/api/update-order-shipping", {
        "order_id": orderId,
        "shipping_method": shippingMethod

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //update payment info display
            update_payment_info(orderId);

            //only let the selected one have the style of "chosen-shipping-method"
            $(".shipping-method-list li").removeClass("chosen-shipping-method");

            if(shippingMethod === "delivery"){
                $("#method-delivery").addClass("chosen-shipping-method");
                //show the address section
                $("#address-section").removeClass("hidden-field");
                //hide the recipient section
                $("#recipient-section").addClass("hidden-field");

            }else if(shippingMethod === "self-collection"){
                $("#method-self").addClass("chosen-shipping-method");
                //hide the address section
                $("#address-section").addClass("hidden-field");
                //show the recipient section
                $("#recipient-section").removeClass("hidden-field");
            }
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}

/**
 * THis function updates the recipient info of the given order
 * @param orderId
 * @param recipientName
 * @param recipientPhone
 */
function update_order_recipient(orderId, recipientName, recipientPhone){
    $.post("/api/update-order-recipient", {
        "order_id": orderId,
        "recipient_name": recipientName,
        "recipient_phone": recipientPhone

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //if success, we can send another Ajax for paying
            pay_for_order(orderId);
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}

/**
 * This function sends Ajax request to call Alipay for paying the order
 * @param orderId
 */
function pay_for_order(orderId){
    $.post("/api/pay-for-order/instrument", {
        "order_id": orderId,

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            // get payment URL then redirect to that URL
            let paymentURL = response['paymentURL']
            location.href = paymentURL;
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}

/**
 * This function sends Ajax request to delete the given address
 * @param orderID The id of this order
 * @param addressId The id of the address needs to be deleted
 */
function delete_address(orderID, addressId){
    $.post("/api/remove-address", {
        "address_id": addressId

    }).done(function(response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0 || returnValue === 3 || returnValue === 2) { //success
            // refresh this page
            let url = "/order-confirm/" + orderID;
            location.href = url;
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}