$(document).ready(function() {
    function setupPictureUpload() {
        if (window.location.href.split("profile")[1] === ""){
            document.getElementsByClassName("photo-view")[0].style.cursor = "pointer";
            //Upload picture code
            $('.photo-view').click(function (event) {
                $('.photo-input').trigger('click');
            });

            $('.photo-input').change(function () {
                img_file = this.files[0]
                var img = new Image();
                img.src = window.URL.createObjectURL(img_file);
                img.onload = function() {
                    var width = img.naturalWidth;
                    var height = img.naturalHeight;
                    window.URL.revokeObjectURL( img.src );

                    if( Math.max(width, height) / Math.min(width, height) < 1.2 ) {
                        var image_size = img_file.size;
                        if (image_size > 8000000) {
                            //Image is too big, must be 8MB or less
                            alert('Your photo is too big, please make sure the image is 8 MB or less in size.');
                        } else {
                            $('.photo-form').submit();
                        }
                    }
                    else {
                        //Image is too big, must be 8MB or less
                        alert('Please make sure the photo is square.');
                    }
                };
            });

            $('.photo-form').on('submit', function (event) {
                event.preventDefault();

                var picture = $('.photo-view');

                //Grab the current picture src
                var original_src = picture.attr('src');

                //Set the
                picture.attr('src', 'static/img/loader.gif');

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
                            $('.navbar-photo').attr('src', resp['url']);
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