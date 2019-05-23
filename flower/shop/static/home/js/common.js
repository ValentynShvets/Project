$(document).ready(function() {

	$('.toggle__menu').click(function(){
		$('.toggle__menu').toggleClass('toggle_active');
		$('.main__menu').toggleClass('main__menu_active');
	});

	$('.search__btn').click(function(e){
		e.preventDefault();
		$('.search__field').toggleClass('search_active');
	});

	$('.filter__btn').click(function(e){
		e.preventDefault();
		$('.filter_wrap').toggleClass('filter_active');
	});

	$('.header__bot .header__tabs li a').click(function(e){
		e.preventDefault();
		$('.header__bot .header__tabs li a').removeClass('tab_active');
		$(this).addClass('tab_active');
	});

	// $('.goods__pages li a').click(function(e){
	// 	e.preventDefault();
	// 	$('.goods__pages li a').removeClass('pages_active');
	// 	$(this).addClass('pages_active');
	// });
	
	$( "#slider" ).slider({
		range: true,
		min: 0,
		max: 5000,
		values: [ 0, 5000 ],
		slide: function( event, ui ) {
			$( "#amount" ).val(ui.values[ 0 ] );
			$( "#amount1" ).val(ui.values[ 1 ] );
		}
	});

	$('.about__gallery').each(function(){
		var parent = $(this);
		var targetBox = $('.gallery__img',parent);
		var thumbs = $('.gallery__img_sm a',parent);
		thumbs.data('done',false)
		thumbs.click(function(event){
			event.preventDefault();
			if(!$(this).data('done')){
				var $img = $('<img src="'+$(this).attr('href')+'" alt="'+$(this).data('alt')+'" data-marker="'+$(this).data('marker')+'"/>');

				$img.appendTo(targetBox);
				$(this).data('done',true)
			}
			$('[data-marker]').removeClass('gallery_active');
			$('[data-marker="'+$(this).data('marker')+'"]').addClass('gallery_active')
		})
	});
	$('[data-marker]').first().click();

	

	$('.order__minus').click(function () {
		var $input = $(this).parent().find('input');
		var count = parseInt($input.val()) - 1;
		count = count < 1 ? 1 : count;
		$input.val(count);
		$input.change();
		return false;
	});
	$('.order__plus').click(function () {
		var $input = $(this).parent().find('input');
		$input.val(parseInt($input.val()) + 1);
		$input.change();
		return false;
	});

});

$(window).on("load", function(){

	$('#gallery').lightSlider({
		item: 4,
		loop: true,
		slideMove: 1,
		speed: 600,
		responsive: [
			{
				breakpoint:1100,
				settings: {
					item:3,
					slideMargin:6,
				}
			},
			{
				breakpoint:760,
				settings: {
					item:2
				}
			},
			{
				breakpoint:640,
				settings: {
					item:1
				}
			}

		]

	});
	$('#partners').lightSlider({
		item: 6,
		loop: true,
		slideMove: 1,
		speed: 600,
		responsive: [
			{
				breakpoint:1100,
				settings: {
					item:4,
					slideMargin:6,
				}
			},
			{
				breakpoint:760,
				settings: {
					item:2
				}
			},
			{
				breakpoint:640,
				settings: {
					item:1
				}
			}

		]

	});

});