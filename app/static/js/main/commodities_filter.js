let checked_value = [];

//This need to be modified if brand number is changed!!!
//Every number is plus one compared to original because "see all" option.
let checking_numbers = [7,48,5,6];

function initialize_checkbox(param){
    let p = 0;
    if (param === "#check_class_"){
        p = 0
    }
    else if(param === "#check_type_"){}
    else if(param === "#check_add_"){}
    else if(param === "#check_brand_"){}
    for (let i=1; i<=checking_numbers[0]; i++){
         let init_select = $('#check_class_'+i);
         init_select.click();

    }
}

$(document).ready(function (){

     for (let i=1; i<=checking_numbers[0]; i++){
         let init_select = $('#check_class_'+i);
         init_select.click();

     }
     for (let i=1; i<=checking_numbers[1]; i++){
         let init_select = $('#check_type_'+i);
         init_select.click();
     }
     $('.category').on("change", function (){
         console.log($(this).attr('id'));

         console.log($(this).attr("checked"));
         let p = $(this).attr('id').split('_').pop();
         console.log(p);

         if (!$(this).prop('checked')){
             console.log("############");
             for (let i = 1; i <= checking_numbers[0]; i++){
                 if(p !== i){
                     let cancel_select = $('#check_class_'+i);
                     cancel_select.attr("class","checkbox category");
                     cancel_select.prop("checked","off");
                     console.log("@@@@@@@@@");
                 }
             }
             $(this).attr("class","checkbox w--redirected-checked category");
             $(this).prop("checked","on");

             console.log($(this).attr("checked")+'2');
         }
     });


     // $('#category_checkbox').on("change",function (){
     //    for (let i=1; i<=7; i++){
     //        console.log(i);
     //        $('#check_class_'+i).on("click",function (){
     //            $(this).attr("class","checkbox w--redirected-checked");
     //            $(this).attr("checked","checked");
     //        })
     //    }
     // });

        $("input[name='checkboxes']:checked").each(function(){
            checked_value=[];
            checked_value.push($(this).val());
            console.log(checked_value);
        });

});