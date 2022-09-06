import django_filters
from django import forms
from django.db.models import Q


class BaseFilterForm(django_filters.FilterSet):
    BASE_FILTER_FIELDS = ['is_active', 'search']
    SEARCH_FIELDS = []
    is_active = django_filters.ChoiceFilter(label='Is active', empty_label='Not selected', method='is_active_filter',
                                            choices=[('true', 'Active'), ('false', 'Not active')])
    search = django_filters.CharFilter(label='Search', method='search_qs',
                                       widget=forms.TextInput(attrs={'type': 'search'}))

    def is_active_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(archived_stamp__isnull=True)
        elif value == 'false':
            queryset = queryset.filter(archived_stamp__isnull=False)
        return queryset

    def search_qs(self, queryset, name, value):
        fields = self.SEARCH_FIELDS
        _filter = Q()
        for field in fields:
            _filter |= Q(**{f'{field}__icontains': value})
        queryset = queryset.filter(_filter)
        return queryset
