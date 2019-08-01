import {setDatePicker} from "./global";

$(document).ready(function () {
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
})