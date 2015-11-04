/*Theme    : assan
 * Author  : Design_mylife
 * Version : V1.8
 * 
 */

 //$( window ).resize(function() {
    //$(".navbar-collapse").css({ maxHeight: $(window).height() - $(".navbar-header").height() + "px" });
//});
//sticky header on scroll
//$(document).ready(function () {
    //$(window).load(function () {
        //$(".sticky").sticky({topSpacing: 0});
    //});
//});

/* ==============================================
 WOW plugin triggers animate.css on scroll
 =============================================== */

//owl carousel for testimonials
$(document).ready(function () {

    $("#testi-carousel").owlCarousel({
        // Most important owl features
        items: 1,
        itemsCustom: false,
        itemsDesktop: [1199, 1],
        itemsDesktopSmall: [980, 1],
        itemsTablet: [768, 1],
        itemsTabletSmall: false,
        itemsMobile: [479, 1],
        singleItem: false,
        startDragging: true,
        autoPlay: 4000
    });

});



