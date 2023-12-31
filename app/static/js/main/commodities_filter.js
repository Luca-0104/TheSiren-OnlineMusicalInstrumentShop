let checked_value = new Array(4);
checked_value = ['', '', '', ''];

let classification, type, additional, brand;

let data;
//This need to be modified if brand number is changed!!!
//Every number is plus one compared to original because "see all" option.
let checking_numbers = [7, 47, 5, 18];

function initialize_checkbox(param)
{
    let p = 0;
    if (param === "#check_class_")
    {
        p = 0;
    }
    else if (param === "#check_type_")
    {
        p = 1;
    }
    else if (param === "#check_add_")
    {
        p = 2;
    }
    else if (param === "#check_brand_")
    {
        p = 3;
    }
    // console.log("Initializing p: " + p);
    for (let i = 1; i <= checking_numbers[p]; i++)
    {
        let init_select = $(param + i);
        // console.log("Checking i: " + i + " : " + init_select.prop('checked'));
        init_select.click();
        // console.log("Checked i: " + i + " : " + init_select.prop('checked'));
        // console.log("")
    }
    // console.log("+++++++++++++++++++++++++++++++++++++++++++++++");
}

$(document).ready(function ()
{

    initialize_checkbox("#check_class_");
    initialize_checkbox("#check_type_");
    initialize_checkbox("#check_add_");
    initialize_checkbox("#check_brand_");

    $('.category').on("change", function ()
    {
        //for test
        // console.log($(this).attr('id'));
        //
        // console.log($(this).prop('checked'));

        let p = $(this).attr('id').split('_').pop();

        if (!$(this).prop('checked'))
        {

            for (let i = 1; i <= checking_numbers[0]; i++)
            {
                if (p !== i)
                {
                    let cancel_select = $('#check_class_' + i);
                    cancel_select.attr("class", "checkbox category");
                    // console.log("Before " + cancel_select.prop('checked'));
                    cancel_select.prop("checked", "off");
                    // console.log("After " + cancel_select.prop('checked'));
                }
            }
            $(this).attr("class", "checkbox w--redirected-checked category");
            $(this).prop("checked", "on");

            checked_value[0] = $(this).attr("name");

            classification = checked_value[0];
            // console.log($(this).attr("checked") + '2');
            // console.log(checked_value);

            //only show the "type" boxes of this class
            update_type_boxes($(this).attr("id"));
        }
    });

    $('.type').on("change", function ()
    {
        // console.log("type checked " + $(this).attr('id'));
        //
        // console.log("type checked " + $(this).prop('checked'));
        let p = $(this).attr('id').split('_').pop();
        // console.log(p);

        if (!$(this).prop('checked'))
        {
            for (let i = 1; i <= checking_numbers[1]; i++)
            {
                if (p !== i)
                {
                    let cancel_select = $('#check_type_' + i);
                    cancel_select.attr("class", "checkbox type");
                    cancel_select.prop("checked", "off");
                }
            }
            $(this).attr("class", "checkbox w--redirected-checked type");
            $(this).prop("checked", "on");

            checked_value[1] = $(this).attr("name");

            type = checked_value[1];
            // console.log($(this).attr("checked") + '2');
            // console.log(checked_value);
        }
    });

    $('.add').on("change", function ()
    {
        // console.log($(this).attr('id'));
        //
        // console.log($(this).prop('checked'));
        let p = $(this).attr('id').split('_').pop();
        // console.log(p);

        if (!$(this).prop('checked'))
        {

            for (let i = 1; i <= checking_numbers[2]; i++)
            {
                if (p !== i)
                {
                    let cancel_select = $('#check_add_' + i);
                    cancel_select.attr("class", "checkbox add");
                    cancel_select.prop("checked", "off");
                }
            }
            $(this).attr("class", "checkbox w--redirected-checked add");
            $(this).prop("checked", "on");

            checked_value[2] = $(this).attr("name");

            additional = checked_value[2];
            // console.log($(this).attr("checked") + '2');
            // console.log(checked_value);
        }
    });

    $('.brands').on("change", function ()
    {
        console.log("==========================================");
        console.log(checking_numbers[3]);
        console.log($(this).attr('id'));

        console.log($(this).prop('checked'));
        let p = $(this).attr('id').split('_').pop();
        console.log(p);

        if (!$(this).prop('checked'))
        {
            for (let i = 1; i <= checking_numbers[3]; i++)
            {
                if (p !== i)
                {
                    let cancel_select = $('#check_brand_' + i);
                    cancel_select.attr("class", "checkbox brand");
                    // console.log(i + " Before " + cancel_select.prop('checked'));
                    cancel_select.prop("checked", "off");
                    // console.log(i + " After " + cancel_select.prop('checked'));
                    // console.log("");
                }
            }
            $(this).attr("class", "checkbox w--redirected-checked brand");
            $(this).prop("checked", "on");

            checked_value[3] = $(this).attr("name");

            brand = checked_value[3];
            // console.log($(this).prop('checked') + '2');
            // console.log(checked_value);
        }
    });

    $('#category_checkbox').on("change", function ()
    {
        //get the search content
        //we need to sent it back to server to search again before filtering
        let searchContent = $("#search").val();

        console.log("ajax")
        console.log("class " + classification)
        console.log("type " + type)
        console.log("additional " + additional)
        console.log("brand " + brand)

        $.post(
            "/api/filter-model-types",
            {
                "c": classification,
                "t": type,
                "a": additional,
                "b": brand,
                "search_content": searchContent

            }).done(function (response)
        {
            // get from server
            let returnValue = response['returnValue'];

            // console.log("recived");

            if (returnValue === 0)
            {
                //success
                data = response['data'];
                // console.log("data below")
                // console.log(data)
                //clear all the model card on this page
                $("#model-list").empty();
                if(data.length > 0)
                {
                    let empty_notify_box = $("#empty-notify-box");
                    empty_notify_box.css('display','none');
                    //put model data on the product card in this page
                    $.each(data, function ()
                    {
                        put_data(this);
                    });
                }
                else
                {
                    let empty_notify_msg = $("#empty-notify-msg");
                    empty_notify_msg.html(get_empty_notify_msg());
                    let empty_notify_box = $("#empty-notify-box");
                    empty_notify_box.css('display','');
                }

            }
            else if (returnValue === 1)
            {
                //failure

            }
            else if (returnValue === 318)
            {
                let targetURL = response['redirectURL'];
                window.location.href = targetURL;
            }
        });
    })

    $("input[name='checkboxes']:checked").each(function ()
    {
        checked_value = [];
        checked_value.push($(this).val());
        console.log(checked_value);
    });

});


/**
 *
 * @param classID The HTML id of class_checkbox
 */
function update_type_boxes(classID)
{
    // initialize_checkbox("#check_type_");

    // firstly, we recover all checkboxes
    $("#type_checkbox label").removeClass("invisible-checkbox");

    /* Then we make them display none */
    if (classID === "check_class_1")
    {
        //see all

    }
    else if (classID === "check_class_2")
    {
        //String
        //(#check_type_14 ~ #check_type_47) are not "String"
        for (let i = 14; i < 48; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }

    }
    else if (classID === "check_class_3")
    {
        //Woodwinds
        //(#check_type_2 ~ #check_type_13) are not "Woodwinds"
        //(#check_type_25 ~ #check_type_47) are not "Woodwinds"
        for (let i = 2; i < 14; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }
        for (let i = 25; i < 48; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }

    }
    else if (classID === "check_class_4")
    {
        //Brass
        //(#check_type_2 ~ #check_type_24) are not "Brass"
        //(#check_type_31 ~ #check_type_47) are not "Brass"
        for (let i = 2; i < 25; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }
        for (let i = 31; i < 48; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }

    }
    else if (classID === "check_class_5")
    {
        //Percussion
        //(#check_type_2 ~ #check_type_30) are not "Percussion"
        //(#check_type_41 ~ #check_type_47) are not "Percussion"
        //(#check_type_35) is not "Percussion"
        for (let i = 2; i < 31; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }
        for (let i = 41; i < 48; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }
        $("#check_type_35").parent("label").addClass("invisible-checkbox");

    }
    else if (classID === "check_class_6")
    {
        //Keyboard
        //(#check_type_2 ~ #check_type_41) are not "Keyboard"
        //(#check_type_45 ~ #check_type_47) are not "Keyboard"
        for (let i = 2; i < 41; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }
        for (let i = 45; i < 48; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }

    }
    else if (classID === "check_class_7")
    {
        //Accessories
        //(#check_type_2 ~ #check_type_44) are not "Accessories"
        //(#check_type_35) is "Percussion"
        for (let i = 2; i < 44; i++)
        {
            let id = "#check_type_" + i;
            $(id).parent("label").addClass("invisible-checkbox");
        }
        $("#check_type_35").parent("label").removeClass("invisible-checkbox");
    }

    let see_all_check = $("#check_type_1");
    see_all_check.click();
    let p = see_all_check.attr('id').split('_').pop();

    if (!see_all_check.prop('checked'))
    {
        for (let i = 1; i <= checking_numbers[1]; i++)
        {
            if (p !== i)
            {
                let cancel_select = $('#check_type_' + i);
                cancel_select.attr("class", "checkbox type");
                cancel_select.prop("checked", "off");
            }
        }
        see_all_check.attr("class", "checkbox w--redirected-checked type");
        see_all_check.prop("checked", "on");

        checked_value[1] = see_all_check.attr("name");
        type = checked_value[1];
    }
}


/**
 * This function is for putting the model data on the product card in this page
 * @param mt mt refers to "model type", each one should be a dict
 */
function put_data(mt)
{
    //get basic info of this model type
    let mtID = mt.id;
    let mtName = mt.name;
    let mtPrice = mt.price;
    let brandName = mt.brand_name;
    let firstPicAddress = mt.pictures[0].address;
    let additionType = mt.addition_type;

    //put those info on to model card
    let cardHTML = '<div role="listitem" class="w-dyn-item commodity-card">'
        + '<div>'
        + '<a href="/product-details/' + mtID + '" class="product-preview-link w-inline-block">'
        + '<div class="commodity-pic commodity-pic' + additionType + '">'
        + '<img src="../../static/' + firstPicAddress + '"loading="lazy" alt="" class="product-thumbnail">'
        + '</div>'
        + '<div class="uppercase-text brand brand-row">' + brandName + '</div>'
        + '<h5 class="no-bottom-margin">' + mtName + '</h5>'
        + '<div class="price-container">'
        + '<div class="old-price"><span>$</span>' + (mtPrice*2) + '</div>'
        + '<div><span>$</span>' + mtPrice + '</div>'
        + '</div>'
        + '</a>'
        + '</div>'
        + '</div>';

    $("#model-list").append(cardHTML);
}

function get_empty_notify_msg()
{
    let msg = "Currently no";

    // console.log("class " + classification)
    // console.log("type " + type)
    // console.log("additional " + additional)
    // console.log("brand " + brand)

    if(type != "" && type != undefined)
    {
        msg = msg + " " + get_name(type);
    }
    else
    {
        msg = msg + " commodity";
    }

    if(classification != "" && classification != undefined)
    {
        msg = msg + " in " + get_name(classification) + " class";
    }
    else
    {

    }

    if(brand != "" && brand != undefined)
    {
        msg = msg + " from " + get_name(brand);
    }
    else
    {

    }

    if(additional != "" && additional != undefined)
    {
        msg = msg + " that satisfies " + get_name(additional);
    }
    else
    {

    }

    return msg;
}

function get_name(mark)
{
    let name = "";
    let target_element = $("[name='" + mark + "']");
    let raw_texts = target_element.parent().text().split("\n");
    let target_text = "";
    for(let i=0; i<raw_texts.length; i++)
    {
        console.log(raw_texts[i]);
        let temp = $.trim(raw_texts[i]);
        if(temp != "")
        {
            name = temp;
        }
    }

    return name;
}






