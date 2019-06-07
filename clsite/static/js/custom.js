$(document).ready(function() {
    function setupPictureUpload() {
        if (window.location.href.split("profile")[1] === ""){
            document.getElementsByClassName("photo-view")[0].style.cursor = "pointer";
            //Upload picture code
            $('.photo-view').click(function (event) {
                $('.photo-input').trigger('click');
            });

            $('.photo-input').change(function () {
                var image_size = this.files[0].size;
                if (image_size > 8000000) {
                    //Image is too big, must be 8MB or less
                    alert('Your picture is too big, please make sure the image is 8 MB or less in size.');
                } else {
                    $('.photo-form').submit();
                }
            });

            $('.photo-form').on('submit', function (event) {
                event.preventDefault();

                var picture = $('.photo-view');

                //Grab the current picture src
                var original_src = picture.attr('src');

                //Set the
                picture.attr('src', 'static/images/loading.gif');

                $.ajax({
                    type: 'POST',
                    url: '/profile',
                    data: new FormData(this),
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function (resp) {
                        if (resp['url']) {
                            $('.photo-view').attr('src', resp['url']);
                        } else {
                            alert(resp['msg']);
                            //Set the original picture back
                            picture.attr('src', original_src);
                        }
                    }
                });

            });
        }
    }

    setupPictureUpload();
});