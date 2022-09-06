from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator

from core.Utils.validators import PhoneValidator


class PhoneField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(PhoneValidator)


PasswordValidators = (
    MaxLengthValidator(limit_value=20),
    MinLengthValidator(limit_value=8),

)
