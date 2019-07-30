import LoaderSpinner from '../img/loader.gif'
require("jquery-ui/ui/widgets/datepicker");

$(document).ready(function () {
    // PROFILE PAGE
    function setupPictureUpload() {
        if (window.location.href.split("profile")[1] === "") {
            document.getElementsByClassName("photo-view")[0].style.cursor = "pointer";
            //Upload picture code
            $('.photo-view').click(function (event) {
                $('.photo-input').trigger('click');
            });

            $('.photo-input').change(function () {
                var img_file = this.files[0]
                var valid_image_extensions = ["image/jpeg", "image/png"];
                if (valid_image_extensions.indexOf(img_file.type) > -1) {
                    var img = new Image();
                    img.src = window.URL.createObjectURL(img_file);
                    img.onload = function () {
                        var width = img.naturalWidth;
                        var height = img.naturalHeight;
                        window.URL.revokeObjectURL(img.src);

                        if (Math.max(width, height) / Math.min(width, height) < 1.2) {
                            var image_size = img_file.size;
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

    $('.profile-form').on('submit', function (event) {
        event.preventDefault();
        let errorsDetailDiv = document.getElementById("response-details");
        while(errorsDetailDiv.hasChildNodes()) {errorsDetailDiv.removeChild(errorsDetailDiv.lastChild);}
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
            error: function(resp) {
                for(let key in resp["responseJSON"]){
                    if(resp["responseJSON"][key] !== undefined){
                        if(Array.isArray(resp["responseJSON"][key])){
                            if(resp["responseJSON"][key].length !== 0 && Object.keys(resp["responseJSON"][key][0]).length !== 0){
                                appendToErrorDetail(errorsDetailDiv, key, JSON.stringify(resp["responseJSON"][key][0]));
                            }
                        }else if(typeof resp["responseJSON"][key] === 'object' && resp["responseJSON"][key] !== null ){
                            if(Object.keys(resp["responseJSON"][key]).length !== 0){
                                for(let errorTitle in resp["responseJSON"][key]){
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

    setupPictureUpload();

    function setDatePicker() {
        $(".datepicker").datepicker({
            changeMonth: true,
            changeYear: true,
            maxDate: 0,
            showAnim: 'slideDown'
        });
    }

    setDatePicker();
    
    const recommendationFieldSelector = '#id_requester_recommendation, #id_requestee_recommendation';
    const recommendationLabelSelector = '[for="id_requester_recommendation"], [for="id_requestee_recommendation"]';
    const confirmTransactionSelector = '.confirm-transaction-fields';

    $(recommendationFieldSelector).hide();
    $(recommendationLabelSelector).hide();
    $(confirmTransactionSelector).hide();
    $('#add-recommendation').on('click', function (e) {
        e.preventDefault();
        $(this).hide();
        $(recommendationFieldSelector).show();
        $(recommendationLabelSelector).show();
    });

    $('#confirm-transaction').on('click', function (e) {
        e.preventDefault();
        $(this).hide();
        $('.deny-transaction').hide();
        $(confirmTransactionSelector).show();
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

    $('#jurisdiction-clone').on('click', function (event) {
        event.preventDefault();
        var form_idx = $('#id_jurisdiction-TOTAL_FORMS').val();
        $('#jurisdiction-formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_jurisdiction-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    $('#language-clone').on('click', function (event) {
        event.preventDefault();
        var form_idx = $('#id_language-TOTAL_FORMS').val();
        $('#language-formset').append($('#language_empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_language-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    // BROWSING PAGE
    $('.jurisdiction-display').on('click', function (event) {
        // toggle active class
        event.currentTarget.classList.add('active');
        $('.law-type-tag-display')[0].classList.remove('active');
        // toggle selection options
        $('#jurisdictions-row').show();
        $('#law-type-tag-row').hide();
    });

    $('.law-type-tag-display').on('click', function (event) {
        // toggle active class
        event.currentTarget.classList.add('active');
        $('.jurisdiction-display')[0].classList.remove('active');
        // toggle selection options
        $('#law-type-tag-row').show();
        $('#jurisdictions-row').hide();
    });

    $('.jurisdiction').on('click', function (event) {
        window.location.href = '/profiles/jurisdictions/' + $(event.currentTarget).children()[0].innerText + '/law-type-tags/all';
    });

    $('.law-type-tag').on('click', function (event) {
        window.location.href = '/profiles/jurisdictions/all/law-type-tags/' + $(event.currentTarget).children()[0].innerText;
    });

    $('#navigate-back').on('click', function (event) {
        window.history.back();
        return false;
    });

});

$("select").on("select2:select", function (evt) {
    var element = evt.params.data.element;
    var $element = $(element);

    $element.detach();
    $(this).append($element);
    $(this).trigger("change");
});