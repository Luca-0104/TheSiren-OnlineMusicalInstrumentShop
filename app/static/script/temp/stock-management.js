/*
    functions that are using AJAX------------------------------------------------------------
*/

//remove a specific product, using ajax
function remove_product(product_id){
    $.post("/api/stock-management/remove-product", {
        "product_id": product_id

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //respond the removal in the frontend page
            // ...
        }

    });
}

//remove a specific model type, using ajax
function remove_model_type(model_type_id){
    $.post("/api/stock-management/remove-model-type", {
        "model_type_id": model_type_id

    }).done(function (response){
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //respond the removal in the frontend page
            // ...
        }

    });
}