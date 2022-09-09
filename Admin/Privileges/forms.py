from django import forms
from django_hosts import reverse

from core.Utils.filtersets import BaseSearchFilterMixin
from core.User.models import User
from core.Privilege.models import PrivilegeUser


class PrivilegeUserFilterForm(BaseSearchFilterMixin):
    SEARCH_FIELDS = ['user__email']

    class Meta:
        model = PrivilegeUser
        fields = BaseSearchFilterMixin.BASE_FILTER_FIELDS


class PrivilegeUserForm(forms.ModelForm):
    excluded_users = forms.CharField(required=False,
                                     widget=forms.HiddenInput(attrs={
                                         'name': 'hidden_exclude_users',
                                         'value': ','.join(map(str, PrivilegeUser.objects.all()
                                                               .values_list('user_id', flat=True)))
                                     }))
    user = forms.ModelChoiceField(label='Privileged user',
                                  queryset=User.objects.filter(is_active=True, is_superuser=False),
                                  empty_label='Select a user',
                                  widget=forms.Select(attrs={'class': 'form-control select2',
                                                             'placeholder': 'Select a user',
                                                             'data-ajax-url': reverse('api-v1:users-admin-list',
                                                                                      host='api')}))

    class Meta:
        model = PrivilegeUser
        fields = ['user']

    def clean_user(self):
        user = self.cleaned_data.get('user')
        instance = self.instance or None

        if instance:
            qs = PrivilegeUser.objects.select_related('user').filter(user=user)
            if qs.exists():
                self.add_error('user', 'Privileged user already added!')

        return user


class PrivilegeUserAddForm(PrivilegeUserForm):
    pass
