function CopyText(text) {
    navigator.clipboard.writeText(text);
}

function MoveCarouselTo(c, pos) {
    var myCarousel = document.querySelector(c)
    var carousel = new bootstrap.Carousel(myCarousel)
    carousel.to(pos, {
        interval: false
    })
}
