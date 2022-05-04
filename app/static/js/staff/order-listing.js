$(".priority-select").change(function()
{
    console.log("run");
    let orderId = $(this).attr("orderId");
    let checkValue = $(this).val();
    let priority_sort = $("#priority-sort-"+orderId);

    $(this).removeClass("btn-light");
    $(this).removeClass("btn-info");
    $(this).removeClass("btn-secondary");

    if(checkValue==='Normal')
    {
        console.log("1");
        $(this).addClass("btn-light");
        priority_sort.html(1);
        update_priority(orderId, 1);
    }
    else if(checkValue==='Important')
    {
        console.log("2");
        $(this).addClass("btn-info");
        priority_sort.html(2);
        update_priority(orderId, 2);
    }
    else if(checkValue==='Significant')
    {
        console.log("3");
        $(this).addClass("btn-secondary");
        priority_sort.html(3);
        update_priority(orderId, 3);
    }
});

function update_priority(orderId, newPriority)
{
    $.post("/api/order-management/update-priority",
        {
            "order_id": orderId,
            "new_priority": newPriority
        }).done(function (response)
        {
            //get response from server
            let returnValue = response['returnValue'];

            if (returnValue === 0)
            {
                console.log('successed');
                //success
                location.reload();
            }
        });
}