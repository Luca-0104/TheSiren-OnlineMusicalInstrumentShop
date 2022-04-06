let checked_value = [];

//This need to be modified if brand number is changed!!!
//Every number is plus one compared to original because "see all" option.
let checking_numbers = [7,48,5,6];

$(document).ready(function (){

     $('.category').on("click", function (){
         console.log($(this).attr('id'));
     })


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