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

    let selected_jurisdiction;
    $('.jurisdiction-option').on('click', function (event){
        window.selected_jursidiction = $(event.currentTarget).children()[0].innerText;
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/browsing',
            headers: {'X-CSRFToken': csrftoken},
            data: {'jurisdiction': selected_jursidiction},
            success: function (resp) {
                let tags_list = document.getElementById("law-tags");
                const tags_list_title = tags_list.firstElementChild;
                while(tags_list.hasChildNodes()) {tags_list.removeChild(tags_list.lastChild);}
                tags_list.appendChild(tags_list_title);
                const law_type_tags = resp["law_type_tags"];
                if (law_type_tags.length < 1){
                    let tag_li = document.createElement("LI");
                    tag_li.classList.add("list-group-item");
                    let tags_not_found = document.createTextNode("No Result Found Please choose some other jurisdiction!");
                    tags_list.appendChild(tags_not_found);
                }
                else {
                    law_type_tags.forEach((tag) => {
                        let tag_li = document.createElement("LI");
                        tag_li.classList.add("list-group-item");
                        tag_li.classList.add("browsing-li");
                        tag_li.classList.add("tag-option");
                        let tag_title = document.createElement("DIV");
                        let tag_navigator = document.createElement("DIV");
                        let profiles_count = document.createElement("DIV");
                        tag_title.textContent = tag.name;
                        profiles_count.textContent = ' (' + tag.number_profile + ')';
                        tag_navigator.textContent = ">";
                        tag_li.appendChild(tag_title);
                        tag_li.appendChild(profiles_count);
                        tag_li.appendChild(tag_navigator);

                        tag_li.addEventListener('click', lawTypeTagClickListener);
                        tags_list.appendChild(tag_li);
                    });
                }
            }
        });
    });

    function lawTypeTagClickListener(){
        let selected_tag = $(event.currentTarget).children()[0].innerText;
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/browsing',
            headers: {'X-CSRFToken': csrftoken},
            data: {'jurisdiction': selected_jursidiction, 'law_type_tag': selected_tag},
            success: function (resp) {
                let resultProfilesList = document.getElementById("result-profiles");
                const resultProfilesTitle = resultProfilesList.firstElementChild;
                while(resultProfilesList.hasChildNodes()) {resultProfilesList.removeChild(resultProfilesList.lastChild);}
                resultProfilesList.appendChild(resultProfilesTitle);
                const profilesList = resp["result_profiles"];
                if (profilesList.length < 1){
                    let profile_not_found = document.createTextNode("No Result Found Please choose some other law type tag!");
                    resultProfilesList.appendChild(profile_not_found);
                }
                else {
                    profilesList.forEach((profile) => {
                        // profile LI
                        let profile_li = document.createElement("LI");
                        profile_li.classList.add("list-group-item");
                        profile_li.classList.add("browsing-li");
                        profile_li.classList.add("tag-option");

                        // profile link
                        let profile_link = document.createElement("a");
                        profile_link.href = "/profile/" + profile.handle;

                        // profile row
                        let profile_row = document.createElement("DIV");
                        profile_row.style.display = "flex";
                        profile_row.style.alignItems = "center";
                        profile_row.style.justifyContent = "space-between";

                        // photo
                        let photo_col = document.createElement("DIV");
                        let photo = document.createElement("IMG");
                        photo.classList.add("d-block");
                        photo.classList.add("card--user__avatar");
                        photo.classList.add("rounded-circle");
                        photo.src = profile.photo_url_or_default;
                        photo_col.appendChild(photo);

                        // details
                        let detail_col = document.createElement("DIV");
                        let name_div = document.createElement("DIV");
                        let name = document.createElement('b');
                        name.textContent = (profile.first_name + " " + profile.last_name);
                        name_div.appendChild(name);

                        let headline = document.createElement("DIV");
                        headline.textContent = profile.headline;

                        detail_col.appendChild(name_div);
                        detail_col.appendChild(headline);

                        // assemble together
                        profile_row.appendChild(photo_col);
                        profile_row.appendChild(detail_col);

                        profile_link.appendChild(profile_row);
                        profile_li.appendChild(profile_link);
                        resultProfilesList.appendChild(profile_li);
                    });
                }
            }
        });
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
});