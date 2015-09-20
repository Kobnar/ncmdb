// NOTE: This code draws heavily from Udacity's "freshtomatoes.py", available
//  through their Full Stack Web Developer Nanodegree.

$(document).ready(function() {
    var $lightbox = $('#lightbox');

    // Empty the video container when user clicks anywhere but the modal:
    $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
        $("#trailerVideoContainer").empty();
    });

    // Create a new <iframe>
    $('[data-target="#lightbox"]').on('click', function(event) {
        var $link = $(this),
            sourceUrl = $link.attr('href'),
            maxSizes = {
                'width': "100%",
                'maxWidth': $(window).width() - 100,
                'maxHeight': $(window).height() - 100
            };

        $('#trailerVideoContainer').empty().append($("<iframe></iframe>", {
            'id': 'trailer-video',
            'type': 'text-html',
            'src': sourceUrl,
            'class': 'embed-responsive-item',
            'css': maxSizes,
            'frameborder': 0
        }));
    });
});