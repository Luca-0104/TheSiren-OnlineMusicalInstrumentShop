$(document).ready(function (){

    //set the address as selected
    $(".address").on("click", function(){
        //only let the selected one have the style of "chosen-class"
        $(".address").removeClass("chosen-address");
        $(this).addClass("chosen-address");

        //send a ajax request to update the order info

    });

});