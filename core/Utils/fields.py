from django import forms

from core.Utils.validators import PhoneValidator


class PhoneField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(PhoneValidator)

