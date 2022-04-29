$(document).ready(function (){

    /* when clicking on the epidemic switching button */
    $("#switch-epidemic").on('click', function (){
        console.log($("#switch-epidemic").prop("checked"))
        // get the "switch_to" status
        let switchTo = $("#switch-epidemic").prop("checked");
        // send Ajax request to switch the mode
        if (switchTo === true){
            switchEpidemicMode('1');
        }else{
            switchEpidemicMode('0');
        }

    });

});

/*
*   ---------------------------- functions use Ajax --------------------------------
*/

function switchEpidemicMode(switchTo){
    $.post("/api/the-siren/switch-epidemic-mode", {
        "switch_to": switchTo

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success

        }else{
            //failed
            //notify the user
            window.alert("Permission Denied!");
            //we refresh this page to change the switch button into the correct looking
            location.href = "/stock-management";
        }
    });
}