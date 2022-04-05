console.log("cart.js activate");
refreshCart();

function refreshCart()
{
    calculateEachPrice();
    calculateTotalCost();
}

function calculatePrice(rowID)
{
    let singlePriceStr = $("#row_"+rowID).attr("single_price");
    let singlePrice = parseFloat(singlePriceStr);

    let quantityStr = $("#quantity_"+rowID).val();
    let quantity = parseInt(quantityStr);

    let price = (singlePrice * quantity).toFixed(2);

    let spanPrice = $("#price_"+rowID);
    spanPrice.html(price);
}

function calculateEachPrice()
{
    let totalRow = $("#cart_table").attr("total_row");
    for(let i=1; i<=totalRow; i++)
    {
        calculatePrice(i);
    }
}

function calculateTotalCost()
{
    let totalRow = $("#cart_table").attr("total_row");
    let totalCost = 0;
    for(let i=1; i<=totalRow; i++)
    {
        if($("#select_"+i).prop('checked'))
        {
            let priceStr = $("#price_"+i).html();
            let price = parseFloat(priceStr);
            totalCost = totalCost + price;
        }
    }

    let totalCostStr = String(totalCost.toFixed(2));

    let spanTotalCost = $("#total_cost");
    spanTotalCost.html(totalCostStr);
}

// remove a model from cart
$(".remove-a").on("click",function()
{
    let focusID = $(this).attr("focusID");
    let focusRow = $("#row_" + focusID);
    let cartID = focusRow.attr("cartid");

    $.post("/api/cart/remove-cart-relation",
        {
            "cart_id": cartID
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if (returnValue === 0)
                {
                    //success
                    focusRow.remove();
                } else if (returnValue === 1)
                {
                    spanQuantity.val(1);
                    calculatePrice(focusID);
                    if ($("#select_" + focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }
                }
            });
});

// change quantity by input a number
// this will automatically activate on every change of the input box
$("input").on("input",function()
{
    let focusID = $(this).attr("focusID");

    let spanQuantity = $("#quantity_"+focusID);

    let modelID = $("#row_"+focusID).attr("modelid");

    let quantityStr = spanQuantity.val();
    let quantity = parseInt(quantityStr);

    $.post("/api/cart/update-cart-count",
        {
            "model_id": modelID,
            "new_count": quantity
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    calculatePrice(focusID);
                    if($("#select_"+focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }
                }
                else if(returnValue === 2)
                {
                    spanQuantity.val(1);
                    calculatePrice(focusID);
                    if($("#select_"+focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }

                    let msg = response['msg'];
                    alert(msg);
                }
                else if(returnValue === 1)
                {
                    spanQuantity.val(1);
                    calculatePrice(focusID);
                    if($("#select_"+focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }
                }
            });
});

// add 1 to the quantity
// cannot add over the stock
$(".add-a").on("click",function()
{
    let focusID = $(this).attr("focusID");

    let spanQuantity = $("#quantity_"+focusID);

    let modelID = $("#row_"+focusID).attr("modelid");

    let quantityStr = spanQuantity.val();
    let quantity = parseInt(quantityStr);

    quantity = quantity + 1;

    $.post("/api/cart/update-cart-count",
        {
            "model_id": modelID,
            "new_count": quantity
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    quantityStr = String(quantity);

                    spanQuantity.val(quantityStr);
                    calculatePrice(focusID);
                    if($("#select_"+focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }
                }
                else if(returnValue === 2)
                {
                    let msg = response['msg'];
                    alert(msg);
                }
                else if(returnValue === 1)
                {
                    spanQuantity.val(1);
                    calculatePrice(focusID);
                    if($("#select_"+focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }
                }
            });
});

// remove 1 of quantity
// cannot remove to 0
$(".reduce-a").on("click",function()
{
    let focusID = $(this).attr("focusID");

    let spanQuantity = $("#quantity_"+focusID);

    let modelID = $("#row_"+focusID).attr("modelid");

    let quantityStr = spanQuantity.val();
    let quantity = parseInt(quantityStr);

    quantity = quantity - 1;

    $.post("/api/cart/update-cart-count",
        {
            "model_id": modelID,
            "new_count": quantity
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    quantityStr = String(quantity);

                    spanQuantity.val(quantityStr);
                    calculatePrice(focusID);
                    if($("#select_"+focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }
                }
                else if(returnValue === 1)
                {
                    spanQuantity.val(1);
                    calculatePrice(focusID);
                    if($("#select_"+focusID).prop('checked'))
                    {
                        calculateTotalCost();
                    }
                }
            });
});

$(":checkbox").on("click",function()
{
    calculateEachPrice();
    calculateTotalCost();
});

$("#checkout-a").on("click",function()
{
    let newRequest = new XMLHttpRequest();
    newRequest.open("POST", "/generate-order-from-cart", true);
    //newRequest.setRequestHeader('content-type', 'application/json');

    var selected = new Array();
    let totalRow = $("#cart_table").attr("total_row");
    for(let i=1; i<=totalRow; i++)
    {
        if($("#select_"+i).prop('checked'))
        {
            let cartID = $("#row_" + i).attr("cartid");
            selected.push(cartID);
        }
    }

    var temp = JSON.stringify(selected);

    $.post("/generate-order-from-cart",
        {
            "JSON_cart_list": temp
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];
                let order_id = response['order_id'];

                if(returnValue === 0)
                {
                    //success
                    window.location.href="/order-confirm/"+order_id;
                }
                else if(returnValue === 1)
                {

                }
            });
});
