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
                let statusBar = $("#status_"+order_id);
                let actionTable = $("#action_table_"+order_id);

                if(returnValue === 0)
                {
                    //success
                    if(new_code == 5)
                    {
                        orderRow.attr("current_status_code",5);

                        let newStatusHtml = "<td colspan=\"3\" class=\"status_col status_c\"> Canceled </td>";
                        statusBar.empty();
                        statusBar.html(newStatusHtml);

                        actionTable.empty();
                    }
                    else if(new_code == 4)
                    {
                        orderRow.attr("current_status_code",4);

                        let newStatusHtml = "<td colspan=\"3\" class=\"status_col status_f\"> Finished </td>";
                        statusBar.empty();
                        statusBar.html(newStatusHtml);

                        let newActionHtml = "<tr><td className=\"clickable action_service button\" onClick=\"\">After Sale Service</td></tr>"+
                                        "<tr><td className=\"clickable action_Comment button\" onClick=\"\">Comment</td></tr>";
                        actionTable.empty();
                        actionTable.html(Action);
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