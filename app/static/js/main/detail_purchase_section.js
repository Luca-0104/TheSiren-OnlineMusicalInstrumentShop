$(document).ready(function(){

    /* buy now */
    $("#btn-buy-now").on("click", function (){
        //get modelID and count
        let modelID = $("#btn-buy-now").attr("model_id");
        let count = $("#quantity-6194caf15498d8612861f033e8278855").val();
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

        if (returnValue === 0) {
            //success

        }

    });
}