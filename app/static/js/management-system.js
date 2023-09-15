// intitial add modeltype
let repeat_model_type = $("#one-model-type");
let product_form = $("#product_form")
let counter = 1;

// add listener to add-model-type button when the window is ready
$(document).ready(function ()
{
    $("#add-model-type").click(function ()
    {
        let repeat_model_name;
        let repeat_model_number;
        let repeat_model_price;
        let repeat_model_stock;
        let repeat_model_intro_pic;
        let repeat_model_pic;
        let repeat_model_description;

        console.log("#add-model-type clicked when counter is " + counter);
        console.log(counter===1);

        let prepend_content = "";

        if (counter === 1)
        {
            prepend_content = "<div class=\"card-footer col-md-12\">\n" +
                "                                       <div id=\"1_model\">\n" +
                "                                            <h4 class=\"card-title\">" + counter + ".</h4>\n" +
                "                                       </div>\n" +
                "                                   </div>"
        }
        else
        {
           prepend_content = "<div class=\"card-footer col-md-12\">\n" +
               "                                       <div id=\"1_model\">\n" +
               "                                            <h4 class=\"card-title\">" + (counter + 1) + ".</h4>\n" +
               "                                       </div>\n" +
               "                                   </div>"
        }

        if (counter === 1)
        {
            repeat_model_type.before(prepend_content);
            counter += 1;
            repeat_model_name = ["<div class=\"col-md-12\">",
                "      <div class=\"form-group\">",
                "              <label>Model Name *</label>",
                "                     <input name=\"", counter, "_model_name\" type=\"text\" class=\"form-control\" placeholder=\"Enter Name\" data-errors=\"Please Enter Name.\">",
                "                      <div class=\"help-block with-errors\"></div>",
                "        </div>",
                "  </div>"].join("");
            repeat_model_number = ["<div class=\"col-md-12\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Serial Number *</label>",
                "                                            <input name=\"", counter, "_model_num\" type=\"text\" class=\"form-control\" placeholder=\"Enter Serial Number\" data-errors=\"Please Enter Serial Number.\">",
                "                                            <div class=\"help-block with-errors\"></div>",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_price = ["<div class=\"col-md-6\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Price *</label>",
                "                                            <input name=\"", counter, "_model_price\" type=\"text\" class=\"form-control\" placeholder=\"Enter Price\" data-errors=\"Please Enter Price.\">",
                "                                            <div class=\"help-block with-errors\"></div>",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_stock = ["<div class=\"col-md-6\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Stock *</label>",
                "                                            <input name=\"", counter, "_model_stock\" type=\"text\" class=\"form-control\" placeholder=\"Enter Stock\" data-errors=\"Please Enter Stock.\">",
                "                                            <div class=\"help-block with-errors\"></div>",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_intro_pic = "";
            // repeat_model_intro_pic = ["<div class=\"col-md-12\">",
            //     "                                        <div class=\"form-group\">",
            //     "                                            <label>Thumbnail *</label>",
            //     "                                            <input name=\"", counter, "_model_intro_pic\" type=\"file\" class=\"form-control image-file\" name=\"pic\" accept=\"image/*\" multiple=\"multiple\">",
            //     "                                        </div>",
            //     "                                    </div>"].join("");
            repeat_model_pic = ["<div class=\"col-md-12\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Product Pictures *</label>",
                "                                            <input name=\"", counter, "_model_pic\" type=\"file\" class=\"form-control image-file\" name=\"pic\" accept=\"image/*\" multiple=\"multiple\">",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_description = ["<div class=\"col-md-12\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Description / Product Details</label>",
                "                                            <textarea name=\"", counter, "_model_description\" class=\"form-control\" rows=\"4\"></textarea>",
                "                                        </div>",
                "                                    </div>"].join("");
            prepend_content = "<div class=\"card-footer col-md-12\">\n" +
                "                                       <div id=\"1_model\">\n" +
                "                                            <h4 class=\"card-title\">" + counter + ".</h4>\n" +
                "                                       </div>\n" +
                "                                   </div>";
            repeat_model_type.before(repeat_model_name + repeat_model_number + repeat_model_price
                + repeat_model_stock + repeat_model_intro_pic + repeat_model_pic +
                repeat_model_description);
            console.log("current counter 1: " + counter);
            repeat_model_type.before(prepend_content);
            product_form.attr("action", "/upload-product" + "?counter=" + counter + "&serial_prefix=" + serial + "&serial_rank=" + serial_rank_g);
        }
        else
        {
            counter += 1;
            repeat_model_name = ["<div class=\"col-md-12\">",
                "      <div class=\"form-group\">",
                "              <label>Model Name *</label>",
                "                     <input name=\"", counter+1, "_model_name\" type=\"text\" class=\"form-control\" placeholder=\"Enter Name\" data-errors=\"Please Enter Name.\">",
                "                      <div class=\"help-block with-errors\"></div>",
                "        </div>",
                "  </div>"].join("");
            repeat_model_number = ["<div class=\"col-md-12\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Serial Number *</label>",
                "                                            <input name=\"", counter, "_model_num\" type=\"text\" class=\"form-control\" placeholder=\"Enter Serial Number\" data-errors=\"Please Enter Serial Number.\">",
                "                                            <div class=\"help-block with-errors\"></div>",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_price = ["<div class=\"col-md-6\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Price *</label>",
                "                                            <input name=\"", counter, "_model_price\" type=\"text\" class=\"form-control\" placeholder=\"Enter Price\" data-errors=\"Please Enter Price.\">",
                "                                            <div class=\"help-block with-errors\"></div>",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_stock = ["<div class=\"col-md-6\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Stock *</label>",
                "                                            <input name=\"", counter, "_model_stock\" type=\"text\" class=\"form-control\" placeholder=\"Enter Stock\" data-errors=\"Please Enter Stock.\">",
                "                                            <div class=\"help-block with-errors\"></div>",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_intro_pic = "";
            // repeat_model_intro_pic = ["<div class=\"col-md-12\">",
            //     "                                        <div class=\"form-group\">",
            //     "                                            <label>Thumbnail *</label>",
            //     "                                            <input name=\"", counter, "_model_intro_pic\" type=\"file\" class=\"form-control image-file\" name=\"pic\" accept=\"image/*\" multiple=\"multiple\">",
            //     "                                        </div>",
            //     "                                    </div>"].join("");
            repeat_model_pic = ["<div class=\"col-md-12\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Product Pictures *</label>",
                "                                            <input name=\"", counter, "_model_pic\" type=\"file\" class=\"form-control image-file\" name=\"pic\" accept=\"image/*\" multiple=\"multiple\">",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_description = ["<div class=\"col-md-12\">",
                "                                        <div class=\"form-group\">",
                "                                            <label>Description / Product Details</label>",
                "                                            <textarea name=\"", counter, "_model_description\" class=\"form-control\" rows=\"4\"></textarea>",
                "                                        </div>",
                "                                    </div>"].join("");
            repeat_model_type.before(repeat_model_name + repeat_model_number + repeat_model_price
                + repeat_model_stock + repeat_model_intro_pic + repeat_model_pic +
                repeat_model_description);
            console.log("current counter 2: " + counter);
            repeat_model_type.before(prepend_content);
            product_form.attr("action", "/upload-product" + "?counter=" + counter + "&serial_prefix=" + serial + "&serial_rank=" + serial_rank_g);
        }
    })
});


// initial Serial collection
let classification = $("#classification");
let type = $("#type");
let additional = $("#additional");
let brand = $("#brand");

let serial = "";
let serial_rank_g;

// add listener to any of these to perform serial_number_half_collection()
classification.change(function ()
{
    serial_number_half_collection()
});

type.change(function ()
{
    serial_number_half_collection()
});

additional.change(function ()
{
    serial_number_half_collection()
});

brand.change(function ()
{
    serial_number_half_collection()
});

// perform serial_number_half_collection() when the window is ready
$(document).ready(function ()
{
    console.log("document ready");
    serial_number_half_collection();
})

function serial_number_half_collection()
{
    console.log("");
    console.log("+++++++++++++++++++++++++++++++++++");
    console.log("serial_number_half_collection() run");
    let classification_selected = $("#classification option:selected");
    let type_selected = $("#type option:selected");
    let additional_selected = $("#additional option:selected");
    let brand_selected = $("#brand option:selected");

    let l = "-";
    serial = String(brand_selected.attr("sn"))
        + l + String(classification_selected.attr("sn"))
        + l + String(type_selected.attr("sn"))
        + l + String(additional_selected.attr("sn"));

    console.log("current serial is " + serial)
    $.post(
        "/api/stock-management/upload-product/validate-serial-p",
        {
            "serial_prefix": serial
        }).done(function (response)
    {
        let returnValue = response['returnValue'];
        let final_serial;

        console.log("ajax recive: " + returnValue);

        if (returnValue === 0)
        {
            //success
            final_serial = response["serial_number"].toString() + l;
            $("#sn_model_type").html(final_serial);
            console.log("final serical get as: " + final_serial);

            let serial_break = final_serial.split("-");
            console.log("serial break into: " + serial_break);
            let serial_rank = serial_break[serial_break.length - 2];
            console.log("serial rank: " + serial_rank);

            serial =
                String(brand_selected.attr("sn"))
                + l + String(classification_selected.attr("sn"))
                + l + String(type_selected.attr("sn"))
                + l + String(additional_selected.attr("sn"));

            console.log("new serial: " + serial);

            product_form.attr("action", "/upload-product" + "?counter=" + counter + "&serial_prefix=" + serial + "&serial_rank=" + serial_rank);
            console.log("puroduct_form's action set as: " + product_form.attr("action"));
            serial_rank_g = serial_rank;

            console.log("+++++++++++++++++++++++++++++++++++");
            console.log("");
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
        else
        {
            //failed
            return 0;
        }
    })
    serial = "";
}