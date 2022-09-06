from factory import fuzzy

joke_data = {
    'text': fuzzy.FuzzyText(length=100).fuzz()
}

joke_error_data = {
    'text': fuzzy.FuzzyText(length=5000).fuzz()
}

joke_empty_data = {
    'text': None
}

joke_filter_data = {
    'search': joke_data['text'],
    'is_active': 'true',
}
