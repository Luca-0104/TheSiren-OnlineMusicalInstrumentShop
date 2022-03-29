function changeStatusTo(order_id, new_code)
{
    $.post("/api/order/my-orders/change-status",
        {
            "new_code": new_code,
            "order_id": order_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                let statusTable = $("#status_table_"+order_id);

                if(returnValue === 0)
                {

                    //success
                    if(new_code == 5)
                    {
                        let newHtml="<tr><td>Canceled</td></tr>";
                        statusTable.empty();
                        statusTable.html(newHtml);
                    }
                    else if(new_code == 4)
                    {
                        let newHtml="<tr><td>Finished</td></tr>";
                        statusTable.empty();
                        statusTable.html(newHtml);
                    }
                }
                else
                {
                    let returnmsg = response['msg'];
                    alert(returnmsg);
                }
            });
}

$(".subSec").on("click",function()
{
    let subAimID = $(this).attr("subAim");
    let curAim = $(".selectedOne");

    curAim.removeClass("selectedOne");
    $(this).addClass("selectedOne");

    $.post("/api/order/my-orders/filter-orders",
        {
            "status_code": subAimID
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];
                let newOrders = response['data'];

                console.log(returnValue);

                console.log(newOrders);

                if(returnValue === 0)
                {

                    //success

                }
            });
});