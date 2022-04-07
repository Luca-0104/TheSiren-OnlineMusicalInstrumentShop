let checked_value = new Array(4);
    checked_value = ['','','',''];

let classification, type, additional, brand;

let data;
//This need to be modified if brand number is changed!!!
//Every number is plus one compared to original because "see all" option.
let checking_numbers = [7,48,5,6];

function initialize_checkbox(param){
    let p = 0;
    if     (param === "#check_class_"){p = 0;}
    else if (param === "#check_type_"){p = 1;}
    else if  (param === "#check_add_"){p = 2;}
    else if(param === "#check_brand_"){p = 3;}
    for (let i=1; i<=checking_numbers[p]; i++){
         let init_select = $(param+i);
         init_select.click();
    }
}

$(document).ready(function (){

     initialize_checkbox("#check_class_");
     initialize_checkbox("#check_type_");
     initialize_checkbox("#check_add_");
     initialize_checkbox("#check_brand_");

     $('.category').on("change", function (){
         console.log($(this).attr('id'));

         console.log($(this).attr("checked"));
         let p = $(this).attr('id').split('_').pop();
         console.log(p);

         if (!$(this).prop('checked')){

             for (let i = 1; i <= checking_numbers[0]; i++){
                 if(p !== i){
                     let cancel_select = $('#check_class_'+i);
                     cancel_select.attr("class","checkbox category");
                     cancel_select.prop("checked","off");

                 }
             }
             $(this).attr("class","checkbox w--redirected-checked category");
             $(this).prop("checked","on");

             checked_value[0] = $(this).attr("name");

             classification = checked_value[0];
             console.log($(this).attr("checked")+'2');
             console.log(checked_value);
         }
     });

     $('.type').on("change", function (){
         console.log($(this).attr('id'));

         console.log($(this).attr("checked"));
         let p = $(this).attr('id').split('_').pop();
         console.log(p);

         if (!$(this).prop('checked')){

             for (let i = 1; i <= checking_numbers[1]; i++){
                 if(p !== i){
                     let cancel_select = $('#check_type_'+i);
                     cancel_select.attr("class","checkbox type");
                     cancel_select.prop("checked","off");
                 }
             }
             $(this).attr("class","checkbox w--redirected-checked type");
             $(this).prop("checked","on");

             checked_value[1] = $(this).attr("name");

             type = checked_value[1];
             console.log($(this).attr("checked")+'2');
             console.log(checked_value);
         }
     });


     $('.add').on("change", function (){
         console.log($(this).attr('id'));

         console.log($(this).attr("checked"));
         let p = $(this).attr('id').split('_').pop();
         console.log(p);

         if (!$(this).prop('checked')){

             for (let i = 1; i <= checking_numbers[2]; i++){
                 if(p !== i){
                     let cancel_select = $('#check_add_'+i);
                     cancel_select.attr("class","checkbox add");
                     cancel_select.prop("checked","off");
                 }
             }
             $(this).attr("class","checkbox w--redirected-checked add");
             $(this).prop("checked","on");

             checked_value[2] = $(this).attr("name");

             additional = checked_value[2];
             console.log($(this).attr("checked")+'2');
             console.log(checked_value);
         }
     });

     $('.brands').on("change", function (){
         console.log($(this).attr('id'));

         console.log($(this).attr("checked"));
         let p = $(this).attr('id').split('_').pop();
         console.log(p);

         if (!$(this).prop('checked')){

             for (let i = 1; i <= checking_numbers[3]; i++){
                 if(p !== i){
                     let cancel_select = $('#check_brand_'+i);
                     cancel_select.attr("class","checkbox brand");
                     cancel_select.prop("checked","off");
                 }
             }
             $(this).attr("class","checkbox w--redirected-checked brand");
             $(this).prop("checked","on");

             checked_value[3] = $(this).attr("name");

             brand = checked_value[3];
             console.log($(this).attr("checked")+'2');
             console.log(checked_value);
         }
     });



     $.post("/api/filter-model-types",
        {
            "c": classification,
            "t": type,
            "a": additional,
            "b": brand
        }).done(function (response)
            {
                console.log('')
                // get from server
                let returnValue = response['returnValue'];

                console.log(returnValue);

                if(returnValue === 0)
                {
                    //success
                    // console.log("ModelType " + model_type_id + "removed");
                    data = response['data'];
                    console.log("data below")
                    console.log(data)
                }
                else if(returnValue === 1){
                    //failure

                }
            });


        $("input[name='checkboxes']:checked").each(function(){
            checked_value=[];
            checked_value.push($(this).val());
            console.log(checked_value);
        });



});