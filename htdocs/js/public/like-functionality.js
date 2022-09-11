$(document).ready(function () {
    $('.button-like-js').click(function (event) {
        event.preventDefault();
        let $current = $(this)
        let buttonClass = 'button-like';
        let siblingClass = 'button-dislike-js'

        if (!$current.hasClass(buttonClass)) {
            $.ajax({
                url: $current.data('ajax-activate-url'),
                method: 'post',
                delay: 100,
                success: function (data, status, xhr) {
                    $current.addClass(buttonClass);
                    $current.siblings(`.${siblingClass}`).removeClass('button-dislike');
                },
                error: function (jqXhr, textStatus, errorMessage) {
                    let status = jqXhr.status;
                    if (status == 403) {
                        alert('You should be logged in to like the joke');
                    } else {
                        alert(errorMessage);
                    }
                }
            })
        } else {
            $.ajax({
                url: $current.data('ajax-disable-url'),
                method: 'post',
                delay: 100,
                success: function (data, status, xhr) {
                    $current.removeClass(buttonClass);
                },
                error: function (jqXhr, textStatus, errorMessage) {
                    alert(errorMessage);
                }
            })
        }
    });

    $('.button-dislike-js').click(function (event) {
        event.preventDefault();
        let $current = $(this)
        let buttonClass = 'button-dislike';
        let siblingClass = 'button-like-js'

        if (!$current.hasClass(buttonClass)) {
            $.ajax({
                url: $current.data('ajax-activate-url'),
                method: 'post',
                delay: 100,
                success: function (data, status, xhr) {
                    $current.addClass(buttonClass);
                    $current.siblings(`.${siblingClass}`).removeClass('button-like');
                },
                error: function (jqXhr, textStatus, errorMessage) {
                    let status = jqXhr.status;
                    if (status == 403) {
                        alert('You should be logged in to like the joke');
                    } else {
                        alert(errorMessage);
                    }
                }
            })
        } else {
            $.ajax({
                url: $current.data('ajax-disable-url'),
                method: 'post',
                delay: 100,
                success: function (data, status, xhr) {
                    $current.removeClass(buttonClass);
                },
                error: function (jqXhr, textStatus, errorMessage) {
                    alert(errorMessage);
                }
            })
        }
    });
})