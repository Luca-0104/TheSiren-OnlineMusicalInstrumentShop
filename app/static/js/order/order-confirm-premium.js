$(document).ready(function (){

    //the currently selected plan
    let selectedPlanID = "plan-30";

    //set the payment info of default plan (30days)
    $("#pay-total").text("98");

    //98 198 328 648 (30, 90, 180, 360 days)
    //3.2666, 2.2, 1.8222, 1.80 (per day)

    /* when a plan is clicked */
    $("#premium-plan-field ul li").on("click", function (){
        //deprive off the "selected" css class from all plans
        $("#premium-plan-field ul li").removeClass("chosen-plan");
        //add the "selected" css class for the selected one
        $(this).addClass("chosen-plan");

        //get the id of the plan
        let planID = $(this).attr("id");
        //update currently selected plan
        selectedPlanID = planID;
        //update the payment info
        if(planID === "plan-30"){
            $("#pay-total").text("98");
        }else if(planID === "plan-90"){
            $("#pay-total").text("198");
        }else if(planID === "plan-180"){
            $("#pay-total").text("328");
        }else if(planID === "plan-360"){
            $("#pay-total").text("648");
        }

    });

    /* When the "place order" btn is clicked */
    $("#btn-place-order").on("click", function (){
        //get payment info
        let payment = $("#pay-total").html();
        //get duration according to the plan
        let duration = 0;
        if (selectedPlanID === "plan-30"){
            duration = 30;
        }else if (selectedPlanID === "plan-90"){
            duration = 90;
        }else if (selectedPlanID === "plan-180"){
            duration = 180;
        }else if (selectedPlanID === "plan-360"){
            duration = 360;
        }
        //send Ajax request to the server to create premium order
        create_premium_order(duration, payment);
    });

});

/*
    ------------------------------ functions Using Ajax ------------------------------
 */

function create_premium_order(duration, payment){
    $.post("/api/generate-premium-order", {
        "duration": duration,
        "payment": payment

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            //get the id of newly created premium order
            let pOrderID = response['p_order_id'];
            //send an Ajax request to pay for the order
            pay_for_premium_order(pOrderID);
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}

function pay_for_premium_order(pOrderID){
    $.post("/api/pay-for-order/premium", {
        "p_order_id": pOrderID

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            // get payment URL then redirect to that URL
            let paymentURL = response['paymentURL']
            location.href = paymentURL;
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}