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
    }
    else if(checkValue==='Important')
    {
        console.log("2");
        $(this).addClass("btn-info");
        priority_sort.html(2);
    }
    else if(checkValue==='Significant')
    {
        console.log("3");
        $(this).addClass("btn-secondary");
        priority_sort.html(3);
    }
});