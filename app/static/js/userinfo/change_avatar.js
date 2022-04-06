$("#show_change_avatar_form_btn").on("click",function()
{
    let blocker = $("#profile_form_blocker");
    let show_add_form = $("#change_avatar_form");
    if(blocker.css("display")=='none')
    {
        blocker.css('display','');
        show_add_form.css('display','');
    }
});

$("#close_change_avatar_form_btn").on("click",function()
{
    let blocker = $("#profile_form_blocker");
    let show_add_form = $("#change_avatar_form");
    if(blocker.css("display")!='none')
    {
        blocker.css('display','none');
        show_add_form.css('display','none');
    }
});