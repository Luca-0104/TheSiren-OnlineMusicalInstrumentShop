$(document).ready(function(){

    // the input blank of quantity
    let quantity = $("#quantity-6194caf15498d8612861f033e8278855");
    // get model id
    let modelID = $("#btn-buy-now").attr("model_id");

    /* buy now */
    $("#btn-buy-now").on("click", function (){
        //get count
        let count = $("#quantity-6194caf15498d8612861f033e8278855").val();
        console.log("count: " + count);
        //send Ajax request
        buy_now(modelID, count);
    });

    /* add to cart */
    $("#btn-add-to-cart").on("click", function (){
       //get modelID and count
        let modelID = $("#btn-buy-now").attr("model_id");
        let count = $("#quantity-6194caf15498d8612861f033e8278855").val();
        //send Ajax request
        add_to_cart(modelID, count);
    });

    /* when changing the quantity */
    quantity.on("change", function (){
        let count = $(this).val();
        //count number should not be empty
        if (count === ""){
            $(this).val(1);
        }
        //send ajax to compare the count with stock
        check_stock(modelID, count);
    });

});

/*
* ------------------ functions Using Ajax ---------------------
*/
function buy_now(modelID, count){

    $.post("/generate-order-from-buy-now", {
        "model_id": modelID,
        "count": count

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) {
            //success
            let order_id = response['order_id'];
            window.location.href = "/order-confirm/" + order_id;

        }else if (returnValue === 2){
            // returnValue=2 means the user does not login
            // we redirect them to the login page
            window.location.href = "/login"

        }else if (returnValue === 3){
            // returnValue=3 means out of stock
            //we can refresh this page, the "out of stock" statement would be shown
            let url = "/product-details/" + modelID;
            location.href = url;
        }

    });
}

function add_to_cart(modelID, count){
    $.post("/api/cart/add-to-cart", {
        "model_id": modelID,
        "count": count

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            /* update the display in the sidebar cart */
            //get the cardID from server response
            let cartID = response['cartID'];

            //concatenate the db id with prefix to get the HTML id of this cart item
            let id = "#cart-item-" + cartID

            //update the count
            $(id + " input").attr("value", parseInt($(id + " input").attr("value")) + parseInt(count));

            //open the sidebar cart
            // let sidebar_cart = $('#sidebar_cart');
            // let cart_errupter = $('#cart_errupter');
            // let side_bar_close = $('#close_cart');
            // if (sidebar_cart.attr('open_') === 'not'){
            //     cart_errupter.prop('style','opacity: 1; transition: opacity 300ms ease 0s;');
            //     sidebar_cart.attr('open_',"opened");
            // }
        }
    });
}

function check_stock(modelID, count){
    $.post("/api/model-detail/validate-model-count", {
        "model_id": modelID,
        "new_count": count

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) {
            //success

        }else if (returnValue === 3){
            //the count exceeds the stock
            window.alert("Quantity exceeds the stock!")
            $("#quantity-6194caf15498d8612861f033e8278855").val(1);

        }else if (returnValue === 4){
            //the stock becomes 0
            //we can refresh this page, the "out of stock" statement would be shown
            let url = "/product-details/" + modelID;
            location.href = url;
        }

    });
}