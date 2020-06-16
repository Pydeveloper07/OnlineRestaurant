$(document).ready(function(){
    $('.order-btn').each(function(){
        $(this).click(function(){
            var foodName = $(this).closest('.item').attr('data-foodName');
            var foodId = $(this).closest('.item').attr('data-foodId');
            var quantity = $(this).closest('.item').find('input.quantity').val();
            sessionStorage.setItem(foodId, quantity);
            console.log(sessionStorage.getItem(foodId));
            $.ajax({
                type: "POST",
                url: "url",
                data: {
                    'id': foodId,
                    'quantity': quantity,
                    'csrfmiddlewaretoken': '{{csrf_token}}',
                },
                dataType: 'json',
                success: function (response) {
                    addToCart(response);
                },
            });
            function addToCart(response) {
                // Add to cart logic
            }
            console.log(sessionStorage.getItem(foodId));
            
        })
    })
});