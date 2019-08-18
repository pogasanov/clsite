import {setDatePicker} from "./global";

$(document).ready(function () {
    setDatePicker();

    const recommendationFieldSelector = '#id_requester_recommendation, #id_requestee_recommendation';
    const recommendationLabelSelector = '[for="id_requester_recommendation"], [for="id_requestee_recommendation"]';
    const confirmTransactionSelector = '.confirm-transaction-fields';
    const transactionProofImageSelector = '#id_proof_receipt_requester_image';

    $(recommendationFieldSelector).hide();
    $(recommendationLabelSelector).hide();
    $(confirmTransactionSelector).hide();
    $(transactionProofImageSelector).hide();

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
    
    $("#id_proof_receipt_requester").change(function(){
        if (this.files && this.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $(transactionProofImageSelector).attr('src', e.target.result);
            };

            $(transactionProofImageSelector).show();
            reader.readAsDataURL(this.files[0]);
        }
    });
});
