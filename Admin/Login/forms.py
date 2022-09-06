from django.forms import forms, fields


class LoginForm(forms.Form):
    email = fields.EmailField(label='Email', max_length=128, required=True,
                              widget=fields.TextInput(attrs={
                                  'class': 'form-control', 'placeholder': 'Enter email'
                              }))
    password = fields.CharField(label='Password', min_length=8, max_length=20, required=True,
                                widget=fields.TextInput(attrs={
                                    'class': 'form-control', 'type': 'password',
                                    'placeholder': 'Enter password'
                                }))
    remember_me = fields.BooleanField(label='Remember me', required=False,
                                      widget=fields.CheckboxInput(attrs={
                                          'name': 'remember_me', 'value': 'remember-me'
                                      }))
