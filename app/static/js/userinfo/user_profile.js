function topicBtnRefresh()
{
    let info_btn = $("#info_btn");
    info_btn.removeClass("clicked");
    info_btn.removeClass("clickable");
    info_btn.addClass("clickable");

    let Address_btn = $("#Address_btn");
    Address_btn.removeClass("clicked");
    Address_btn.removeClass("clickable");
    Address_btn.addClass("clickable");

    let brand_btn = $("#brand_btn");
    brand_btn.removeClass("clicked");
    brand_btn.removeClass("clickable");
    brand_btn.addClass("clickable");

    let category_btn = $("#category_btn");
    category_btn.removeClass("clicked");
    category_btn.removeClass("clickable");
    category_btn.addClass("clickable");

    let prime_btn = $("#prime_btn");
    prime_btn.removeClass("clicked");
    prime_btn.removeClass("clickable");
    prime_btn.addClass("clickable");

    let Order_btn = $("#Order_btn");
    Order_btn.removeClass("clicked");
    Order_btn.removeClass("clickable");
    Order_btn.addClass("clickable");
}

$("#info_btn").on("click",function()
{
    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    let info_btn = $("#info_btn");

    if(info_container.css("display")=='none')
    {
        info_container.css('display','');
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','none');

        topicBtnRefresh();

        info_btn.removeClass("clickable");
        info_btn.addClass("clicked");
    }
});

$("#Address_btn").on("click",function()
{
    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    let Address_btn = $("#Address_btn");

    if(address_container.css("display")=='none')
    {
        info_container.css('display','none');
        address_container.css('display','');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','none');

        topicBtnRefresh();

        Address_btn.removeClass("clickable");
        Address_btn.addClass("clicked");
    }
});

$("#brand_btn").on("click",function()
{
    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    let brand_btn = $("#brand_btn");

    if(brand_container.css("display")=='none')
    {
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','none');

        topicBtnRefresh();

        brand_btn.removeClass("clickable");
        brand_btn.addClass("clicked");
    }
});

$("#category_btn").on("click",function()
{
    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    let category_btn = $("#category_btn");

    if(category_container.css("display")=='none')
    {
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','');
        prime_container.css('display','none');
        order_container.css('display','none');

        topicBtnRefresh();

        category_btn.removeClass("clickable");
        category_btn.addClass("clicked");
    }
});

$("#prime_btn").on("click",function()
{
    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    let prime_btn = $("#prime_btn");

    if(prime_container.css("display")=='none')
    {
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','');
        order_container.css('display','none');

        topicBtnRefresh();

        prime_btn.removeClass("clickable");
        prime_btn.addClass("clicked");
    }
});

$("#Order_btn").on("click",function()
{
    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    let Order_btn = $("#Order_btn");

    if(order_container.css("display")=='none')
    {
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','');

        topicBtnRefresh();

        Order_btn.removeClass("clickable");
        Order_btn.addClass("clicked");
    }
});

window.on('load',function ()
{
    window.alert("3456789io0");
    let top_bar = $("#top_bar");
    let percent = top_bar.val();
    // top_bar.style.width= "percent%";
     top_bar.css("width",function (){return percent})
    var message = top_bar.css;
    window.alert(message);
});