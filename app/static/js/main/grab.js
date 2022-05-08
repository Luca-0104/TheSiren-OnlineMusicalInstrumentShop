$(".grab").on("mousedown", function ()
{
    $(this).removeClass("grab");
    $(this).addClass("grabbing")
});

document.addEventListener("mouseup",function ()
{
   $(".grabbing").addClass("grab");
   $(".grabbing").removeClass("grabbing");
});