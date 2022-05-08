/*
    functions that are using AJAX------------------------------------------------------------
*/

//remove a specific product, using ajax
function remove_product(product_id)
{
    let targetName = "product-section-" + product_id;
    let target = document.getElementById(targetName);

    $.post("/api/stock-management/remove-product",
        {
            "product_id": product_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    console.log("Product " + product_id + "removed");
                    target.remove();
                }
            });
}

//remove a specific model type, using ajax
function remove_model_type(model_type_id, product_id)
{
    let targetName = "modeltype-section-" + model_type_id;
    let target = document.getElementById(targetName);

    console.log(target);

    console.log("remove model_type: " + targetName);
    $.post("/api/stock-management/remove-model-type",
        {
            "model_type_id": model_type_id
        }).done(function (response)
            {
                console.log('delete get replied')
                // get from server (backend)
                let returnValue = response['returnValue'];

                console.log(returnValue);

                if(returnValue === 0)
                {
                    //success
                    console.log("ModelType " + model_type_id + "removed");
                    target.remove();
                }
                else if(returnValue === 2)
                {
                    //success and there is no modeltype in is product
                    console.log("ModelType " + model_type_id + "removed");
                    remove_product(product_id);
                }
            });
}

$(".brands").template()

function search_by(type_id)
{
    let invisible_search_type = $("#invisible-search-type");
    let search_by = $("#search-by");
    $("#invisible-search-type").val(type_id);
    if(type_id == 1)
    {
        search_by.html("Model Name");
    }
    else if(type_id == 2)
    {
        search_by.html("Model Serial");
    }
}