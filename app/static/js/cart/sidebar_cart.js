let sidebar_cart = $('#sidebar_cart');
let cart_errupter = $('#cart_errupter');
let side_bar_close = $('#close_cart');

$(document).ready(function (){
    sidebar_cart.on('click', function (){

        console.log(sidebar_cart.attr('open_'));
        if (sidebar_cart.attr('open_') === 'not'){
            cart_errupter.prop('style','opacity: 1; transition: opacity 300ms ease 0s;');
            sidebar_cart.attr('open_',"opened");
        }
    })

    side_bar_close.on('click',function (){
        cart_errupter.prop('style', 'display:none;');
        sidebar_cart.attr('open_','not');
    })
});
