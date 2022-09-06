import django_filters
from core.Utils.filtersets import BaseFilterForm
from core.User.models import User


class UserFilterForm(BaseFilterForm):
    SEARCH_FIELDS = ['username', 'email']

    is_staff = django_filters.ChoiceFilter(label='Is staff', method='is_staff_filter', empty_label='Not selected',
                                           choices=[('true', 'Staff'), ('false', 'Not staff')])
    is_superuser = django_filters.ChoiceFilter(label='Is superuser', method='is_superuser_filter',
                                               empty_label='Not selected',
                                               choices=[('true', 'Superuser'), ('false', 'Not superuser')])

    class Meta:
        model = User
        fields = BaseFilterForm.BASE_FILTER_FIELDS

    def is_active_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(is_active=True)
        elif value == 'false':
            queryset = queryset.filter(is_active=False)
        return queryset

    def is_staff_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(is_staff=True)
        elif value == 'false':
            queryset = queryset.filter(is_staff=False)
        return queryset

    def is_superuser_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(is_superuser=True)
        elif value == 'false':
            queryset = queryset.filter(is_superuser=False)
        return queryset
