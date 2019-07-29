import {setDatePicker} from "./global";

$(document).ready(function () {
    setDatePicker();

    const recommendationFieldSelector = '#id_requester_recommendation';
    const recommendationLabelSelector = '[for="id_requester_recommendation"]';

    $(recommendationFieldSelector).hide();
    $(recommendationLabelSelector).hide();
    $('#add-recommendation').on('click', function (e) {
        e.preventDefault();
        $(this).hide();
        $(recommendationFieldSelector).show();
        $(recommendationLabelSelector).show();
    });
})