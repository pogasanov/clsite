import {setDatePicker} from "./global";

$(document).ready(function () {
    setDatePicker();

    const confirmTransactionSelector = '.confirm-transaction-fields';

    $(confirmTransactionSelector).hide();

    $('#confirm-transaction').on('click', function (e) {
        e.preventDefault();
        $(this).hide();
        $('.deny-transaction').hide();
        $(confirmTransactionSelector).show();
    });
})