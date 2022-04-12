let threed_display = $('#3d_display_section');

$(document).ready(function (){

        threed_display.hover(

            function (){
            console.log("switch");
            threed_display.style.cursor = "move";
            },

            function (){
            console.log("switch again");
            threed_display.style.cursor = "default";
        })

})
