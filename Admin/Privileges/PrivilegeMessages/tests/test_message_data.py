from factory import fuzzy

message_data = {
    'message': fuzzy.FuzzyText(length=1000).fuzz()
}

message_error_data = {
    'message': fuzzy.FuzzyText(length=2000).fuzz()
}

message_empty_data = {
    'message': None
}
