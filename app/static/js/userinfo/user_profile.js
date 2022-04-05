$("#info_btn").on("click",function()
{
    console.log("#info_btn clicked");

    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    let info_btn = $("#info_btn");
    let Address_btn = $("#info_btn");
    let brand_btn = $("#info_btn");
    let category_btn = $("#info_btn");
    let prime_btn = $("#info_btn");
    let Order_btn = $("#info_btn");

    if(info_container.css("display")=='none')
    {
        console.log("#info_container to show");
        info_container.css('display','');
        console.log(info_container.css("display"));
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','none');
    }
});

$("#Address_btn").on("click",function()
{
    console.log("#info_btn clicked");

    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    if(address_container.css("display")=='none')
    {
        console.log("#address_container to show");
        info_container.css('display','none');
        address_container.css('display','');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','none');
    }
});

$("#brand_btn").on("click",function()
{
    console.log("#info_btn clicked");

    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    if(brand_container.css("display")=='none')
    {
        console.log("#brand_container to show");
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','none');
    }
});

$("#category_btn").on("click",function()
{
    console.log("#info_btn clicked");

    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    if(category_container.css("display")=='none')
    {
        console.log("#category_container to show");
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','');
        prime_container.css('display','none');
        order_container.css('display','none');
    }
});

$("#prime_btn").on("click",function()
{
    console.log("#info_btn clicked");

    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    if(prime_container.css("display")=='none')
    {
        console.log("#prime_container to show");
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','');
        order_container.css('display','none');
    }
});

$("#Order_btn").on("click",function()
{
    console.log("#info_btn clicked");

    let info_container = $("#info_container");
    let address_container = $("#address_container");
    let brand_container = $("#brand_container");
    let category_container = $("#category_container");
    let prime_container = $("#prime_container");
    let order_container = $("#order_container");

    if(order_container.css("display")=='none')
    {
        console.log("#order_container to show");
        info_container.css('display','none');
        address_container.css('display','none');
        brand_container.css('display','none');
        category_container.css('display','none');
        prime_container.css('display','none');
        order_container.css('display','');
    }
});