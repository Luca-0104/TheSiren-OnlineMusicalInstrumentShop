$(document).ready(function (){

    /* When selecting the customization selection  */
    $("#select-model-type").change(function (){
        // get the URL of the target page
        let targetMtURL = $(this).val();
        console.log(targetMtURL);

        // redirect to the details page of this model type
        location.href = targetMtURL;
    });

});