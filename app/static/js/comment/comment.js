$(".star ").on("click",function()
{
    let star_level = $(this).attr("star-level");
    console.log(star_level);
    for(let i=1; i<=5; i++)
    {
        if(i<=star_level)
        {
            $("#star_"+i).removeClass("star-dark");
            $("#star_"+i).addClass("star-bright");
        }
        else
        {
            $("#star_" + i).removeClass("star-bright");
            $("#star_" + i).addClass("star-dark");
        }
    }
    $("#form-rate").val(star_level);
});

//This part is newly added
$('#comment_send').on('click', function(){
    console.log("send comment");
    $.post('',

    )
});