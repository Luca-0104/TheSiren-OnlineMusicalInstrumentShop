$(document).ready(function ()
{
    let sidebar_anchor = $("#sidebar-anchor").attr("sidebar-anchor");
    console.log(sidebar_anchor);
    $(".sidebar-selection").removeClass("active");
    let target_sidebar = $("#sidebar-"+sidebar_anchor);
    let super_sidebar_anchor = target_sidebar.attr("super-selection");
    let super_sidebar = $("#"+super_sidebar_anchor);
    target_sidebar.addClass("active");
    target_sidebar.parent().addClass("show");
    super_sidebar.addClass("active");
    super_sidebar.children("a").attr("aria-expanded",true);
});