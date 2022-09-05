from django import template

register = template.Library()


@register.simple_tag
def get_message_class(message_tag):
    message_tag_map = {
        'debug': 'alert-light',
        'info': 'alert-info',
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-danger',
        'default': 'alert-dark',
    }
    default = message_tag_map.get('default')
    return message_tag_map.get(message_tag, default)


@register.simple_tag
def url_get_field(request, field):
    if request.method == 'GET':
        _dict = request.GET.copy()
    else:
        _dict = request.POST.copy()

    return _dict.get(field)


@register.simple_tag
def url_replace(request, field, value):
    if request.method == 'GET':
        _dict = request.GET.copy()
    else:
        _dict = request.POST.copy()

    _dict[field] = value
    return _dict.urlencode()


@register.simple_tag
def url_replace_multiple(request, fields, values):
    if request.method == 'GET':
        _dict = request.GET.copy()
    else:
        _dict = request.POST.copy()

    if len(fields) == len(values):
        for field, value in zip(fields, values):
            _dict[field] = value
    else:
        raise ValueError('Length of fields and values have to be equal!')

    return _dict.urlencode()
