$(document).ready(function(){

    $("#btn-buy-now").on("click", function (){
        //get modelID and count
        let modelID = $("#btn-buy-now").attr("model_id");
        let count = $("#quantity-6194caf15498d8612861f033e8278855").val();
        //send Ajax request
        buy_now(modelID, count);
    });

});

/*
* ------------------ functions Using Ajax
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