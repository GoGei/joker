from factory import fuzzy

user_data = {
    'email': fuzzy.FuzzyText(length=100).fuzz()
}

user_filter_data = {
    'search': user_data['email'],
    'is_active': 'true',
    'is_staff': 'false',
    'is_superuser': 'false',
}
