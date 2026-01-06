//===============================================================
// debounce関数
//===============================================================
function debounce(func, wait) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

//===============================================================
// メニュー関連
//===============================================================
var $menubar = $('#menubar');
var $menubarHdr = $('#menubar_hdr');

$(window).on("load resize", debounce(function() {
    if(window.innerWidth < 900) {
        $('body').addClass('small-screen').removeClass('large-screen');
        $menubar.addClass('display-none').removeClass('display-block');
        $menubarHdr.removeClass('display-none ham').addClass('display-block');
    } else {
        $('body').addClass('large-screen').removeClass('small-screen');
        $menubar.addClass('display-block').removeClass('display-none');
        $menubarHdr.removeClass('display-block').addClass('display-none');
        $('.ddmenu_parent > ul').hide();
    }
}, 10));

$(function() {
    $menubarHdr.click(function() {
        $(this).toggleClass('ham');
        if ($(this).hasClass('ham')) {
            $menubar.addClass('display-block');
        } else {
            $menubar.removeClass('display-block');
        }
    });

    $menubar.find('a[href*="#"]').click(function() {
        $menubar.removeClass('display-block');
        $menubarHdr.removeClass('ham');
    });

    $menubar.find('a[href=""]').click(function() {
        return false;
    });

    $menubar.find('li:has(ul)').addClass('ddmenu_parent');
    $('.ddmenu_parent > a').addClass('ddmenu');

    var touchStartY = 0;

    $('.ddmenu').on('touchstart', function(e) {
        touchStartY = e.originalEvent.touches[0].clientY;
    }).on('touchend', function(e) {
        var touchEndY = e.originalEvent.changedTouches[0].clientY;
        var touchDifference = touchStartY - touchEndY;
        
        if (Math.abs(touchDifference) < 10) {
            var $nextUl = $(this).next('ul');
            if ($nextUl.is(':visible')) {
                $nextUl.stop().hide();
            } else {
                $nextUl.stop().show();
            }
            $('.ddmenu').not(this).next('ul').hide();
            return false;
        }
    });

    $('.ddmenu_parent').hover(function() {
        $(this).children('ul').stop().show();
    }, function() {
        $(this).children('ul').stop().hide();
    });

    $('.ddmenu_parent ul a').click(function() {
        $('.ddmenu_parent > ul').hide();
    });
});

//===============================================================
// 小さなメニューが開いている際のみ、body要素のスクロールを禁止
//===============================================================
$(function() {
  function toggleBodyScroll() {
    if ($('#menubar_hdr').hasClass('ham') && !$('#menubar_hdr').hasClass('display-none')) {
      $('body').css({
        overflow: 'hidden',
        height: '100%'
      });
    } else {
      $('body').css({
        overflow: '',
        height: ''
      });
    }
  }

  toggleBodyScroll();

  const observer = new MutationObserver(toggleBodyScroll);
  observer.observe(document.getElementById('menubar_hdr'), { attributes: true, attributeFilter: ['class'] });
});

//===============================================================
// スムーススクロール
//===============================================================
$(function() {
    var headerHeight = $('header').outerHeight();
    var headerMargin = parseInt($('header').css("margin-top"));
    var totalHeaderHeight = headerHeight + headerMargin;
    var topButton = $('.pagetop');
    var scrollShow = 'pagetop-show';

    function smoothScroll(target) {
        var scrollTo = target === '#' ? 0 : $(target).offset().top - totalHeaderHeight;
        $('html, body').animate({scrollTop: scrollTo}, 500);
    }

    $('a[href^="#"], .pagetop').click(function(e) {
        e.preventDefault();
        var id = $(this).attr('href') || '#';
        smoothScroll(id);
    });

    $(topButton).hide();
    $(window).scroll(function() {
        if($(this).scrollTop() >= 300) {
            $(topButton).fadeIn().addClass(scrollShow);
        } else {
            $(topButton).fadeOut().removeClass(scrollShow);
        }
    });

    if(window.location.hash) {
        $('html, body').scrollTop(0);
        setTimeout(function() {
            smoothScroll(window.location.hash);
        }, 10);
    }
});

//===============================================================
// スライドショー
//===============================================================
$(function() {
        var slides = $('#mainimg .slide');
        var slideCount = slides.length;
        var currentIndex = 0;

        slides.eq(currentIndex).css('opacity', 1).addClass('active');

        setInterval(function() {
                var nextIndex = (currentIndex + 1) % slideCount;
                slides.eq(currentIndex).css('opacity', 0).removeClass('active');
                slides.eq(nextIndex).css('opacity', 1).addClass('active');
                currentIndex = nextIndex;
        }, 4000);
});

//===============================================================
// テキストのフェードイン効果
//===============================================================
$(function() {
    $('.fade-in-text').on('inview', function(event, isInView) {
        if (isInView && !$(this).data('animated')) {
            let innerHTML = '';
            const text = $(this).text();
            $(this).text('');

            for (let i = 0; i < text.length; i++) {
                innerHTML += `<span class="char" style="animation-delay: ${i * 0.2}s;">${text[i]}</span>`;
            }

            $(this).html(innerHTML).css('visibility', 'visible');
            $(this).data('animated', true);
        }
    });
});
