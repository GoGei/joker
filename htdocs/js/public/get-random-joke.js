$(document).ready(function () {
    $('#getRandomButton').click(function (event) {
        event.preventDefault();

        let sessionKey = 'seenJokes'

        let seenJokes = localStorage.getItem(sessionKey) || [];
        $.ajax({
            url: $(this).data('url'),
            method: 'get',
            data: {'seen_jokes': seenJokes},
            success: function (data, status, xhr) {
                console.log(localStorage.getItem(sessionKey))
                if (!localStorage.getItem(sessionKey)) {
                    console.log('init me')
                    let empty = [];
                    localStorage.setItem(sessionKey, empty);
                }

                if ('add_to_cache' in data) {
                    console.log('add data to cache');
                    let jokeId = data['id'].toString();
                    let seen_jokes = localStorage.getItem(sessionKey);
                    console.log('seen_jokes', seen_jokes)
                    console.log('jokeId', jokeId)
                    seen_jokes.push(jokeId);
                    localStorage.setItem(sessionKey, seen_jokes);
                }

                if ('all_jokes_seen' in data) {
                    console.log('clear all jokes');
                    localStorage.clear();
                }

                console.log(data)
                console.log(localStorage.getItem(sessionKey))
            },
            error: function (jqXhr, textStatus, errorMessage) {
                alert(errorMessage);
            }
        })
    })
})