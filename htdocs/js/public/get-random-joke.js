$(document).ready(function () {
    $('#getRandomButton').click(function (event) {
        event.preventDefault();

        $.ajax({
            url: $(this).data('url'),
            method: 'get',
            success: function (data, status, xhr) {
                if ('all_jokes_seen' in data) {
                    console.log('All seen')
                } else {
                    console.log(data)
                }
            },
            error: function (jqXhr, textStatus, errorMessage) {
                alert(errorMessage);
            }
        })
    })
});