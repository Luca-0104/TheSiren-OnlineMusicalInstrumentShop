let checked_value = new Array(4);
checked_value = ['', '', '', ''];

let classification, type, additional, brand;

let data;
//This need to be modified if brand number is changed!!!
//Every number is plus one compared to original because "see all" option.
let checking_numbers = [7, 48, 5, 6];

function initialize_checkbox(param) {
    let p = 0;
    if (param === "#check_class_") {
        p = 0;
    } else if (param === "#check_type_") {
        p = 1;
    } else if (param === "#check_add_") {
        p = 2;
    } else if (param === "#check_brand_") {
        p = 3;
    }
    for (let i = 1; i <= checking_numbers[p]; i++) {
        let init_select = $(param + i);
        init_select.click();
    }
}

$(document).ready(function () {

    initialize_checkbox("#check_class_");
    initialize_checkbox("#check_type_");
    initialize_checkbox("#check_add_");
    initialize_checkbox("#check_brand_");

    $('.category').on("change", function () {
        console.log($(this).attr('id'));

        console.log($(this).attr("checked"));
        let p = $(this).attr('id').split('_').pop();
        console.log(p);

        if (!$(this).prop('checked')) {

            for (let i = 1; i <= checking_numbers[0]; i++) {
                if (p !== i) {
                    let cancel_select = $('#check_class_' + i);
                    cancel_select.attr("class", "checkbox category");
                    cancel_select.prop("checked", "off");

                }
            }
            $(this).attr("class", "checkbox w--redirected-checked category");
            $(this).prop("checked", "on");

            checked_value[0] = $(this).attr("name");

            classification = checked_value[0];
            console.log($(this).attr("checked") + '2');
            console.log(checked_value);
        }
    });

    $('.type').on("change", function () {
        console.log($(this).attr('id'));

        console.log($(this).attr("checked"));
        let p = $(this).attr('id').split('_').pop();
        console.log(p);

        if (!$(this).prop('checked')) {

            for (let i = 1; i <= checking_numbers[1]; i++) {
                if (p !== i) {
                    let cancel_select = $('#check_type_' + i);
                    cancel_select.attr("class", "checkbox type");
                    cancel_select.prop("checked", "off");
                }
            }
            $(this).attr("class", "checkbox w--redirected-checked type");
            $(this).prop("checked", "on");

            checked_value[1] = $(this).attr("name");

            type = checked_value[1];
            console.log($(this).attr("checked") + '2');
            console.log(checked_value);
        }
    });


    $('.add').on("change", function () {
        console.log($(this).attr('id'));

        console.log($(this).attr("checked"));
        let p = $(this).attr('id').split('_').pop();
        console.log(p);

        if (!$(this).prop('checked')) {

            for (let i = 1; i <= checking_numbers[2]; i++) {
                if (p !== i) {
                    let cancel_select = $('#check_add_' + i);
                    cancel_select.attr("class", "checkbox add");
                    cancel_select.prop("checked", "off");
                }
            }
            $(this).attr("class", "checkbox w--redirected-checked add");
            $(this).prop("checked", "on");

            checked_value[2] = $(this).attr("name");

            additional = checked_value[2];
            console.log($(this).attr("checked") + '2');
            console.log(checked_value);
        }
    });

    $('.brands').on("change", function () {
        console.log($(this).attr('id'));

        console.log($(this).attr("checked"));
        let p = $(this).attr('id').split('_').pop();
        console.log(p);

        if (!$(this).prop('checked')) {

            for (let i = 1; i <= checking_numbers[3]; i++) {
                if (p !== i) {
                    let cancel_select = $('#check_brand_' + i);
                    cancel_select.attr("class", "checkbox brand");
                    cancel_select.prop("checked", "off");
                }
            }
            $(this).attr("class", "checkbox w--redirected-checked brand");
            $(this).prop("checked", "on");

            checked_value[3] = $(this).attr("name");

            brand = checked_value[3];
            console.log($(this).attr("checked") + '2');
            console.log(checked_value);
        }
    });


    $('#category_checkbox').on("change", function () {
        //get the search content
        //we need to sent it back to server to search again before filtering
        let searchContent = $("#search").val();

        $.post("/api/filter-model-types",
            {
                "c": classification,
                "t": type,
                "a": additional,
                "b": brand,
                "search_content": searchContent

            }).done(function (response) {
            // get from server
            let returnValue = response['returnValue'];

            if (returnValue === 0) {
                //success
                data = response['data'];
                console.log("data below")
                console.log(data)
                //clear all the model card on this page
                $("#model-list").empty();
                //put model data on the product card in this page
                $.each(data, function(){
                    put_data(this);
                });

            } else if (returnValue === 1) {
                //failure

            }
        });
    })

    $("input[name='checkboxes']:checked").each(function () {
        checked_value = [];
        checked_value.push($(this).val());
        console.log(checked_value);
    });

});

/**
 * This function is for putting the model data on the product card in this page
 * @param mt mt refers to "model type", each one should be a dict
 */
function put_data(mt){
    //get basic info of this model type
    let mtID = mt.id;
    let mtName = mt.name;
    let mtPrice = mt.price;
    let brandName = mt.brand_name;
    let firstPicAddress = mt.pictures[0].address;

    //put those info on to model card
    let cardHTML = '<div role="listitem" class="w-dyn-item">'
                        + '<div>'
                            + '<a href="/product-details/' + mtID + '" class="product-preview-link w-inline-block">'
                                + '<img src="../../static/' + firstPicAddress + '"loading="lazy" alt="" class="product-thumbnail">'
                                + '<div class="uppercase-text brand">' + brandName + '</div>'
                                + '<h5 class="no-bottom-margin">' + mtName + '</h5>'
                                + '<div class="price-container">'
                                    + '<div class="old-price"><span>$</span>' + mtPrice + '</div>'
                                    + '<div><span>$</span>' + mtPrice + '</div>'
                                + '</div>'
                            + '</a>'
                        + '</div>'
                    + '</div>';

    $("#model-list").append(cardHTML);
}








