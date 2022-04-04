$("#show").on("click",function()
{
    let target = $("#avatar_form");
    if(target.css("display")=='none')
    {
        target.css('display','');
    }
});

$("#close_triger").on("click",function()
{
    let target = $("#avatar_form");
    if(target.css("display")!='none')
    {
        target.css('display','none');
    }
});