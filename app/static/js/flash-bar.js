console.log("flash-bar activated");

$('.flash-cross').on("click",function()
{
    console.log("flash-cross clicked");
    let flashText = $('.flash-text');
    let flashBar = $('.flash-bar');

    flashText.addClass("fade-away");
    flashBar.addClass("closed");
})