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
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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
        browsingPostAPI(event, 'jurisdiction')
    });

    $('.law-type-tag').on('click', function(event){
        browsingPostAPI(event, 'law_type_tag')
    });

    function browsingPostAPI(event, key){
        let value = $(event.currentTarget).children()[0].innerText;
        // clear user cards
        let userCards = document.getElementsByClassName("card-deck")[0];
        while(userCards.hasChildNodes()) {userCards.removeChild(userCards.lastChild);}

        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/users',
            headers: {'X-CSRFToken': csrftoken},
            data: {[key]: value},
            success: function (resp) {
                const users = resp["users"];
                if (users.length > 0){
                    users.forEach((user) => {
                        // card
                        let card = document.createElement("DIV");
                        card.classList.add("card");
                        card.classList.add("card--user");

                        // card body
                        let cardBody = document.createElement("DIV");
                        cardBody.classList.add("card-body");

                        let profile_link = document.createElement("a");
                        profile_link.href = "/profile/" + user.handle;


                        let photo = document.createElement("IMG");
                        photo.classList.add("d-block");
                        photo.classList.add("mx-auto");
                        photo.classList.add("card--user__avatar");
                        photo.classList.add("rounded-circle");
                        photo.src = user.photo_url_or_default;

                        let name = document.createElement("h5");
                        name.classList.add("card-title");
                        name.classList.add("text-center");
                        name.classList.add("my-0");
                        name.textContent = user.first_name + " " + user.last_name;

                        let jurisdiction = document.createElement("h6");
                        jurisdiction.classList.add("my-0");
                        jurisdiction.classList.add("text-center");
                        jurisdiction.textContent = user.jurisdiction;

                        let headline = document.createElement("p");
                        headline.textContent = user.headline;

                        profile_link.appendChild(photo);
                        profile_link.appendChild(name);
                        profile_link.appendChild(jurisdiction);
                        profile_link.appendChild(headline);

                        cardBody.appendChild(profile_link);
                        // card footer
                        let cardFooter = document.createElement("DIV");
                        cardFooter.classList.add("card-footer");

                        let footerText = document.createElement('small');
                        footerText.textContent = user.date_joined;

                        cardFooter.appendChild(footerText);

                        // wrap up
                        card.appendChild(cardBody);
                        card.appendChild(cardFooter);

                        userCards.appendChild(card);

                    });
                }
            }
        });
    }
});