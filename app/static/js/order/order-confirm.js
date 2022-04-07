$(document).ready(function (){

    //get the order id of current order
    let orderId = $(".address-list").attr("order-id")

    // set the default address as selected
    let defaultSign = $("#address-default-sign")
    let defaultAddressId = defaultSign.parent(".address").attr("address-id")
    defaultSign.parent(".address").addClass("chosen-address");
    update_order_address(orderId, defaultAddressId)

    //update the display of payment
    update_payment_info(orderId);

    /* when an address is clicked */
    $(".address").on("click", function(){
        // get address id of this address
        let addressId = $(this).attr("address-id");
        //send a ajax request to update the order info
        update_order_address(orderId, addressId);
    });

    /* when a shipping address is clicked */
    $(".shipping-method-list li").on("click", function(){
        //get the id of the selected method
        let methodId = $(this).attr("id")
        let shippingMethod = "delivery"
        if(methodId === "method-delivery"){
            shippingMethod = "delivery"
        }else if(methodId === "method-self"){
            shippingMethod = "self-collection"
        }

        //send an ajax request to update the shipping method
        update_order_shipping(orderId, shippingMethod)
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
            //update the display of payment
            $("#pay-subtotal").text(subTotal)
            $("#pay-total").text(payTotal)
            $("#pay-delivery").text(deliveryFee)
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
            //only let the selected one have the style of "chosen-class"
            $(".address").removeClass("chosen-address");
            let id = "#address-" + addressId
            $(id).addClass("chosen-address");
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
            //get the payment info from response
            let payTotal = response['payTotal']
            let deliveryFee = response['deliveryFee']
            let subTotal = payTotal - deliveryFee
            //update the display of payment
            $("#pay-subtotal").text(subTotal)
            $("#pay-total").text(payTotal)
            $("#pay-delivery").text(deliveryFee)

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
    });

}