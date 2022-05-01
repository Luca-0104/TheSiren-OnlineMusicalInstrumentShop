let sidebar_cart = $('#sidebar_cart');
let cart_errupter = $('#cart_errupter');
let side_bar_close = $('#close_cart');

$(document).ready(function (){
    sidebar_cart.on('click', function (){

        console.log(sidebar_cart.attr('open_'));
        if (sidebar_cart.attr('open_') === 'not'){
            cart_errupter.prop('style','opacity: 1; transition: opacity 300ms ease 0s;');
            sidebar_cart.attr('open_',"opened");
        }
    });

    side_bar_close.on('click',function (){
        cart_errupter.prop('style', 'display:none;');
        sidebar_cart.attr('open_','not');
    });

    /* Update the display of total payment */
    update_payment_display();

    /* When the remove btn is clicked */
    $(".cart-item-remove-btn").on("click", function (){
        //get the db id of this item
        let cartID = $(this).attr("cart-id");
        //send Ajax request to server to remove this cart relation
        remove_cart_relation(cartID);
    });

    /* When quantity is changed */
    $(".side-cart-quantity").on("change", function (){
        //get model id and new quantity
        let newCount = $(this).val()
        let modelID = $(this).attr('model-id');
        //This will also validate the count with stock
        update_item_count(modelID, newCount, $(this));
    });
});

/**
 * This function updates the display of the total payment
 */
function update_payment_display(){
    /* calculate the total payment of the items in this cart */
    let totalPayment = 0;
    $(".cart-item-price").each(function (){
        totalPayment +=  parseFloat($(this).html()) * parseFloat($(this).attr("item-count"));
    });
    //set the payment display
    $("#number-subtotal").text(totalPayment);
}

/*
    ------------------------------ functions using Ajax ------------------------------
 */

/**
 * This function sends Ajax request to server to remove the specific cart relation
 * @param cartID The db id of the cart relation that we wanna remove
 */
function remove_cart_relation(cartID){
    $.post("/api/cart/remove-cart-relation", {
        "cart_id": cartID

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) {    //success
            /* delete the displaying of this cart item */
            //concatenate the db id with prefix to get the HTML id of this cart item
            let id = "#cart-item-" + cartID
            $(id).remove();

            /* update the total payment */
            update_payment_display();
        }
    });
}


function update_item_count(modelID, newCount, quantityInput){
    $.post("/api/cart/update-cart-count", {
        "model_id": modelID,
        "new_count": newCount

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) {    //success

        }else if (returnValue === 2){  // exceed stock
            //notify the user
            let msg = response['msg'];
            window.alert(msg);

            //set the quantity back to one
            quantityInput.val(1);
            update_item_count(modelID, 1, quantityInput);

        }else if (returnValue === 3){   // this item run out of the stock
            //notify the user
            let msg = response['msg'];
            window.alert(msg);

            // refresh

        }
    });
}
