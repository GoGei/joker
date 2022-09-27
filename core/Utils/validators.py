from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

PhoneValidator = RegexValidator(regex=r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$',
                                message=(
                                    "Phone number must be entered in the format: '+380(99)-999-9999'."))

TelegramNicknameValidator = RegexValidator(regex=r'^\B@[a-zA-Z][\w\d]{5,30}[a-zA-Z\d]$',
                                           message="Enter correct telegram nickname")


class ContainsUpperCaseValidator(object):
    def __call__(self, value):
        if not any(e.isupper() for e in value):
            raise ValidationError('Has to contain at least one upper case letter')
        return value


class ContainsLowerCaseValidator(object):
    def __call__(self, value):
        if not any(e.islower() for e in value):
            raise ValidationError('Has to contain at least one lower case letter')
        return value


class ContainsSpecialCharValidator(object):
    def __init__(self, special_chars='!@#$%^&*()-+?_=,<>/'):
        self.special_chars = special_chars

    def __call__(self, value):
        if not any(e in self.special_chars for e in value):
            raise ValidationError('Has to contain at least one special character: "%s"' % self.special_chars)
        return value


PasswordValidators = (
    MaxLengthValidator(limit_value=20),
    MinLengthValidator(limit_value=8),
    ContainsUpperCaseValidator(),
    ContainsLowerCaseValidator(),
    ContainsSpecialCharValidator(special_chars='!@#.'),
)
