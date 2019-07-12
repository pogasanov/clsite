import LoaderSpinner from '../img/loader.gif'

$(document).ready(function() {
    function setupPictureUpload() {
        if (window.location.href.split("profile")[1] === ""){
            document.getElementsByClassName("photo-view")[0].style.cursor = "pointer";
            //Upload picture code
            $('.photo-view').click(function (event) {
                $('.photo-input').trigger('click');
            });

            $('.photo-input').change(function () {
                var img_file = this.files[0]
                var valid_image_extensions = ["image/jpeg", "image/png"];
                if(valid_image_extensions.indexOf(img_file.type) > -1){
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
                            } else if(Math.max(width, height) < 300) {
                                alert('Your photo dimension is insufficient, please make sure that it is atleast 300 X 300 in pixels.');
                            } else {
                                $('.photo-form').submit();
                            }
                        } else {
                            //Image is too big, must be 8MB or less
                            alert('Please make sure the photo is square.');
                        }
                        $('.photo-input')[0].value = '';
                    };
                } else {
                    alert('invalid file format, please use JPEG/PNG format only.');
                }
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

    function appendToErrorDetail(errorDiv, errorTitle, errorDescription){
        let errorTitleDiv = document.createElement("div");
        let errorDescriptionDiv = document.createElement("div");
        errorTitleDiv.classList.add('col-md-3');
        errorDescriptionDiv.classList.add('col-md-9');
        errorTitleDiv.innerText = "[" + errorTitle + "]";
        errorTitleDiv.style.color = "red";
        errorDescriptionDiv.innerText = errorDescription;
        errorDiv.appendChild(errorTitleDiv);
        errorDiv.appendChild(errorDescriptionDiv);
    }

    $('.profile-form').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/profile',
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function (resp) {
                document.getElementById("response-message").textContent= resp["message"];
            },
            error: function(resp) {
                let errorsDetailDiv = document.getElementById("response-details");
                while(errorsDetailDiv.hasChildNodes()) {errorsDetailDiv.removeChild(errorsDetailDiv.lastChild);}
                for(let key in resp["responseJSON"]){
                    if(resp["responseJSON"][key] !== undefined){
                        if(Object.prototype.toString.call(resp["responseJSON"][key]) == "[object Array]"){
                            if(resp["responseJSON"][key].length !== 0 && Object.keys(resp["responseJSON"][key][0]).length !== 0){
                                appendToErrorDetail(errorsDetailDiv, key, JSON.stringify(resp["responseJSON"][key][0]));
                            }
                        }else if(Object.prototype.toString.call(resp["responseJSON"][key]) == "[object Object]"){
                            if(Object.keys(resp["responseJSON"][key]).length !== 0){
                                for(let errorTitle in resp["responseJSON"][key]){
                                    appendToErrorDetail(errorsDetailDiv, errorTitle, resp["responseJSON"][key][errorTitle]);
                                }
                            }
                        }
                    }
                }
                document.getElementById("response-message").textContent= resp["message"];
            }
        });
    });

    setupPictureUpload();

    $('.jurisdiction-display').on('click', function (event){
        // toggle active class
        event.currentTarget.classList.add('active');
        $('.law-type-tag-display')[0].classList.remove('active');
        // toggle selection options
        $('#jurisdictions-row').show();
        $('#law-type-tag-row').hide();
    });

    $('.law-type-tag-display').on('click', function (event){
        // toggle active class
        event.currentTarget.classList.add('active');
        $('.jurisdiction-display')[0].classList.remove('active');
        // toggle selection options
        $('#law-type-tag-row').show();
        $('#jurisdictions-row').hide();
    });

    $('.jurisdiction').on('click', function(event){
        window.location.href= '/profiles/jurisdictions/'+ $(event.currentTarget).children()[0].innerText + '/law-type-tags/all';
    });

    $('.law-type-tag').on('click', function(event){
        window.location.href= '/profiles/jurisdictions/all/law-type-tags/' + $(event.currentTarget).children()[0].innerText;
    });

    $('#navigate-back').on('click', function(event){
        window.history.back();
        return false;
    });

});