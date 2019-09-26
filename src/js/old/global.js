function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setDatePicker() {
    $(".datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        maxDate: 0,
        showAnim: 'slideDown'
    });
}

$("select").on("select2:select", function (evt) {
    let element = evt.params.data.element;
    let $element = $(element);

    $element.detach();
    $(this).append($element);
    $(this).trigger("change");
});

export {getCookie, setDatePicker}