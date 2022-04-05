$("#show_edit").on("click",function()
{window.alert("1111111111")
    let target = $("#profile_form");
    if(target.css("display")=='none')
    {
        window.alert("2222222222")
        target.css('display','');
        window.alert(target.css)
    }
});

$("#close_triger").on("click",function()
{
    let target = $("#profile_form");
    if(target.css("display")!='none')
    {
        target.css('display','none');
    }
});