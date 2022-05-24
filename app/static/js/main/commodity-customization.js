$(document).ready(function (){

    /* When selecting the customization selection  */
    $("#select-model-type").change(function (){

        // get the URL of the target page
        let targetMtURL = $(this).val();

        // check if we need to redirect to another page
        if (targetMtURL === "#modeltype-3d-model"){
            // make it slower smooth
            $('html,body').animate({ scrollTop:$("#modeltype-3d-model").offset().top - 200 },800);

        }else{
            // redirect to the details page of this model type
            location.href = targetMtURL;
        }
    });

});