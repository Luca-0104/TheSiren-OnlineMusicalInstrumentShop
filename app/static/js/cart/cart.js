
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

$("input").on("input",function()
{
    let focusID = $(this).attr("focusID");
    calculatePrice(focusID);
    if($("#select_"+focusID).prop('checked'))
    {
        calculateTotalCost();
    }
});

$(".add-a").on("click",function()
{
    console.log("add");
    let focusID = $(this).attr("focusID");

    let spanQuantity = $("#quantity_"+focusID);

    let modelID = $("row_"+focusID).attr("modelid");

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
            });
});

$(".reduce-abtn").on("click",function()
{
    let focusID = $(this).attr("focusID");

    let spanQuantity = $("#quantity_"+focusID);

    let quantityStr = spanQuantity.val();
    let quantity = parseInt(quantityStr);

    quantity = quantity - 1;

    quantityStr = String(quantity);

    spanQuantity.val(quantityStr);
    calculatePrice(focusID);
    if($("#select_"+focusID).prop('checked'))
    {
        calculateTotalCost();
    }
});

$(":checkbox").on("click",function()
{
    calculateEachPrice();
    calculateTotalCost();
});


