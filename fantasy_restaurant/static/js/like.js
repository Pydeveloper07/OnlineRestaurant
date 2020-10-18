$(document).on('click', '.like', function(){
    var foodId = $(this).closest('.card-body').attr('data-foodId');
    var URL = $(this).closest(".card-body").attr('data-urlLike');
    var csrfToken = $(this).closest('.card-body').attr('data-csrf');
    var element = $(this);
    $.ajax({
        type: 'POST',
        url: URL,
        dataType: 'json',
        data: {
            'foodId': foodId,
            'csrfmiddlewaretoken': csrfToken,
        },
        success: function(response){
            like(response);
        },
        error: function(){
            console.log('Internal error occurred');
        }
    });
    function like(response){
        if (response.status == 'like'){
            element.attr('data-prefix', 'fas');
        }
        else {
            element.attr('data-prefix', 'far');
        }
        element.closest('.res-container').find('.like-count').text(response.numOfLikes);
        if (response.existed){
            element.closest('.res-container').find('.dislike-count').text(response.numOfDislikes);
            element.closest('.res-container').find('.dislike').attr('data-prefix', 'far');
        }
    }
});
$(document).on('click', '.dislike', function(){
    var foodId = $(this).closest('.card-body').attr('data-foodId');
    var URL = $(this).closest(".card-body").attr('data-urlDislike');
    var csrfToken = $(this).closest('.card-body').attr('data-csrf');
    var element = $(this);
    $.ajax({
        type: 'POST',
        url: URL,
        dataType: 'json',
        data: {
            'foodId': foodId,
            'csrfmiddlewaretoken': csrfToken,
        },
        success: function(response){
            dislike(response);
        },
        error: function(){
            console.log('Internal error occurred');
        }
    });
    function dislike(response){
        if (response.status == 'dislike'){
            element.attr('data-prefix', 'fas');
        }
        else {
            element.attr('data-prefix', 'far');
        }
        element.closest('.res-container').find('.dislike-count').text(response.numOfDislikes);
        if (response.existed){
            element.closest('.res-container').find('.like-count').text(response.numOfLikes);
            element.closest('.res-container').find('.like').attr('data-prefix', 'far');
        }
    }
});