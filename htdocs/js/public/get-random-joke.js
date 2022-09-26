$(document).ready(function () {
    $('#getRandomButton').click(function (event) {
        event.preventDefault();

        var $modal = $('#jokeShowModal');

        $.ajax({
            url: $(this).data('url'),
            method: 'get',
            success: function (data, status, xhr) {
                if ('all_jokes_seen' in data) {
                    $('#jokeShowModal .modal-body').html(data['text']);
                    $modal.modal('show');
                } else {
                    $('#jokeShowModal .modal-body').html(`<p>${data['text']}</p>`);
                    $modal.modal('show');
                }
            },
            error: function (jqXhr, textStatus, errorMessage) {
                alert(errorMessage);
            }
        })
    })
});