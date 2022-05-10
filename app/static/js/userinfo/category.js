$(".category-btn").on("click",function()
{
    let category_id = $(this).attr("category_id");
    console.log(category_id);
    let category_space =$("#categorySpace_"+category_id);
    if(category_space.is('.followed'))
    {
        unfollow_category(category_id);
    }
    else
    {
        follow_category(category_id);
    }
});

function follow_category(category_id)
{
    let category_space =$("#categorySpace_"+category_id);

    $.post("/api/userinfo/category-section/follow-category",
        {
            "category_id": category_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    if(!category_space.is('.followed'))
                    {
                        console.log("add");
                        category_space.addClass('followed');
                    }
                }
                else if (returnValue === 318)
                {
                    let targetURL = response['redirectURL'];
                    window.location.href = targetURL;
                }
            });
}

function unfollow_category(category_id)
{
    let category_space =$("#categorySpace_"+category_id);

    $.post("/api/userinfo/brand-section/unfollow-category",
        {
            "category_id": category_id
        }).done(function (response)
            {
                // get from server (backend)
                let returnValue = response['returnValue'];

                if(returnValue === 0)
                {
                    //success
                    if(category_space.is('.followed'))
                    {
                        console.log("remove");
                        category_space.removeClass('followed');
                    }
                }
                else if (returnValue === 318)
                {
                    let targetURL = response['redirectURL'];
                    window.location.href = targetURL;
                }
            });
}