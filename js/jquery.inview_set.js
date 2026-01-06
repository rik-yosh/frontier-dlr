/**
 * jQuery.inview Plugin
 */
$(function() {
    $('.up, .down, .blur, .transform1, .transform2, .transform3').on('inview', function(event, isInView) {
        if (isInView) {
            if ($(this).hasClass('up')) {
                $(this).addClass('upstyle');
            } else if ($(this).hasClass('down')) {
                $(this).addClass('downstyle');
            } else if ($(this).hasClass('blur')) {
                $(this).addClass('blurstyle');
            } else if ($(this).hasClass('transform1')) {
                $(this).addClass('transform1style');
            } else if ($(this).hasClass('transform2')) {
                $(this).addClass('transform2style');
            } else if ($(this).hasClass('transform3')) {
                $(this).addClass('transform3style');
            }
        }
    });
});
