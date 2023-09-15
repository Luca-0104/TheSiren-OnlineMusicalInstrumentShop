$(".brand-btn").on("click",function()
{
    let brand_id = $(this).attr("brand_id");
    console.log(brand_id);
    let brand_space =$("#brandSpace_"+brand_id);
    if(brand_space.is('.followed'))
    {
        unfollow_brand(brand_id);
    }
    else
    {
        follow_brand(brand_id);
    }
});

function follow_brand(brand_id)
{
    let brand_space =$("#brandSpace_"+brand_id);

    $.post("/api/userinfo/brand-section/follow-brand",
        {
            "brand_id": brand_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    if(!brand_space.is('.followed'))
                    {
                        console.log("add");
                        brand_space.addClass('followed');
                    }
                }
                else if (returnValue === 318)
                {
                    let targetURL = response['redirectURL'];
                    window.location.href = targetURL;
                }
            });
}

function unfollow_brand(brand_id)
{
    let brand_space =$("#brandSpace_"+brand_id);

    $.post("/api/userinfo/brand-section/unfollow-brand",
        {
            "brand_id": brand_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    if(brand_space.is('.followed'))
                    {
                        console.log("remove");
                        brand_space.removeClass('followed');
                    }
                }
                else if (returnValue === 318)
                {
                    let targetURL = response['redirectURL'];
                    window.location.href = targetURL;
                }
            });
}