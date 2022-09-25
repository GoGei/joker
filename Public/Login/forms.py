from django.forms import forms, fields
from django import forms as django_forms
from core.User.models import User


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


class RegisterUserForm(django_forms.ModelForm):
    password = fields.CharField(label='Password',
                                widget=fields.TextInput(attrs={
                                    'class': 'form-control', 'type': 'password'
                                }))
    repeat_password = fields.CharField(label='Repeat password',
                                       widget=fields.TextInput(attrs={
                                           'class': 'form-control', 'type': 'password'
                                       }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeat_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            self.add_error('email', 'User with email %s already exists' % email)
        except User.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            self.add_error('username', 'User with username %s already exists' % username)
        except User.DoesNotExist:
            return username

    def clean(self):
        data = super().clean()

        password = data.get('password')
        repeat_password = data.get('repeat_password')

        if password != repeat_password:
            msg = 'Password mismatch'
            self.add_error('password', msg)
            self.add_error('repeat_password', msg)

        return data

    def save(self, commit=True):
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        user = User.objects.create_user(email=email, password=password, username=username, is_active=False)
        user.save()

        return user


class RegisterUserResendForm(forms.Form):
    email = fields.EmailField(label='Email', max_length=128, required=False,
                              widget=fields.TextInput(attrs={
                                  'class': 'form-control', 'placeholder': 'Enter email'
                              }))
    username = fields.CharField(label='Username', max_length=128, required=False,
                                widget=fields.TextInput(attrs={
                                    'class': 'form-control', 'placeholder': 'Enter username'
                                }))

    def clean(self):
        data = super().clean()

        email = data.get('email', None)
        username = data.get('username', None)

        if not (email and username):
            msg = 'Enter email or username'
            self.add_error('email', msg)
            self.add_error('username', msg)

        filters = {'is_active': True}

        if email:
            filters['email'] = email
        if username:
            filters['username'] = username

        qs = User.objects.filter(**filters).all()
        if qs.exists():
            if qs.count() != 1:
                self.add_error(None, 'Found multiple users')
            else:
                user = qs.first()
                data['user'] = user
        else:
            self.add_error(None, 'User by this data is not found')

        return data
