import {setDatePicker} from "./global";

$(document).ready(function () {
    setDatePicker();
    const transactionProofImageSelector = '#id_proof_receipt_image';
    $(transactionProofImageSelector).hide();

    $("#success-alert").fadeTo(1500, 500).slideUp(500, function() {
        $("#success-alert").slideUp(500);
    });

    $("#id_proof_receipt").change(function(){
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
