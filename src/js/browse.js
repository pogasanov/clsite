$(document).ready(function () {
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
})