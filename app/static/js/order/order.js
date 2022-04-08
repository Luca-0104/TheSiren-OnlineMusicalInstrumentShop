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

    // $.post("/api/order/my-orders/filter-orders",
    //     {
    //         "status_code": subAimID
    //     }).done(function (response)
    //         {
    //             // get from server (backend)
    //             let returnValue = response['returnValue'];
    //             let newOrders = response['data'];
    //
    //             console.log(returnValue);
    //
    //             console.log(newOrders);
    //
    //             if(returnValue === 0)
    //             {
    //                 let mainTable = $("#order-listing-table");
    //                 mainTable.empty();
    //
    //                 let newHtml = "";
    //
    //                 //success
    //                 for(let i=0; i<newOrders.length; i++)
    //                 {
    //                     let order = newOrders[i];
    //                     newHtml = newHtml +
    //                     "<tr>"+
    //                         "<td href=\"#\" onClick=\"window.open('/order-details/" + order["id"] + "');\">"+
    //                             "<table border=\"1\" width=\"100%\" height=\"100%\" className=\"clickable\">"+
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Recipient Name"+
    //                                     "</td>"+
    //                                     "<td>"+
    //                                         order["address"]["recipient_name"]+
    //                                     "</td>"+
    //                                 "</tr>"+
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Contact Phone"+
    //                                     "</td>"+
    //                                     "<td>"+
    //                                         order["address"]["phone"]+
    //                                     "</td>"+
    //                                 "</tr>"+
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Address"+
    //                                     "</td>"+
    //                                     "<td>"+
    //                                         order["address"]["contry"]+order["address"]["province_or_state"]+order["address"]["city"]+order["address"]["city"]+
    //                                     "</td>"+
    //                                 "</tr>"+
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Time Stamp"+
    //                                     "</td>"+
    //                                     "<td>"+
    //                                         order["timestamp"]+
    //                                     "</td>"+
    //                                 "</tr>"+
    //                             "</table>"+
    //                         "</td>"+
    //                         "<td>"+
    //                             "<table border=\"1\" width=\"100%\" height=\"100%\">";
    //                     for(let j=0; j<Math.min(order['model_types'].length, 4); j++)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<td>"+
    //                                     "<img src=\"../../static/images/example/yamaha_yep621s.jpg\" loading=\"lazy\" alt=\"\" class=\"w-commerce-commercecartitemimage cart-item-image\">"
    //                                 "</td>";
    //
    //                     }
    //                     newHtml = newHtml +
    //                             "</table>"+
    //                         "</td>"+
    //                         "<td>"+
    //                             "<table id=\"status_table_" + order['id'] + "\" border=\"1\" width=\"100%\" height=\"100%\">";
    //                     if(order['status_code'] == 0)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Waiting for Payment"+
    //                                     "</td>"+
    //                                 "</tr>"+
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "<a href=\"#\">Pay</a>"+
    //                                     "</td>"+
    //                                 "</tr>"+
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "<a href=\"#\" onClick=\"changeStatusTo(" + order['id'] + ", 5)\">Cancel</a>"+
    //                                     "</td>"+
    //                                 "</tr>";
    //                     }
    //                     else if(order['status_code'] == 1)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Preparing"+
    //                                     "</td>"+
    //                                 "</tr>";
    //                     }
    //                     else if(order['status_code'] == 2)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "On Delivery"+
    //                                     "</td>"+
    //                                 "</tr>"+
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "<a href=\"#\" onClick=\"changeStatusTo(" + order['id'] + ", 4)\">Comfirmed</a>"+
    //                                     "</td>"+
    //                                 "</tr>";
    //                     }
    //                     else if(order['status_code'] == 3)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Waiting for Collection"+
    //                                     "</td>"+
    //                                 "</tr>";
    //                     }
    //                     else if(order['status_code'] == 4)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Finished"+
    //                                     "</td>"+
    //                                 "</tr>";
    //                     }
    //                     else if(order['status_code'] == 5)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Canceled"+
    //                                     "</td>"+
    //                                 "</tr>";
    //                     }
    //                     else if(order['status_code'] == 6)
    //                     {
    //                         newHtml = newHtml +
    //                                 "<tr>"+
    //                                     "<td>"+
    //                                         "Expired"+
    //                                     "</td>"+
    //                                 "</tr>";
    //                     }
    //
    //                     newHtml = newHtml +
    //                             "</table>"+
    //                         "</td>"+
    //                     "</tr>";
    //                 }
    //                 mainTable.html(newHtml);
    //             }
    //         });
});