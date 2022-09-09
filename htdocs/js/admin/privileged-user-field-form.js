Users = {};

(function (obj, $) {
    function init() {
        let $users = $('#id_user');
        let $exclude_users = $('input#id_excluded_users');
        let to_exclude = $exclude_users.val();
        console.log(to_exclude)

        $users.select2({
            allowClear: true,
            placeholder: $users.attr('placeholder'),
            ajax: {
                url: $users.data('ajax-url'),
                method: 'GET',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        search: params.term,
                        page: params.page,
                        format: 'json',
                        to_exclude: to_exclude
                    }
                },
                processResults: function (data, params) {
                    params.page = params.page || 1;
                    return {
                        pagination: {
                            more: Boolean(data.next)
                        },
                        results: $.map(data.results, function (obj) {
                            return {
                                id: obj.id,
                                text: obj.email
                            }
                        })
                    }
                }
            }
        })
    }

    obj.init = init;
})(Users, jQuery);

$(document).ready(function () {
    console.log('Init users for privileges');
    Users.init();
})