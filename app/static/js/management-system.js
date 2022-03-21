let repeat_model_type = $("#one-model-type");
let counter = 1;
$(document).ready(function (){
    $("#add-model-type").click(function (){
        let prepend_content = "<div class=\"card-footer col-md-12\">\n" +
                "                                       <div id=\"1_model\">\n" +
                "                                            <h4 class=\"card-title\">" + counter + ".</h4>\n" +
                "                                       </div>\n" +
                "                                   </div>"
            if(counter === 1){
                repeat_model_type.before(prepend_content);
                counter += 1;
                prepend_content = "<div class=\"card-footer col-md-12\">\n" +
                "                                       <div id=\"1_model\">\n" +
                "                                            <h4 class=\"card-title\">" + counter + ".</h4>\n" +
                "                                       </div>\n" +
                "                                   </div>"
                console.log(prepend_content);
                console.log(counter);
            }
            repeat_model_type.before(repeat_model_type.html());
            repeat_model_type.before(prepend_content);

            counter += 1;
    })
});
