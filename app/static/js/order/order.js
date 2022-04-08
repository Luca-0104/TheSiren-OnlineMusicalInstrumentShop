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

                let orderRow = $("#order_row_"+order_id);
                let actionTable = $("#action_table_"+order_id);

                if(returnValue === 0)
                {

                    //success
                    if(new_code == 5)
                    {
                        orderRow.attr('current_status_code',5);
                        let newHtml="<tr><td>Canceled</td></tr>";
                        actionTable.empty();
                        actionTable.html(newHtml);
                    }
                    else if(new_code == 4)
                    {
                        orderRow.attr('current_status_code',4);
                        let newHtml="<tr><td>After Sale Service</td></tr><tr><td>Comment</td></tr>";
                        actionTable.empty();
                        actionTable.html(newHtml);
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

    $(".order_row").each(function()
    {
        if(subAimID == -1)
        {
            $(this).css('display','');
        }
        else if(subAimID == $(this).attr('current_status_code'))
        {
            $(this).css('display','');
        }
        else
        {
            $(this).css('display','none');
        }
    });
});