$('a.email-send, a.telegram-send').click(function (e) {
    e.preventDefault();

    let $modal = $('#jokeSendToModal');
    let $modalBody = $('#jokeSendToModal .modal-body');
    let $modalSuccessResponse = $('#jokeSendToModalSuccess');
    let $modalErrorResponse = $('#jokeSendToModalError');

    let renderUrl = $(this).data('ajax-form-render-url');
    let actionUrl = $(this).data('ajax-action-url');

    $.ajax({
        url: renderUrl,
        method: 'get'
    }).done(function (data) {
        $modalBody.html(data);
        $modal.modal('show');

        $('#jokeSendToModal form').submit(function (e) {
            e.preventDefault();

            let $form = $(this);

            data = $form.serializeArray();
            $.ajax({
                url: actionUrl,
                method: 'post',
                data: data,
                success: function (data, status, xhr) {
                    $modal.modal('hide');
                    if (data['is_send']) {
                        $modalSuccessResponse.modal('show');
                    } else {
                        $modalErrorResponse.modal('show');
                    }
                },
                error: function (response) {
                    let errors = response.responseJSON;
                    $.each(errors, function (name, messages) {
                        let field = $form.find(`[name=${name}]`);
                        if (field.length) {
                            let row = field.closest('.form-group');
                            row.addClass('has-error');
                            $.each(messages, function (i, message) {
                                $('<div/>', {
                                    'class': 'error-message text-right text-danger',
                                    'text': message
                                }).appendTo(row);
                            });
                        } else {
                            $.each(messages, function (i, message) {
                                $('<div/>', {
                                    'class': 'error-message alert alert-warning',
                                    'text': message
                                }).prependTo($form);
                            });
                        }
                    });
                }
            })
        })
    });
});
