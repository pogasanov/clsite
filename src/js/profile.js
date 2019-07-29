require("jquery-ui/ui/widgets/datepicker");
import LoaderSpinner from '../img/loader.gif'

$(document).ready(function () {
    setupPictureUpload();

    $('.profile-form').on('submit', function (event) {
        event.preventDefault();
        let errorsDetailDiv = document.getElementById("response-details");
        while (errorsDetailDiv.hasChildNodes()) {
            errorsDetailDiv.removeChild(errorsDetailDiv.lastChild);
        }
        $.ajax({
            type: 'POST',
            url: '/profile',
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function (resp) {
                document.getElementById("response-message").textContent = resp["message"];
            },
            error: function (resp) {
                for (let key in resp["responseJSON"]) {
                    if (resp["responseJSON"][key] !== undefined) {
                        if (Array.isArray(resp["responseJSON"][key])) {
                            if (resp["responseJSON"][key].length !== 0 && Object.keys(resp["responseJSON"][key][0]).length !== 0) {
                                appendToErrorDetail(errorsDetailDiv, key, JSON.stringify(resp["responseJSON"][key][0]));
                            }
                        } else if (typeof resp["responseJSON"][key] === 'object' && resp["responseJSON"][key] !== null) {
                            if (Object.keys(resp["responseJSON"][key]).length !== 0) {
                                for (let errorTitle in resp["responseJSON"][key]) {
                                    appendToErrorDetail(errorsDetailDiv, errorTitle, resp["responseJSON"][key][errorTitle]);
                                }
                            }
                        }
                    }
                }
                document.getElementById("response-message").textContent = resp["message"];
            }
        });
    });

    $('.country').on('change', function (e) {
        let stateDiv = $(e.currentTarget).parent().siblings('.state-div')[0];
        let stateDropdown = $(stateDiv).children('select')[0];
        let countryName = $(e.currentTarget).children("option").filter(":selected").text();
        let csrfToken = getCookie('csrftoken');
        while (stateDropdown.hasChildNodes()) {
            stateDropdown.removeChild(stateDropdown.lastChild);
        }
        $.ajax({
            type: 'POST',
            url: '/states',
            headers: {'X-CSRFToken': csrfToken},
            data: {'country': countryName},
            success: function (resp) {
                resp['data'].forEach(value => {
                    $(stateDropdown).append('<option value="' + value[0] + '">' + value[1] + '</option>');
                });
            }
        });
    });

    $('#jurisdiction-clone').on('click', function (event) {
        event.preventDefault();
        let form_idx = $('#id_jurisdiction-TOTAL_FORMS').val();
        $('#jurisdiction-formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_jurisdiction-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
})

function setupPictureUpload() {
    if (window.location.href.split("profile")[1] === "") {
        document.getElementsByClassName("photo-view")[0].style.cursor = "pointer";
        //Upload picture code
        $('.photo-view').click(function (event) {
            $('.photo-input').trigger('click');
        });

        $('.photo-input').change(function () {
            let img_file = this.files[0]
            let valid_image_extensions = ["image/jpeg", "image/png"];
            if (valid_image_extensions.indexOf(img_file.type) > -1) {
                let img = new Image();
                img.src = window.URL.createObjectURL(img_file);
                img.onload = function () {
                    let width = img.naturalWidth;
                    let height = img.naturalHeight;
                    window.URL.revokeObjectURL(img.src);

                    if (Math.max(width, height) / Math.min(width, height) < 1.2) {
                        let image_size = img_file.size;
                        if (image_size > 8000000) {
                            //Image is too big, must be 8MB or less
                            alert('Your photo is too big, please make sure the image is 8 MB or less in size.');
                        } else if (Math.max(width, height) < 300) {
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

            let picture = $('.photo-view');

            //Grab the current picture src
            let original_src = picture.attr('src');

            //Set the
            picture.attr('src', LoaderSpinner);

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

function appendToErrorDetail(errorDiv, errorTitle, errorDescription) {
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