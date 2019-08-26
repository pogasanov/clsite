import {setDatePicker} from "./global";

$(document).ready(function () {
    setDatePicker();
    $("#success-alert").fadeTo(1500, 500).slideUp(500, function() {
        $("#success-alert").slideUp(500);
    });
})