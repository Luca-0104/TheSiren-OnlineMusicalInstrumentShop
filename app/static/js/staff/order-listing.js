console.log("js order-listing");

$(".priority-select").change(function () {
    let orderId = $(this).attr("orderId");
    let checkValue = $(this).val();
    let priority_sort = $("#priority-sort-" + orderId);

    $(this).removeClass("btn-light");
    $(this).removeClass("btn-info");
    $(this).removeClass("btn-secondary");

    if (checkValue === 'Normal') {
        $(this).addClass("btn-light");
        priority_sort.html(1);
        update_priority(orderId, 1);
    } else if (checkValue === 'Important') {
        $(this).addClass("btn-info");
        priority_sort.html(2);
        update_priority(orderId, 2);
    } else if (checkValue === 'Significant') {
        $(this).addClass("btn-secondary");
        priority_sort.html(3);
        update_priority(orderId, 3);
    }
});

function update_priority(orderId, newPriority) {
    $.post("/api/order-management/update-priority",
        {
            "order_id": orderId,
            "new_priority": newPriority
        }).done(function (response) {
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) {
            //success
            location.reload();
        }
    });
}

function changeStatusTo(order_id, new_code) {
    $.post("/api/order/my-orders/change-status",
        {
            "new_code": new_code,
            "order_id": order_id
        }).done(function (response) {
        // get from server (backend)
        let returnValue = response['returnValue'];

        if (returnValue === 0) {
            //success
            location.reload();
        }
    });
}

$(".type-select").change(function () {
    console.log("here");
});