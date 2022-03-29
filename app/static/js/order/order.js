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

                if (returnValue === 0)
                {
                    let

                    //success
                    if(new_code == 5)
                    {
                        newHtml=""
                    }
                        <tr><td>Waiting for Payment</td></tr>
                        <tr><td><a href="#">Pay</a></td></tr>
                        <tr><td><a href="#" onclick="changeStatusTo({{ order.id }}, 5)">Cancel</a></td></tr>
                    {% elif order.status_code == 1 %}
                        <tr>
                            <td>
                                Preparing
                            </td>
                        </tr>
                    {% elif order.status_code == 2 %}
                        <tr>
                            <td>
                                On Delivery
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <a href="#" onclick="changeStatusTo({{ order.id }}, 4)">Comfirmed</a>
                            </td>
                        </tr>
                    {% elif order.status_code == 3 %}
                        <tr>
                            <td>
                                Waiting for Collection
                            </td>
                        </tr>
                    {% elif order.status_code == 4 %}
                        <tr>
                            <td>
                                Finished
                            </td>
                        </tr>
                    {% elif order.status_code == 5 %}
                        <tr>
                            <td>
                                Canceled
                            </td>
                        </tr>
                    {% elif order.status_code == 6 %}
                        <tr>
                            <td>
                                Expired
                            </td>
                        </tr>
                    {% endif %}
                }
                else
                {
                    let returnmsg = response['msg'];
                    alert(returnmsg);
                }
            });
}