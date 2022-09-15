$(document).ready(function () {
    $('#getRandomButton').click(function (event) {
        event.preventDefault();

        let seenJokes = $.sessionStorage.getItem('seen_jokes');
        $.ajax({
            url: $(this).data('url'),
            method: 'get',
            data: {'seen_jokes': seenJokes},
            success: function (data, status, xhr) {
                if (!$.sessionStorage.getItem('seen_jokes')){
                    $.sessionStorage.getItem('seen_jokes');
                }

                if ('add_to_cache' in data) {
                    let jokeId = data['id'];
                    $.sessionStorage.getItem('seen_jokes');
                    console.log('add data to cache');
                }

                if ('all_jokes_seen' in data) {
                    $.sessionStorage.getItem('seen_jokes');
                    console.log('all jokes are seen');
                    console.log('clear all jokes');
                }

                console.log(data)
            },
            error: function (jqXhr, textStatus, errorMessage) {
                alert(errorMessage);
            }
        })
    })
})