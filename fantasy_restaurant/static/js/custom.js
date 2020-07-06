$(document).ready(function(){
    var wow = new WOW();
    wow.init();
    $('#alertPanel').delay(5000).fadeOut(1000);
    // index.html js
    try {
        var form = $('#tableOrderForm');
		form.find('select').on('change', function() {
            document.getElementById('tableHelp').innerHTML = null;
            var tableId = form.find('select').val();
			$.ajax({
                type: "POST",
                url: form.attr('data-url'),
                data: {
                    'tableId': tableId,
                    'csrfmiddlewaretoken': form.attr('data-csrf'),
                },
                dataType: 'json',
                success: function (response) {
                    giveTableInfo(response);
                },
                error: function(){
                    console.log('Internal Error Occurred');
                }
			});
			function giveTableInfo(response){
                var infoCont = $('#tableHelp');
                if (response.is_busy){
                    infoCont.append("<span>Table is busy:</span>");
                    for (var i = 0; i < response.time_list.length; i++) {
                        var child = "<span>" + response.time_list[i].start_time + '-' + response.time_list[i].end_time + "</span>";
                        infoCont.append(child);
                    }
                }
                else{
                    infoCont.append("<span class='text-success'>Table is not busy today!</span>");
                }
            }
        });
        form.find('#numberOfPeople').on('change', function(){
            if ($('#tables').val()){
                var url = $(this).attr('data-url');
                var csrf_token = $('#tableOrderForm').attr('data-csrf');
                var tableId = $('#tables').val();
                var errMessageCont = $(this).siblings('.err-message');
                var numOfPeople = $(this).val();
                $.ajax({
                    type: 'POST',
                    url: url,
                    dataType: 'json',
                    data: {
                        'tableId': tableId,
                        'numOfPeople': numOfPeople,
                        'csrfmiddlewaretoken': csrf_token
                    },
                    success: function (response) {
                        if (response.error) {
                            errMessageCont.text(response.message);
                        }
                        else{
                            errMessageCont.text('');
                        }
                    },
                    error: function () {
                        console.log('Internal Error Occurred');
                    }
                });
            }
        });
        form.find('#reserveStartTime, #reserveEndTime').on('change', function(){
            if ($('#reserveStartTime').val() && $('#reserveEndTime').val() && $('#tables').val()){
                var url = $('#reserveEndTime').attr('data-url');
                var csrf_token = $('#tableOrderForm').attr('data-csrf');
                var messageCont = $('#reserveTimeMessage');
                var tableId = $('#tables').val();
                var startTime = $('#reserveStartTime').val();
                var endTime = $('#reserveEndTime').val();
                $.ajax({
                    type: 'POST',
                    url: url,
                    dataType: 'json',
                    data: {
                        'tableId': tableId,
                        'startTime': startTime,
                        'endTime': endTime,
                        'csrfmiddlewaretoken': csrf_token
                    },
                    success: function(response){
                        if (response.error){
                            messageCont.attr('class', 'text-danger');
                            messageCont.text(response.message);
                        }
                        else{
                            messageCont.attr('class', 'font-weight-bold text-warning');
                            messageCont.text(response.message);
                        }
                    },
                    error: function(){
                        console.log('Internal Error Occurred');
                    }
                });
            }
        });
        form.find('button[type="submit"]').on('click', function(event){
            event.preventDefault();
            if ($('#tables').val() && form.find('input[name="num_of_people"]').val() && $('#reserveStartTime').val() && $('#reserveEndTime').val()){
                form.submit();
            }
        });
        $('#editReviewBtn').click(function(){
            $('#reviewStatus').val('updating');
        });
        $('#leaveReviewBtn').click(function () {
            $('#reviewStatus').val('new');
        });
        $('#reviewForm button[type="submit"]').click(function (event) {
            event.preventDefault();
            var reviewContent = $.trim($('#reviewContent').val());
            if ($('#rating').val() && (reviewContent != '')) {
                $('#reviewForm').submit();
            }
            else {
                if (!$('#rating').val()) {
                    $('#rateError').fadeIn();
                }
                else {
                    $('#rateError').fadeOut();
                }
                if (reviewContent != '') {
                    $('#reviewContentError').fadeIn();
                }
                else {
                    $('#reviewContentError').fadeOut();
                }
            }
        });
		$(document).on('click', '.star', function(){
			 $('#rating').val($(this).attr('data-value'));
			 value = $(this).attr('data-value');
			 $(this).siblings('.star').each(function(){
				 if ($(this).attr('data-value') <= value){
					$(this).css({'color':'yellow'});
				 }
				 else{
					 $(this).css({'color':'black'});
				 }
			 });
			 $(this).css({'color': 'yellow'}); 
			 elem = $('#rate-emoji');
			 switch(value){
				 case '1': elem.attr('class', 'ec ec-confounded'); break;
				 case '2': elem.attr('class', 'ec ec-expressionless'); break;
				 case '3': elem.attr('class', 'ec ec-blush'); break;
				 case '4': elem.attr('class', 'ec ec-yum'); break;
				 case '5': elem.attr('class', 'ec ec-heart-eyes'); break;
				 default: elem.attr('class', '');
			 }
        });
        var owl = $('.owl-carousel-discount');
        owl.owlCarousel({
            items: 3,
            loop: true,
            margin: 10,
            /*autoplay: false,
            autoplayTimeout: 2000,
            autoplayHoverPause: true,*/
            responsiveClass: true,
            nav: false,
            autoHeight: true,
            responsive: {
                0: {
                    items: 1,
                    nav: false
                },
                600: {
                    items: 2,
                    nav: false
                },
                1000: {
                    items: 3,
                    nav: false,
                }
            }
        });
    } catch (error) {}
    // menu.html js
    try {
        var wow = new WOW();
        wow.init();
        $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            if (scroll > 10) {
                $('.custom-nav').addClass('wow fadeInDown');
            }
        });
        var owl1 = $('.owl-carousel-cuisine');
        var owl2 = $('.owl-carousel-type');
        owl1.owlCarousel({
            items: 4,
            loop: false,
            margin:10,
            responsiveClass:true,
            nav: false,
            autoHeight: true,
            responsive:{
                0:{
                    items:1,
                    nav:false
                },
                600:{
                    items:2,
                    nav:false
                },
                    1000:{
                    items:4,
                    nav:false,
                }
            }
        });
        owl2.owlCarousel({
            items: 4,
            loop: false,
            margin: 10,
            responsiveClass: true,
            nav: false,
            autoHeight: true,
            responsive: {
                0: {
                    items: 1,
                    nav: false
                },
                600: {
                    items: 2,
                    nav: false
                },
                1000: {
                    items: 4,
                    nav: false,
                }
            }
        });
    } catch (error) {}
});

$(window).resize(function(){
    try {
        var width = $('.card .image-container').css('width');
        $('.card .image-container').css({'height': width});
    } catch (error) {}
});
try {
    $('.section-cuisine .cuisine .overlay').each(function(){
        $(this).mouseover(function(){
            $(this).css({
                'opacity': '1',
            })
        });
    });
    $('.section-cuisine .cuisine .overlay').each(function () {
        $(this).mouseout(function () {
            $(this).css({
                'opacity': '0',
            })
        });
    });
} catch (error) {}
